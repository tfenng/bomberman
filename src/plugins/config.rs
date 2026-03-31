use std::fs;

use bevy::prelude::*;
use serde::Deserialize;

pub struct ConfigPlugin;

impl Plugin for ConfigPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(GameBalanceConfig::default())
            .add_systems(Startup, load_balance_config);
    }
}

#[derive(Resource, Debug, Clone, Deserialize)]
pub struct GameBalanceConfig {
    pub main_stage_timer_seconds: u32,
    pub bomb_fuse_seconds: f32,
    pub flame_duration_seconds: f32,
    pub punisher_spawn_count: u8,
}

impl Default for GameBalanceConfig {
    fn default() -> Self {
        Self {
            main_stage_timer_seconds: 300,
            bomb_fuse_seconds: 2.25,
            flame_duration_seconds: 0.45,
            punisher_spawn_count: 2,
        }
    }
}

fn load_balance_config(mut config: ResMut<GameBalanceConfig>) {
    let path = "assets/config/gameplay.json";

    let parsed = fs::read_to_string(path)
        .ok()
        .and_then(|content| serde_json::from_str::<GameBalanceConfig>(&content).ok());

    if let Some(value) = parsed {
        *config = value;
        info!("Loaded gameplay config from {path}");
    } else {
        warn!("Using default gameplay config. Missing or invalid: {path}");
    }
}
