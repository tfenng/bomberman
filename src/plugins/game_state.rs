use bevy::prelude::*;

use crate::plugins::app::AppState;

#[derive(Resource, Debug, Clone)]
pub struct GameState {
    pub current_level: u32,
    pub total_levels: u32,
    pub lives: u8,
    pub score: u32,
}

impl Default for GameState {
    fn default() -> Self {
        Self {
            current_level: 1,
            total_levels: 4, // First 4 levels for MVP
            lives: 3,
            score: 0,
        }
    }
}

pub struct GameStatePlugin;

impl Plugin for GameStatePlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<GameState>()
            .add_systems(OnEnter(AppState::MainMenu), reset_game_state)
            .add_systems(OnEnter(AppState::InGame), start_level)
            .add_systems(OnExit(AppState::InGame), cleanup_level_entities);
    }
}

fn reset_game_state(mut game_state: ResMut<GameState>) {
    *game_state = GameState::default();
}

fn start_level(
    game_state: Res<GameState>,
    mut next_state: ResMut<NextState<AppState>>,
) {
    info!("Starting Level {}", game_state.current_level);

    // Check if this is the last level
    if game_state.current_level > game_state.total_levels {
        info!("All levels complete - Victory!");
        next_state.set(AppState::Victory);
    }
    // Otherwise, level will be set up by map system
}

fn cleanup_level_entities(
    mut commands: Commands,
    players: Query<Entity, With<crate::plugins::player::Player>>,
    bombs: Query<Entity, With<crate::plugins::bomb::Bomb>>,
    flames: Query<Entity, With<crate::plugins::bomb::Flame>>,
) {
    // Despawn all players
    for entity in &players {
        commands.entity(entity).despawn();
    }
    // Despawn all bombs
    for entity in &bombs {
        commands.entity(entity).despawn();
    }
    // Despawn all flames
    for entity in &flames {
        commands.entity(entity).despawn();
    }
}
