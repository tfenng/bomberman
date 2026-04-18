use bevy::prelude::*;

use crate::plugins::{
    bomb::BombPlugin, config::ConfigPlugin, core::CorePlugin, map::MapPlugin, player::PlayerPlugin,
};

pub struct AppPlugin;

impl Plugin for AppPlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: "Blast Maze".to_string(),
                resolution: (1280, 720).into(),
                resizable: false,
                ..default()
            }),
            ..default()
        }))
        .init_state::<AppState>()
        .add_plugins((
            CorePlugin,
            ConfigPlugin,
            MapPlugin,
            PlayerPlugin,
            BombPlugin,
        ));
    }
}

#[derive(States, Debug, Clone, Eq, PartialEq, Hash, Default)]
pub enum AppState {
    #[default]
    MainMenu,
    InGame,
    Paused,
    GameOver,
    Victory,
}
