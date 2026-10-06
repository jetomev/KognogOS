#!/usr/bin/env bash
# NOTE (2026-10-06): written for the first hypeForge disc (Hyprland, retired 2026-10-05) and
# saved onto main when that branch was deleted (tag archive/hypeforge-edition-hyprland).
# Desktop-agnostic except the login step (SDDM, below): the Sway login screen is not chosen
# yet. Issue #2.
# kognog-install — install KognogOS from the live disc onto one whole disk.
#
#   sudo kognog-install /dev/vda
#
# The first, small version of KognogOS's installer (issue #2), written for the
# hypeForge edition's VM test (2026-09-30). installForge, the real terminal app,
# grows out of it later.
#
# How: it copies the live system exactly as it is on the disc (the method
# Calamares-based distros use), then takes out the live-only parts, and sets up
# the parts every computer needs for itself: start-up (initramfs + GRUB), the
# login screen, a user, a name, a time zone.
#
# Layout: UEFI only. GPT, a 1 GiB EFI partition at /boot/efi, the rest btrfs with
# subvolumes @ @home @snapshots @var_log @pkg (the layout grub-btrfs snapshots use).
#
# THE WHOLE DISK IS ERASED. It asks you to type the disk's name before it does.
set -euo pipefail

LIVE=/run/archiso/airootfs              # the disc's pristine system (squashfs), read-only
LOG=/tmp/kognog-install.log             # everything shown is also saved here, then copied
                                        # into the new system as /var/log/kognog-install.log
MNT=/mnt
say()  { printf '\n\033[1;35m==> %s\033[0m\n' "$*"; }
die()  { printf '\n\033[1;31m!! %s\033[0m\n' "$*" >&2; exit 1; }
ask()  { local a; read -r -p "$1 [$2]: " a; echo "${a:-$2}"; }

exec > >(tee -a "$LOG") 2>&1
echo "kognog-install started $(date)"

# 1 · Checks -----------------------------------------------------------------------------
[[ $EUID -eq 0 ]]                || die "run it with sudo"
[[ -d $LIVE/usr ]]               || die "this only runs from the KognogOS live disc"
[[ -d /sys/firmware/efi ]]       || die "this computer did not start in UEFI mode; this version needs UEFI"
DISK="${1:-}"
[[ -b $DISK ]]                   || { lsblk -dpno NAME,SIZE,MODEL | grep -v loop; die "usage: kognog-install /dev/<disk>"; }
findmnt -rno SOURCE | grep -q "^$DISK" && die "$DISK is in use (mounted)"

# 2 · Questions --------------------------------------------------------------------------
say "About you and this computer"
USERNAME=$(ask "User name (lower case)" "javier")
[[ $USERNAME =~ ^[a-z_][a-z0-9_-]*$ ]] || die "a user name is lower-case letters, digits, - and _"
FULLNAME=$(ask "Full name" "$USERNAME")
HOST=$(ask "Computer name" "kognogos")
TZONE=$(ask "Time zone" "America/New_York")
[[ -f /usr/share/zoneinfo/$TZONE ]] || die "unknown time zone: $TZONE"
KEYMAP=$(ask "Keyboard layout" "us")

say "The disk"
lsblk -po NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS "$DISK"
echo
echo "EVERYTHING on $DISK will be erased."
read -r -p "Type the disk's name ($DISK or ${DISK#/dev/}) to go ahead, anything else stops: " CONFIRM
[[ $CONFIRM == "$DISK" || $CONFIRM == "${DISK#/dev/}" ]] || die "stopped; nothing was changed"

# 3 · Disk -------------------------------------------------------------------------------
say "Partitioning $DISK"
sgdisk --zap-all "$DISK"
sgdisk -n1:0:+1G -t1:EF00 -c1:EFI -n2:0:0 -t2:8300 -c2:KognogOS "$DISK"
partprobe "$DISK"; udevadm settle
P1=$(lsblk -lnpo NAME "$DISK" | sed -n 2p)
P2=$(lsblk -lnpo NAME "$DISK" | sed -n 3p)
mkfs.fat -F32 -n EFI "$P1"
mkfs.btrfs -f -L KognogOS "$P2"

say "btrfs subvolumes"
mount "$P2" $MNT
for sv in @ @home @snapshots @var_log @pkg; do btrfs subvolume create "$MNT/$sv"; done
umount $MNT
OPTS=noatime,compress=zstd:1
mount -o $OPTS,subvol=@ "$P2" $MNT
mkdir -p $MNT/{home,.snapshots,var/log,var/cache/pacman/pkg,boot/efi}
mount -o $OPTS,subvol=@home      "$P2" $MNT/home
mount -o $OPTS,subvol=@snapshots "$P2" $MNT/.snapshots
mount -o $OPTS,subvol=@var_log   "$P2" $MNT/var/log
mount -o $OPTS,subvol=@pkg       "$P2" $MNT/var/cache/pacman/pkg
mount "$P1" $MNT/boot/efi

# 4 · Copy the live system ---------------------------------------------------------------
say "Copying KognogOS onto the disk (a few minutes)"
rsync -aAXH --info=progress2 --exclude='/home/liveuser' "$LIVE/" $MNT/
KVER=$(ls $MNT/usr/lib/modules | head -1)
install -m644 "$MNT/usr/lib/modules/$KVER/vmlinuz" $MNT/boot/vmlinuz-linux
genfstab -U $MNT > $MNT/etc/fstab

# 5 · Inside the new system --------------------------------------------------------------
say "Setting up the new system"
cat > $MNT/root/kognog-setup.sh <<SETUP
set -euo pipefail
cd /

# Take out the live-only parts: the live user and its auto-login, the disc's own
# start-up recipe, and services that only make sense on the disc.
userdel liveuser 2>/dev/null || true
groupdel liveuser 2>/dev/null || true
rm -f /etc/sudoers.d/00-live /etc/motd /root/.automated_script.sh /root/.zlogin
rm -rf /etc/systemd/system/getty@tty1.service.d /etc/ssh/sshd_config.d/10-archiso.conf \\
       /etc/systemd/journald.conf.d/volatile-storage.conf /etc/systemd/logind.conf.d/do-not-suspend.conf \\
       /etc/systemd/resolved.conf.d/archiso.conf /etc/systemd/system-generators/systemd-gpt-auto-generator \\
       /etc/mkinitcpio.conf.d/archiso.conf /etc/pacman.d/hooks/uncomment-mirrors.hook \\
       /etc/pacman.d/hooks/zzzz99-remove-custom-hooks-from-airootfs.hook
for u in choose-mirror pacman-init livecd-talk livecd-alsa-unmuter etc-pacman.d-gnupg; do
    rm -f /etc/systemd/system/\$u.* /etc/systemd/system/*/\$u.*
done
systemctl disable sshd.service vboxservice.service vmtoolsd.service vmware-vmblock-fuse.service \\
    hv_fcopy_daemon.service hv_kvp_daemon.service hv_vss_daemon.service 2>/dev/null || true
rm -rf /etc/systemd/system/cloud-init.target.wants
# Package signing keys: the disc kept them in memory only.
pacman-key --init
pacman-key --populate archlinux
pacman -Q chaotic-keyring >/dev/null 2>&1 && pacman-key --populate chaotic || true

# Name, time, language, keyboard.
echo "$HOST" > /etc/hostname
ln -sf /usr/share/zoneinfo/$TZONE /etc/localtime
hwclock --systohc
sed -i 's/^#en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen
locale-gen
echo LANG=en_US.UTF-8 > /etc/locale.conf
echo KEYMAP=$KEYMAP > /etc/vconsole.conf

# Start-up: KognogOS's initramfs recipe (issue #2: an install must not boot like stock Arch).
cat > /etc/mkinitcpio.d/linux.preset <<'EOF'
# mkinitcpio preset for the 'linux' package (KognogOS)
ALL_kver='/boot/vmlinuz-linux'
PRESETS=('default' 'fallback')
default_image='/boot/initramfs-linux.img'
fallback_image='/boot/initramfs-linux-fallback.img'
fallback_options='-S autodetect'
EOF
cat > /etc/mkinitcpio.conf.d/kognog.conf <<'EOF'
# KognogOS: the splash (plymouth) right after base + udev.
HOOKS=(base udev plymouth autodetect microcode modconf kms keyboard keymap consolefont block filesystems fsck)
EOF
for p in mkinitcpio-archiso archinstall clonezilla cloud-init livecd-sounds; do
    pacman -Q \$p >/dev/null 2>&1 && pacman -Rns --noconfirm \$p || true
done
# (removed after the start-up recipe above is in place, so the rebuild pacman
# triggers uses KognogOS's recipe, not the disc's)
mkinitcpio -P

# GRUB, with the KognogOS theme and the splash on the kernel line (F-1).
install -d /boot/grub/themes
cp -r /usr/share/kognog/grub-theme/kognogos /boot/grub/themes/
sed -i 's/^GRUB_DISTRIBUTOR=.*/GRUB_DISTRIBUTOR="KognogOS"/; s/^GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash loglevel=3"/' /etc/default/grub
sed -i 's|^#\?GRUB_THEME=.*|GRUB_THEME="/boot/grub/themes/kognogos/theme.txt"|; s|^#\?GRUB_GFXMODE=.*|GRUB_GFXMODE=auto|' /etc/default/grub
grep -q '^GRUB_THEME=' /etc/default/grub || echo 'GRUB_THEME="/boot/grub/themes/kognogos/theme.txt"' >> /etc/default/grub
# GRUB 2.16 lists every firmware boot entry as "(EFI BootNext)" (DVD drive, shell,
# firmware apps). KognogOS's menu shows systems, not firmware plumbing (F-19).
grep -q '^GRUB_DISABLE_BOOTNEXT=' /etc/default/grub || echo 'GRUB_DISABLE_BOOTNEXT=true' >> /etc/default/grub
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=KognogOS
# Also the standard fallback copy, EFI/BOOT/BOOTX64.EFI (F-18): firmware always looks
# there, so the system still starts when the firmware's own boot list is reset or lost
# (a BIOS update, a CMOS reset, some VMs). Found when the VM lost its KognogOS entry.
grub-install --target=x86_64-efi --efi-directory=/boot/efi --removable
grub-mkconfig -o /boot/grub/grub.cfg

# Login: KognogOS's own SDDM greeter (D-38), without the disc's auto-login.
rm -f /etc/sddm.conf.d/autologin.conf

# The user. /etc/skel already holds the hypeForge desktop and the KognogOS shell.
useradd -m -G wheel -s /usr/bin/fish -c "$FULLNAME" "$USERNAME"
echo '%wheel ALL=(ALL:ALL) ALL' > /etc/sudoers.d/20-wheel
chmod 440 /etc/sudoers.d/20-wheel

systemctl enable NetworkManager.service bluetooth.service sddm.service
SETUP
arch-chroot $MNT bash /root/kognog-setup.sh
rm $MNT/root/kognog-setup.sh

say "A password for $USERNAME"
until arch-chroot $MNT passwd "$USERNAME"; do echo "Try again."; done

say "Done"
echo "== INSTALL FINISHED OK"
cp "$LOG" $MNT/var/log/kognog-install.log
umount -R $MNT
echo "KognogOS is installed on $DISK. Take the disc out and restart: sudo reboot"
