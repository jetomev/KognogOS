use serde::Deserialize;
use std::fs;

#[derive(Debug, Deserialize)]
struct TierConfig {
    hold_days: u32,
    manual_signoff: bool,
    packages: Option<Vec<String>>,
}

#[derive(Debug, Deserialize)]
struct TierPins {
    tier1: TierConfig,
    tier2: TierConfig,
    tier3: TierConfig,
}

#[derive(Debug, PartialEq, Clone)]
pub enum Tier {
    One,
    Two,
    Three,
}

impl std::fmt::Display for Tier {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            Tier::One   => write!(f, "Tier 1 (manual sign-off required)"),
            Tier::Two   => write!(f, "Tier 2 (10-day hold)"),
            Tier::Three => write!(f, "Tier 3 (fast-track)"),
        }
    }
}

pub struct TierManager {
    pins: TierPins,
}

impl TierManager {
    pub fn load(path: &str) -> Result<Self, String> {
        let contents = fs::read_to_string(path)
            .map_err(|e| format!("Could not read {}: {}", path, e))?;
        let pins: TierPins = toml::from_str(&contents)
            .map_err(|e| format!("Could not parse tier-pins.toml: {}", e))?;
        Ok(TierManager { pins })
    }

    pub fn classify(&self, package: &str) -> Tier {
        if let Some(pkgs) = &self.pins.tier1.packages {
            if pkgs.iter().any(|p| p == package) {
                return Tier::One;
            }
        }
        if let Some(pkgs) = &self.pins.tier2.packages {
            if pkgs.iter().any(|p| p == package) {
                return Tier::Two;
            }
        }
        Tier::Three
    }

    pub fn is_manual_signoff(&self, package: &str) -> bool {
        self.classify(package) == Tier::One && self.pins.tier1.manual_signoff
    }

    pub fn hold_days(&self, package: &str) -> u32 {
        match self.classify(package) {
            Tier::One   => self.pins.tier1.hold_days,
            Tier::Two   => self.pins.tier2.hold_days,
            Tier::Three => self.pins.tier3.hold_days,
        }
    }

    pub fn tier1_packages(&self) -> Vec<String> {
        self.pins.tier1.packages.clone().unwrap_or_default()
    }
}