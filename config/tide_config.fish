# KognogOS default tide prompt configuration
# Run once after installing fisher and tide to apply the default prompt style
# Usage: source ~/.config/fish/tide_config.fish

set -U tide_character_color 5FD700
set -U tide_character_color_failure FF0000
set -U tide_character_icon ❯
set -U tide_character_vi_icon_default ❮
set -U tide_character_vi_icon_replace ▶
set -U tide_character_vi_icon_visual V

set -U tide_left_prompt_frame_enabled false
set -U tide_left_prompt_items 'os' 'pwd' 'git' 'newline' 'character'
set -U tide_left_prompt_prefix
set -U tide_left_prompt_separator_diff_color 
set -U tide_left_prompt_separator_same_color 
set -U tide_left_prompt_suffix 

set -U tide_right_prompt_frame_enabled false
set -U tide_right_prompt_items 'status' 'cmd_duration' 'context' 'jobs' 'direnv' 'bun' 'node' 'python' 'rustc' 'java' 'php' 'ruby' 'go' 'gcloud' 'pulumi' 'kubectl' 'terraform' 'aws' 'nix_shell' 'crystal' 'toolbox' 'distrobox' 'shlvl' 'vi_mode' 'time'
set -U tide_right_prompt_prefix 
set -U tide_right_prompt_separator_diff_color 
set -U tide_right_prompt_separator_same_color 
set -U tide_right_prompt_suffix

set -U tide_prompt_add_newline_before true
set -U tide_prompt_color_frame_and_connection 6C6C6C
set -U tide_prompt_color_separator_same_color 949494
set -U tide_prompt_icon_connection ' '
set -U tide_prompt_min_cols 34
set -U tide_prompt_pad_items true
set -U tide_prompt_transient_enabled false

set -U tide_pwd_bg_color 303030
set -U tide_pwd_color_anchors 00AFFF
set -U tide_pwd_color_dirs 0087AF
set -U tide_pwd_color_truncated_dirs 8787AF
set -U tide_pwd_icon 
set -U tide_pwd_icon_home 
set -U tide_pwd_icon_unwritable 

set -U tide_git_bg_color 303030
set -U tide_git_bg_color_unstable 303030
set -U tide_git_bg_color_urgent 303030
set -U tide_git_color_branch 5FD700
set -U tide_git_color_conflicted FF0000
set -U tide_git_color_dirty D7AF00
set -U tide_git_color_operation FF0000
set -U tide_git_color_staged D7AF00
set -U tide_git_color_stash 5FD700
set -U tide_git_color_untracked 00AFFF
set -U tide_git_color_upstream 5FD700
set -U tide_git_icon 
set -U tide_git_truncation_length 24

set -U tide_os_bg_color 303030
set -U tide_os_color EEEEEE
set -U tide_os_icon 

set -U tide_time_bg_color 303030
set -U tide_time_color 5F8787
set -U tide_time_format '%r'

set -U tide_status_bg_color 303030
set -U tide_status_bg_color_failure 303030
set -U tide_status_color 5FAF00
set -U tide_status_color_failure D70000
set -U tide_status_icon ✔
set -U tide_status_icon_failure ✘

set -U tide_cmd_duration_bg_color 303030
set -U tide_cmd_duration_color 87875F
set -U tide_cmd_duration_decimals 0
set -U tide_cmd_duration_icon 
set -U tide_cmd_duration_threshold 3000

set -U tide_shlvl_bg_color 303030
set -U tide_shlvl_color d78700
set -U tide_shlvl_icon 
set -U tide_shlvl_threshold 1

set -U tide_vi_mode_bg_color_default 303030
set -U tide_vi_mode_bg_color_insert 303030
set -U tide_vi_mode_bg_color_replace 303030
set -U tide_vi_mode_bg_color_visual 303030
set -U tide_vi_mode_color_default 949494
set -U tide_vi_mode_color_insert 87AFAF
set -U tide_vi_mode_color_replace 87AF87
set -U tide_vi_mode_color_visual FF8700
set -U tide_vi_mode_icon_default D
set -U tide_vi_mode_icon_insert I
set -U tide_vi_mode_icon_replace R
set -U tide_vi_mode_icon_visual V

set -U tide_jobs_bg_color 303030
set -U tide_jobs_color 5FAF00
set -U tide_jobs_icon 
set -U tide_jobs_number_threshold 1000

set -U tide_context_always_display false
set -U tide_context_bg_color 303030
set -U tide_context_color_default D7AF87
set -U tide_context_color_root D7AF00
set -U tide_context_color_ssh D7AF87
set -U tide_context_hostname_parts 1

echo "KognogOS tide prompt configured successfully!"