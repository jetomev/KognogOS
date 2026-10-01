-- hypeForge prototype: title bars with maximise and close (D-33, D-34: no minimise).
-- Drawn by hyprbars, the Hyprland team's title-bar plugin (github.com/hyprwm/hyprland-plugins),
-- for windows that do not draw their own, such as Alacritty and other terminals.
-- Needs the plugin loaded (hyprpm enable hyprbars && hyprpm reload). Colours come from the
-- chosen theme (hypeforge-theme.lua, D-36), with Catppuccin Mocha as the fallback.

local T = (HYPEFORGE_THEME and HYPEFORGE_THEME.c) or {
    titlebar = "#181825", text = "#cdd6f4", red = "#f38ba8", green = "#a6e3a1", btnIcon = "#1e1e2e",
}
local function rgba(hex, alpha) return "rgba(" .. hex:sub(2) .. (alpha or "ff") .. ")" end
local colours = {
    bar = rgba(T.titlebar, "ee"), text = rgba(T.text),
    red = rgba(T.red), green = rgba(T.green), icon = rgba(T.btnIcon),
}

-- Runs Lua inside Hyprland from a button click (buttons run a shell command).
local function lua_cmd(code) return "hyprctl eval '" .. code .. "'" end

local MAXIMISE = lua_cmd('hl.dispatch(hl.dsp.window.fullscreen({ mode = "maximized", action = "toggle" }))')

hl.config({
    plugin = {
        hyprbars = {
            bar_height = 26,
            bar_color = colours.bar,
            ["col.text"] = colours.text,
            bar_text_font = "JetBrainsMono Nerd Font",
            bar_text_size = 12,
            bar_text_align = "left",
            bar_padding = 10,
            bar_button_padding = 8,
            bar_buttons_alignment = "right",
            on_double_click = MAXIMISE,
        },
    },
})

-- Buttons are listed right to left: close, maximise.
local hb = hl.plugin and hl.plugin.hyprbars
if hb and hb.add_button then
    hb.add_button({ bg_color = colours.red, fg_color = colours.icon, size = 14, icon = "󰖭",
                    action = lua_cmd("hl.dispatch(hl.dsp.window.close())") })
    hb.add_button({ bg_color = colours.green, fg_color = colours.icon, size = 14, icon = "󰖯",
                    action = MAXIMISE })
end

-- Apps that draw their own title bar keep theirs, so they do not get two.
hl.window_rule({
    name = "hypeforge-own-titlebar",
    match = { class = "^(chromium|google-chrome|brave-browser|org\\.gnome\\..*)$" },
    ["hyprbars:no_bar"] = true,
})
