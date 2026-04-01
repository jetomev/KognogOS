use std::process::{Command, ExitStatus, Output};

pub fn run(args: &[&str]) -> ExitStatus {
    Command::new("pacman")
        .args(args)
        .status()
        .unwrap_or_else(|e| panic!("nog: failed to launch pacman: {}", e))
}

pub fn install(packages: &[String]) -> ExitStatus {
    let pkgs: Vec<&str> = packages.iter().map(|s| s.as_str()).collect();
    let mut args = vec!["-S", "--noconfirm"];
    args.extend_from_slice(&pkgs);
    run(&args)
}

pub fn remove(packages: &[String]) -> ExitStatus {
    let pkgs: Vec<&str> = packages.iter().map(|s| s.as_str()).collect();
    let mut args = vec!["-Rs", "--noconfirm"];
    args.extend_from_slice(&pkgs);
    run(&args)
}

pub fn update() -> ExitStatus {
    run(&["-Syu"])
}

pub fn search(query: &str) -> ExitStatus {
    run(&["-Ss", query])
}

pub fn search_capture(query: &str) -> Output {
    Command::new("pacman")
        .args(["-Ss", query])
        .output()
        .unwrap_or_else(|e| panic!("nog: failed to launch pacman: {}", e))
}