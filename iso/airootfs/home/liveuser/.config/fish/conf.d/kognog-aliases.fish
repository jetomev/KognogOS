# KognogOS shell aliases.
#
# eza replaces ls. Fish aliases apply to INTERACTIVE use only, so scripts and
# anything non-interactive still get the real ls. `command ls` reaches it
# explicitly at any time.
#
# --icons=auto renders icons only when output is a terminal, so piping stays
# clean. The glyphs come from the terminal's Nerd Font, not from the server.

alias ls 'eza --group-directories-first --icons=auto'
alias ll 'eza --long --header --git --group-directories-first --icons=auto'
alias la 'eza --long --header --git --all --group-directories-first --icons=auto'
alias lt 'eza --tree --level=2 --group-directories-first --icons=auto'
