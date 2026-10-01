-- hypeForge: the KognogOS Hyprland desktop. Hyprland 0.56+, Lua settings only (D-3, D-5).
--
-- Everything lives in one portable folder, ~/.config/hypeforge/ (D-8, D-28). ~/.config/hypr
-- points into it. Details that belong to one computer (screens, graphics card) go in
-- machines/<hostname>/, loaded at the end of this file when that folder exists.
--
-- Background helpers (Noctalia the desktop shell, idle lock, password pop-up, USB drives)
-- run as systemd user services under uwsm, not from here (D-25, D-40).

local HOME = os.getenv("HOME")
HYPEFORGE_DIR = HOME .. "/.config/hypeforge"
package.path = HYPEFORGE_DIR .. "/hypr/?.lua;" .. package.path

-- Apps started from keys go through uwsm, so each one gets its own place in the session (D-25).
local function app(cmd) return hl.dsp.exec_cmd("uwsm app -- " .. cmd) end
HYPEFORGE_APP = app

local terminal = "alacritty"

-- Screens: every screen at its best mode, side by side. A machine file can replace this.
hl.monitor({ output = "", mode = "highrr", position = "auto", scale = 1 })

-- Look ---------------------------------------------------------------------------------------
hl.config({
    general = {
        border_size = 2,
        resize_on_border = true,        -- drag a border to resize, like Plasma
        layout = "dwindle",
    },
    decoration = {
        rounding = 8,
        shadow = { enabled = true, range = 12, render_power = 3, color = 0x661a1a1a },
        blur = { enabled = true, size = 4, passes = 2 },
    },
    animations = { enabled = true },
    dwindle = { preserve_split = true },
    misc = {
        force_default_wallpaper = 0,    -- our wallpaper comes from hyprpaper
        disable_hyprland_logo = true,
        disable_splash_rendering = true,
        focus_on_activate = true,
    },
    input = {
        kb_layout = "us",
        follow_mouse = 1,
        sensitivity = 0,
        touchpad = { natural_scroll = true },
    },
    cursor = { no_hardware_cursors = 2 },   -- 2 = automatic: software cursors where hardware ones break
})

hl.curve("easeOutQuint", { type = "bezier", points = { { 0.23, 1 }, { 0.32, 1 } } })
hl.curve("almostLinear", { type = "bezier", points = { { 0.5, 0.5 }, { 0.75, 1 } } })
hl.animation({ leaf = "global",  enabled = true, speed = 10,  bezier = "default" })
hl.animation({ leaf = "windows", enabled = true, speed = 4,   bezier = "easeOutQuint", style = "popin 90%" })
hl.animation({ leaf = "fade",    enabled = true, speed = 3,   bezier = "almostLinear" })
hl.animation({ leaf = "layers",  enabled = true, speed = 3.8, bezier = "easeOutQuint", style = "fade" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 2, bezier = "almostLinear", style = "fade" })

-- Themes first: the title bars read their colours from it (D-36).
require("theme")
-- Floating-first windows, Win + arrow snapping, Alt + Tab, Alt + F4, Win + Return (D-7, D-30..D-35).
require("snap")
-- Title bars for windows that do not draw their own (D-31, D-33). The plugin is a package
-- (hyprland-plugin-hyprbars), locked to this Hyprland version through nog (D-9).
local ok, err = pcall(hl.plugin.load, "/usr/lib/libhyprbars.so")
if ok then require("titlebars") else print("hypeForge: title bars not loaded: " .. tostring(err)) end

-- Keys (D-29: Plasma's keys keep their jobs) --------------------------------------------------
-- Windows: snapping, maximise, restore, Alt + F4, Alt + Tab and Win + T live in snap.lua.
hl.bind("SUPER + CTRL + ESCAPE", hl.dsp.exec_cmd("hyprctl kill"), { description = "Force-quit a window" })
for key, dir in pairs({ LEFT = "left", RIGHT = "right", UP = "up", DOWN = "down" }) do
    hl.bind("SUPER + ALT + " .. key, hl.dsp.focus({ direction = dir }), { description = "Focus " .. dir })
end
hl.bind("SUPER + SHIFT + LEFT",  hl.dsp.window.move({ monitor = "l" }), { description = "Window to the screen on the left" })
hl.bind("SUPER + SHIFT + RIGHT", hl.dsp.window.move({ monitor = "r" }), { description = "Window to the screen on the right" })

-- Apps and menus. The launcher opens when Win is tapped alone (released without another key).
-- Noctalia, the desktop shell (D-40), answers these through its remote control.
local function noctalia(cmd) return hl.dsp.exec_cmd("noctalia msg " .. cmd) end
hl.bind("SUPER + SUPER_L", noctalia("panel-toggle launcher"), { release = true, description = "Launcher" })
hl.bind("SUPER + V", noctalia("panel-toggle clipboard"), { description = "Clipboard history" })
hl.bind("SUPER + K", app("krusader"), { description = "File manager" })
hl.bind("SUPER + E", app(terminal .. " -e superfile"), { description = "Terminal file manager" })
hl.bind("SUPER + L", hl.dsp.exec_cmd("loginctl lock-session"), { description = "Lock the screen" })
hl.bind("CTRL + ALT + DELETE", noctalia("panel-toggle session"), { description = "Power menu" })
hl.bind("SUPER + ALT + T", hl.dsp.exec_cmd("bash " .. HYPEFORGE_DIR .. "/bin/hypeforge-theme-next"), { description = "Next theme" })
hl.bind("CTRL + ESCAPE", app(terminal .. " -e btop"), { description = "System monitor" })
hl.bind("SUPER + SHIFT + C", hl.dsp.exec_cmd("hyprpicker -a"), { description = "Colour picker" })
hl.bind("SUPER + F1", app("bash " .. HYPEFORGE_DIR .. "/bin/hypeforge-keys"), { description = "Keyboard shortcuts (this list)" })

-- Screenshots (Spectacle's keys). Satty lets you draw on the picture before saving.
local shots = "$(xdg-user-dir PICTURES)/Screenshots"
local function shot(grim_args)
    return hl.dsp.exec_cmd("mkdir -p " .. shots .. " && grim " .. grim_args ..
        " " .. shots .. "/$(date +%Y%m%d-%H%M%S).png")
end
local box_and_draw = hl.dsp.exec_cmd("grim -g \"$(slurp)\" - | satty --filename - --output-filename " ..
    shots .. "/$(date +%Y%m%d-%H%M%S).png --copy-command wl-copy")
hl.bind("Print", box_and_draw, { description = "Screenshot: drag a box, then draw" })
hl.bind("SUPER + SHIFT + S", box_and_draw, { description = "Screenshot: drag a box, then draw" })
hl.bind("SHIFT + Print", shot(""), { description = "Screenshot: whole desktop" })
hl.bind("SUPER + SHIFT + Print", hl.dsp.exec_cmd("mkdir -p " .. shots ..
    " && grim -g \"$(slurp)\" " .. shots .. "/$(date +%Y%m%d-%H%M%S).png"), { description = "Screenshot: a box, saved straight away" })
hl.bind("SUPER + Print", hl.dsp.exec_cmd("mkdir -p " .. shots .. " && grim -g \"$(hyprctl activewindow -j | " ..
    "jq -r '\"\\(.at[0]),\\(.at[1]) \\(.size[0])x\\(.size[1])\"')\" " .. shots .. "/$(date +%Y%m%d-%H%M%S).png"),
    { description = "Screenshot: the active window" })

-- Sound, media and brightness, with Noctalia's on-screen pop-ups (D-40).
hl.bind("XF86AudioRaiseVolume", noctalia("volume-up"),   { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", noctalia("volume-down"), { locked = true, repeating = true })
hl.bind("SHIFT + XF86AudioRaiseVolume", noctalia("volume-up 1"),   { locked = true, repeating = true })
hl.bind("SHIFT + XF86AudioLowerVolume", noctalia("volume-down 1"), { locked = true, repeating = true })
hl.bind("XF86AudioMute",    noctalia("volume-mute"), { locked = true })
hl.bind("XF86AudioMicMute", noctalia("mic-mute"),    { locked = true })
hl.bind("SUPER + XF86AudioMute", noctalia("mic-mute"), { locked = true })
hl.bind("XF86AudioPlay",  noctalia("media toggle"),   { locked = true })
hl.bind("XF86AudioPause", noctalia("media toggle"),   { locked = true })
hl.bind("XF86AudioNext",  noctalia("media next"),     { locked = true })
hl.bind("XF86AudioPrev",  noctalia("media previous"), { locked = true })
-- Laptop brightness. Desktop monitors use ddcutil instead, set in the machine file (D-20).
hl.bind("XF86MonBrightnessUp",   noctalia("brightness-up"),   { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", noctalia("brightness-down"), { locked = true, repeating = true })

-- Zoom (Win + = / - / 0).
local function zoom(expr)
    return function()
        local z = tonumber(hl.get_config("cursor.zoom_factor")) or 1
        z = math.max(1, expr(z))
        hl.config({ cursor = { zoom_factor = z } })
    end
end
hl.bind("SUPER + equal", zoom(function(z) return z * 1.25 end), { description = "Zoom in" })
hl.bind("SUPER + minus", zoom(function(z) return z / 1.25 end), { description = "Zoom out" })
hl.bind("SUPER + 0",     zoom(function() return 1 end),        { description = "Zoom back to normal" })

-- Drag windows with Win + left mouse, resize with Win + right mouse.
hl.bind("SUPER + mouse:272", hl.dsp.window.drag(),   { mouse = true })
hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })

-- Rules -----------------------------------------------------------------------------------------
-- XWayland drag-and-drop helper windows must not take focus (from Hyprland's own example).
hl.window_rule({
    name = "hypeforge-xwayland-drags",
    match = { class = "^$", title = "^$", xwayland = true, float = true, fullscreen = false, pin = false },
    no_focus = true,
})
-- Noctalia's settings window: a normal-sized floating window (its docs suggest floating).
hl.window_rule({
    name = "hypeforge-noctalia-settings",
    match = { class = "^(dev.noctalia.Noctalia)$" },
    size = { "(monitor_w*0.6)", "(monitor_h*0.7)" },
    center = true,
})
-- Picture-in-picture stays on top, small, in a corner.
hl.window_rule({
    name = "hypeforge-pip",
    match = { title = "^(Picture.in.[Pp]icture)$" },
    pin = true,
    size = { "(monitor_w*0.25)", "(monitor_h*0.25)" },
})

-- This computer's own details, if any: machines/<hostname>/machine.lua (D-28).
local host = (io.open("/etc/hostname") or { read = function() return "" end, close = function() end })
local name = host:read("*l") or ""
host:close()
local machine = HYPEFORGE_DIR .. "/machines/" .. name .. "/machine.lua"
local f = io.open(machine, "r")
if f then f:close(); dofile(machine) end
-- Screen layout saved by Monique, the screen settings app (F-5), in the same folder.
local monitors = HYPEFORGE_DIR .. "/machines/" .. name .. "/monitors.lua"
f = io.open(monitors, "r")
if f then f:close(); dofile(monitors) end
