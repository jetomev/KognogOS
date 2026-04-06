import subprocess, json, urllib.request
from rich.console import Console
from rich.text import Text

console = Console()

def get(cmd):
    try: return subprocess.check_output(cmd, shell=True, text=True).strip()
    except: return "N/A"

def bar(pct, width=22):
    filled = round(pct * width / 100)
    empty  = width - filled
    color  = "#a6e3a1" if pct < 60 else "#f9e2af" if pct < 85 else "#f38ba8"
    b = Text()
    b.append("|" * filled, style=color)
    b.append("." * empty,  style="#313244")
    return b

# ── Gather system info ────────────────────────────────────────────────────────
user     = get("whoami")
host     = get("cat /etc/hostname")
os_name  = get("grep '^PRETTY_NAME' /etc/os-release | cut -d= -f2 | tr -d '\"'")
kernel   = get("uname -r")
desktop  = get("echo $XDG_CURRENT_DESKTOP")
cpu      = get("grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | sed 's/^ //;s/(R)//g;s/(TM)//g;s/ with.*//;s/ Processor.*//'")
gpu      = get("lspci 2>/dev/null | grep -i 'vga\\|3d' | head -1 | sed 's/.*\\[//;s/\\].*//'")
uptime   = get("uptime -p | sed 's/up //'")
mem_used = get("free -h | awk '/^Mem:/ {print $3}'")
mem_tot  = get("free -h | awk '/^Mem:/ {print $2}'")
mem_pct  = int(get("free | awk '/^Mem:/ {printf \"%.0f\", $3/$2*100}'") or 0)
dsk_used = get("df -h / | awk 'NR==2 {print $3}'")
dsk_tot  = get("df -h / | awk 'NR==2 {print $2}'")
dsk_pct  = int(get("df / | awk 'NR==2 {print $5}'").replace('%','') or 0)
cpu_pct  = int(get("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$3+$4+$5)} END {printf \"%.0f\", usage}'") or 0)

# ── Check for actionable tier updates ────────────────────────────────────────
def get_available_updates():
    try:
        out = subprocess.check_output("checkupdates 2>/dev/null", shell=True, text=True).strip()
        if not out:
            return {}
        updates = {}
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 1:
                updates[parts[0]] = parts[3] if len(parts) >= 4 else ""
        return updates
    except:
        return {}

def get_tier1_packages():
    try:
        out = subprocess.check_output(
            "grep -A100 '\\[tier1\\]' /etc/nog/tier-pins.toml | grep -A100 'packages' | grep '\"' | sed 's/.*\"//;s/\".*//'",
            shell=True, text=True).strip()
        return [p.strip().strip('",') for p in out.splitlines() if p.strip().strip('",')]
    except:
        return []

def get_tier2_packages():
    try:
        out = subprocess.check_output(
            "grep -A100 '\\[tier2\\]' /etc/nog/tier-pins.toml | grep -A100 'packages' | grep -B100 '\\[tier3\\]' | grep '\"' | sed 's/.*\"//;s/\".*//'",
            shell=True, text=True).strip()
        return [p.strip().strip('",') for p in out.splitlines() if p.strip().strip('",')]
    except:
        return []

available   = get_available_updates()
tier1_pkgs  = get_tier1_packages()
tier2_pkgs  = get_tier2_packages()

tier1_ready = [p for p in tier1_pkgs if p in available]
tier2_ready = [p for p in tier2_pkgs if p in available]

# ── Render ────────────────────────────────────────────────────────────────────

console.print()

# Logo line
logo = Text()
logo.append("Kognog ", style="bold #89b4fa")
logo.append("OS", style="bold #cdd6f4")
logo.append("  ", style="")
logo.append("SEMI-ROLLING ARCH · TIER-AWARE", style="#585b70")
console.print(logo)

# Top divider
console.print("─" * 90, style="#89b4fa")

# Two column info
col_w = 14
rows = [
    ("OS",      os_name,  "CPU",    f"{cpu_pct}%",          bar(cpu_pct)),
    ("Kernel",  kernel,   "Memory", f"{mem_used}/{mem_tot}", bar(mem_pct)),
    ("Desktop", desktop,  "Disk",   f"{dsk_used}/{dsk_tot}", bar(dsk_pct)),
    ("CPU",     cpu,      "",       "",                       None),
    ("GPU",     gpu,      "",       "",                       None),
    ("Uptime",  uptime,   "",       "",                       None),
]

for label1, val1, label2, val2, barval in rows:
    line = Text()
    line.append(f"{label1:<10}", style="#89b4fa")
    line.append(f"{val1:<32}", style="#cdd6f4")
    if label2:
        line.append(f"{label2:<10}", style="#89b4fa")
        line.append(f"{val2:<12}", style="#6c7086")
        if barval:
            line.append_text(barval)
    console.print(line)

# ── Tier notifications ────────────────────────────────────────────────────────
if tier1_ready or tier2_ready:
    console.print("─" * 90, style="#313244")

if tier1_ready:
    t1 = Text()
    t1.append("⚠ Tier 1 ready for sign-off: ", style="bold #f38ba8")
    t1.append("  nog unlock <pkg> --promote", style="#cba6f7")
    console.print(t1)
    console.print("  " + "  ·  ".join(tier1_ready), style="#f38ba8")

if tier2_ready:
    t2 = Text()
    t2.append("✓ Tier 2 ready to install: ", style="bold #a6e3a1")
    t2.append("  nog update", style="#cba6f7")
    console.print(t2)
    console.print("  " + "  ·  ".join(tier2_ready), style="#a6e3a1")

# Bottom divider
console.print("─" * 90, style="#313244")

# ── Weather ───────────────────────────────────────────────────────────────────
try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=25.77&longitude=-80.19&current_weather=true&temperature_unit=fahrenheit"
    with urllib.request.urlopen(url, timeout=3) as res:
        data = json.loads(res.read())
        temp = data['current_weather']['temperature']
        wind = data['current_weather']['windspeed']
        console.print(f"  [#f9e2af]Miami  {temp}°F[/#f9e2af]  [#cdd6f4]💨 {wind} km/h[/#cdd6f4]")
except:
    pass

# ── Welcome message ───────────────────────────────────────────────────────────
welcome = Text()
welcome.append("\n  Welcome ", style="#a6e3a1")
welcome.append(user, style="bold #f5c2e7")
welcome.append(", let's rock this session! 🧙\n", style="#a6e3a1")
console.print(welcome)