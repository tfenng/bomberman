use bevy::prelude::*;

use crate::plugins::{
    assets::SpriteAssetsPlugin, bomb::BombPlugin, config::ConfigPlugin, core::CorePlugin,
    enemy::EnemyPlugin, game_state::GameStatePlugin, map::MapPlugin, player::PlayerPlugin,
    ui::UiPlugin,
};
use crate::plugins::map::{MAP_HEIGHT, MAP_WIDTH, TILE_SIZE};

pub struct AppPlugin;

impl Plugin for AppPlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins(
            DefaultPlugins
                .set(ImagePlugin::default_nearest())
                .set(WindowPlugin {
                    primary_window: Some(Window {
                        title: "Blast Maze".to_string(),
                        resolution: (
                            (MAP_WIDTH as f32 * TILE_SIZE) as u32,
                            (MAP_HEIGHT as f32 * TILE_SIZE) as u32,
                        )
                            .into(),
                        resizable: true,
                        ..default()
                    }),
                    ..default()
                }),
        )
        .init_state::<AppState>()
        .add_plugins((
            CorePlugin,
            ConfigPlugin,
            SpriteAssetsPlugin,
            EnemyPlugin,
            MapPlugin,
            PlayerPlugin,
            BombPlugin,
            GameStatePlugin,
            UiPlugin,
        ));
    }
}

#[derive(States, Debug, Clone, Eq, PartialEq, Hash, Default)]
pub enum AppState {
    MainMenu,
    #[default]
    InGame,
    Paused,
    GameOver,
    Victory,
}
