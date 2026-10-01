-- hypeForge: the terminal's 16 colours for each theme (F-12). Chosen by Javier on
-- 2026-09-30 from the preview page (https://claude.ai/artifact/PmTan1DKRuBtxAxxanVamt):
-- "all the proposed terminal themes I like". Dark themes use Catppuccin Mocha's official
-- terminal colours; White uses Catppuccin Latte's with yellow, green, pink and cyan
-- darkened; Green has its own green-grey set. Every colour reads at 4.5:1 or better.
-- Order: black, red, green, yellow, blue, magenta, cyan, white.
local MOCHA = { "#f38ba8", "#a6e3a1", "#f9e2af", "#89b4fa", "#f5c2e7", "#94e2d5" }
local function set(bg, fg, black, white, bblack, bwhite, acc)
    return { bg = bg, fg = fg,
             normal = { black, acc[1], acc[2], acc[3], acc[4], acc[5], acc[6], white },
             bright = { bblack, acc[1], acc[2], acc[3], acc[4], acc[5], acc[6], bwhite } }
end
return {
    mocha = set("#1e1e2e", "#cdd6f4", "#45475a", "#bac2de", "#585b70", "#a6adc8", MOCHA),
    black = set("#0f0f0f", "#e4e4e4", "#3a3a3a", "#bdbdbd", "#6b6b6b", "#f2f2f2", MOCHA),
    gray  = set("#303030", "#ececec", "#1e1e1e", "#c8c8c8", "#8a8a8a", "#ffffff", MOCHA),
    green = set("#e2efe6", "#0e3321", "#1f4a33", "#9fbfad", "#3b6a4f", "#c8dccf",
                { "#b8142d", "#1d6e2a", "#7f5200", "#1552b8", "#8e2a7c", "#0d6f68" }),
    white = set("#ececec", "#1c1c1c", "#5c5f77", "#9ca0b0", "#6c6f85", "#bcc0cc",
                { "#d20f39", "#2f7d1f", "#a86a00", "#1e66f5", "#b3389f", "#147f86" }),
}
