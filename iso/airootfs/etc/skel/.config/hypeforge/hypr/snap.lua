-- hypeForge prototype: floating-first windows with Plasma's Win + arrow snapping.
-- Hyprland 0.56+ (Lua). Research: docs/research/2026-09-28-floating-first-and-omarchy-vm.md
-- Load it last, after any config that binds the same keys:  require("hypr.hypeforge-snap")
--
-- Keys (Plasma's defaults, D-29):
--   Win + Left/Right/Up/Down   snap to halves; combine into quarters (KWin's rules)
--   Win + Up at the top        maximise; Win + Down on a maximised window: back to its half (D-30)
--   Win + PageUp               maximise / restore
--   Win + Backspace            put the window back to its size before the first snap
--   Win + T                    switch this window between floating and tiled
--   Alt + F4                   close the window
--   Win + Return               open Alacritty
--   Alt + Tab / Alt + Shift + Tab   next / previous window, brought to the front (D-35)
-- New windows open floating at 80 % of the screen, centred; an app's "maximise me" in its
-- first moments is undone (D-32).

local M = {}

-- 1. Every new window floats. ---------------------------------------------------
hl.window_rule({
    name = "hypeforge-float-everything",
    match = { class = ".*" },
    float = true,
})

-- Normal windows open at 80 % of the screen, centred (D-32). Dialogs ("modal" windows,
-- like "Are you sure?") keep the size they ask for.
hl.window_rule({
    name = "hypeforge-open-80",
    match = { class = ".*", modal = false },
    size = { "(monitor_w*0.8)", "(monitor_h*0.8)" },
    center = true,
})

-- Space around windows (D-33): 8 between windows, 13 at the screen edges.
hl.config({ general = { gaps_in = 8, gaps_out = 13 } })

-- 2. Geometry helpers. ------------------------------------------------------------
local function sides(v, d)
    if type(v) == "number" then return { top = v, right = v, bottom = v, left = v } end
    if type(v) == "string" then local n = tonumber(v) or d; return { top = n, right = n, bottom = n, left = n } end
    v = type(v) == "table" and v or {}
    return {
        top = v.top or v[1] or d, right = v.right or v[2] or d,
        bottom = v.bottom or v[3] or d, left = v.left or v[4] or d,
    }
end

local function num(v, d)
    if type(v) == "table" then v = v[1] or v.top end
    return tonumber(v) or d
end

-- The usable box of a monitor, in whole-desktop coordinates (minus the bar and outer gaps).
local function work_area(mon)
    local s = (mon.scale and mon.scale > 0) and mon.scale or 1
    local w, h = mon.width / s, mon.height / s        -- width/height are raw pixels
    if (mon.transform or 0) % 2 == 1 then w, h = h, w end
    local r = sides(mon.reserved, 0)
    local g = sides(hl.get_config("general.gaps_out"), 10)
    return {
        x = mon.x + r.left + g.left, y = mon.y + r.top + g.top,
        w = w - r.left - r.right - g.left - g.right,
        h = h - r.top - r.bottom - g.top - g.bottom,
    }
end

-- 3. Snap zones, as horizontal part x vertical part. ---------------------------------
-- h: "L", "R" or "F" (full width); v: "T", "B" or "F" (full height).
local FRAC = { L = { 0, .5 }, R = { .5, 1 }, T = { 0, .5 }, B = { .5, 1 }, F = { 0, 1 } }

local state = {}   -- per window address: { h, v, saved = {x, y, w, h} }

local function place(win, h, v)
    local target = "address:" .. win.address
    local a = work_area(win.monitor)
    local b = num(hl.get_config("general.border_size"), 2)
    local gi = num(hl.get_config("general.gaps_in"), 5)
    local x0, x1 = a.x + a.w * FRAC[h][1], a.x + a.w * FRAC[h][2]
    local y0, y1 = a.y + a.h * FRAC[v][1], a.y + a.h * FRAC[v][2]
    -- Inner edges (where two snapped windows meet) get the gap between windows.
    if FRAC[h][1] > 0 then x0 = x0 + gi end
    if FRAC[h][2] < 1 then x1 = x1 - gi end
    if FRAC[v][1] > 0 then y0 = y0 + gi end
    if FRAC[v][2] < 1 then y1 = y1 - gi end
    -- at/size exclude the border, so shrink by it. Resize first: a floating resize keeps the centre.
    hl.dispatch(hl.dsp.window.resize({ x = math.floor(x1 - x0 - 2 * b), y = math.floor(y1 - y0 - 2 * b), window = target }))
    hl.dispatch(hl.dsp.window.move({ x = math.floor(x0 + b), y = math.floor(y0 + b), window = target }))
end

-- KWin's combination rules (window.cpp, combineQuickTileMode):
--   not snapped + arrow        -> that half
--   left half + Up             -> top-left quarter        (and so on)
--   top-left quarter + Right   -> top half                (opposite side widens a quarter)
--   left half + Right          -> right half
--   left half + Left           -> next monitor to the left, as its right half
local OPP = { L = "R", R = "L", T = "B", B = "T" }

local function combine(st, dir)
    local h, v = st and st.h or "F", st and st.v or "F"
    local horizontal = (dir == "L" or dir == "R")
    local cur, other = horizontal and h or v, horizontal and v or h
    if cur == dir then return nil end                      -- same side again: next monitor
    local new
    if cur == OPP[dir] and other ~= "F" then new = "F"     -- quarter + opposite -> half
    else new = dir end                                     -- half + opposite, or fresh -> this side
    if horizontal then return new, v else return h, new end
end

-- The nearest monitor on one side of this one, or nil. Asking Hyprland to move a window to a
-- monitor that does not exist fails with "Invalid monitor", shown as an error notification.
local function neighbour(mon, dir)
    if not mon then return nil end
    local function box(m)
        local s = (m.scale and m.scale > 0) and m.scale or 1
        local w, h = m.width / s, m.height / s
        if (m.transform or 0) % 2 == 1 then w, h = h, w end
        return m.x, m.y, w, h
    end
    local mx, my, mw, mh = box(mon)
    local best, dist
    for _, m in ipairs(hl.get_monitors() or {}) do
        if m.name ~= mon.name and not m.is_mirror then
            local x, y, w, h = box(m)
            local d
            if dir == "L" and x + w <= mx then d = mx - (x + w)
            elseif dir == "R" and x >= mx + mw then d = x - (mx + mw)
            elseif dir == "T" and y + h <= my then d = my - (y + h)
            elseif dir == "B" and y >= my + mh then d = y - (my + mh) end
            if d and (not dist or d < dist) then best, dist = m, d end
        end
    end
    return best
end

local function snap(dir)
    local win = hl.get_active_window()
    if not win then return end
    local target = "address:" .. win.address
    if not win.floating then
        hl.dispatch(hl.dsp.window.float({ action = "on", window = target }))   -- "set" would toggle
        win = hl.get_window(target) or win
    end
    local st = state[win.address]
    if (win.fullscreen or 0) ~= 0 then                    -- move/resize refuse maximised windows
        hl.dispatch(hl.dsp.window.fullscreen_state({ internal = 0, client = -1, window = target }))
        win = hl.get_window(target) or win
        if dir == "B" then                                -- Win + Down on a maximised window:
            if st and st.h then place(win, st.h, st.v) end -- back to its half (D-30)
            return
        end
    end
    if not st then
        st = { saved = { x = win.at.x, y = win.at.y, w = win.size.x, h = win.size.y } }
        state[win.address] = st
    end
    if dir == "T" and st.v == "T" then                     -- Win + Up at the top: maximise (D-30).
        hl.dispatch(hl.dsp.window.fullscreen({ mode = "maximized", action = "toggle", window = target }))
        return                                             -- The monitors sit side by side, so
    end                                                    -- Up never needs to hop a monitor.
    local h, v = combine(st.h and st or nil, dir)
    if not h then                                          -- same direction twice: hop monitor
        local next_mon = neighbour(win.monitor, dir)
        if not next_mon then return end                    -- none on that side: do nothing, quietly
        hl.dispatch(hl.dsp.window.move({ monitor = next_mon.name, window = target }))
        win = hl.get_window(target) or win
        h, v = st.h, st.v
        if dir == "L" or dir == "R" then h = OPP[dir] else v = OPP[dir] end
    end
    st.h, st.v = h, v
    place(win, h, v)
end

local function restore()
    local win = hl.get_active_window()
    if not win then return end
    local st = state[win.address]
    if not st then return end
    local target = "address:" .. win.address
    if (win.fullscreen or 0) ~= 0 then
        hl.dispatch(hl.dsp.window.fullscreen_state({ internal = 0, client = -1, window = target }))
    end
    local s = st.saved
    hl.dispatch(hl.dsp.window.resize({ x = s.w, y = s.h, window = target }))
    hl.dispatch(hl.dsp.window.move({ x = s.x, y = s.y, window = target }))
    state[win.address] = nil
end

-- 4. Keys. Unbind first, in case an earlier config (like Omarchy's) uses them. -------
for _, k in ipairs({ "SUPER + LEFT", "SUPER + RIGHT", "SUPER + UP", "SUPER + DOWN",
                     "SUPER + Page_Up", "SUPER + BACKSPACE", "SUPER + T", "ALT + F4",
                     "ALT + TAB", "ALT + SHIFT + TAB", "SUPER + RETURN" }) do
    pcall(hl.unbind, k)
end

hl.bind("SUPER + LEFT",  function() snap("L") end, { description = "Snap window left" })
hl.bind("SUPER + RIGHT", function() snap("R") end, { description = "Snap window right" })
hl.bind("SUPER + UP",    function() snap("T") end, { description = "Snap window to the top" })
hl.bind("SUPER + DOWN",  function() snap("B") end, { description = "Snap window to the bottom" })
hl.bind("SUPER + Page_Up", hl.dsp.window.fullscreen({ mode = "maximized", action = "toggle" }),
        { description = "Maximise / restore" })
hl.bind("SUPER + BACKSPACE", restore, { description = "Restore size before snapping" })
hl.bind("SUPER + T", hl.dsp.window.float({ action = "toggle" }),
        { description = "Floating / tiled" })

hl.bind("ALT + F4", hl.dsp.window.close(), { description = "Close window" })

-- Win + Return: the terminal, Alacritty (D-29).
hl.bind("SUPER + RETURN", hl.dsp.exec_cmd("alacritty"), { description = "Terminal" })

-- Alt + Tab: jump to the next window and bring it to the front; Shift goes back (D-35).
-- Simple on purpose: no window list. (Same two keys Omarchy uses, with thanks.)
hl.bind("ALT + TAB", function()
    hl.dispatch(hl.dsp.window.cycle_next())
    hl.dispatch(hl.dsp.window.bring_to_top())
end, { description = "Next window" })
hl.bind("ALT + SHIFT + TAB", function()
    hl.dispatch(hl.dsp.window.cycle_next({ next = false }))
    hl.dispatch(hl.dsp.window.bring_to_top())
end, { description = "Previous window" })

hl.on("window.close", function(w) if w and w.address then state[w.address] = nil end end)

-- 5. New windows open floating, not maximised (D-32). ---------------------------------
-- Apps like Chromium remember "maximised" and ask for it again right after opening. We undo
-- that only in a window's first moments, so its maximise button keeps working afterwards.
-- It then opens like any window: 80 % of the screen, centred.
local fresh = {}

local function unmaximise_new(win)
    if not win or (win.fullscreen or 0) ~= 1 then return end
    local target = "address:" .. win.address
    hl.dispatch(hl.dsp.window.fullscreen_state({ internal = 0, client = 0, window = target }))
    win = hl.get_window(target)
    if not win or not win.monitor then return end
    local a = work_area(win.monitor)
    local w, h = math.floor(a.w * 0.8), math.floor(a.h * 0.8)
    hl.dispatch(hl.dsp.window.resize({ x = w, y = h, window = target }))
    hl.dispatch(hl.dsp.window.move({ x = math.floor(a.x + (a.w - w) / 2), y = math.floor(a.y + (a.h - h) / 2), window = target }))
end

hl.on("window.open", function(w)
    if not w or not w.address then return end
    local addr = w.address
    fresh[addr] = true
    unmaximise_new(w)
    hl.timer(function() fresh[addr] = nil end, { timeout = 1500, type = "oneshot" })
end)

hl.on("window.fullscreen", function(w)
    w = w or hl.get_active_window()
    if w and w.address and fresh[w.address] then unmaximise_new(hl.get_window("address:" .. w.address)) end
end)

-- Test handle: lets `hyprctl repl` drive the same functions the keys use.
M.snap, M.restore = snap, restore
_G.hypeforge_snap = M

return M
