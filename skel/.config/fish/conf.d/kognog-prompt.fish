# KognogOS prompt identity.
#
# Tide chooses its OS icon in _tide_detect_os, which reads ID=kognogos,
# does not recognise it, and falls through to ID_LIKE=arch -- so the
# prompt wears the Arch logo. That icon is not an image: Nerd Fonts
# patches ~3,600 glyphs into the private-use area of JetBrainsMono, and
# the Arch logo is just the character U+F303.
#
# Until ttf-kognogos-symbols ships the real emblem as its own glyph, this
# stands in with md-chevron_triple_up -- three stacked chevrons, the
# emblem's silhouette, in white.
#
# GLOBAL rather than universal on purpose: tide keeps its own values as
# universal variables and `tide configure` rewrites them. A global shadows
# a universal for the session, so this survives a reconfigure instead of
# being silently reverted.
set -g tide_os_icon 󰶼
set -g tide_os_color FFFFFF
set -g tide_os_bg_color 303030
