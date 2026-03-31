use std::collections::HashSet;

use bevy::prelude::*;

use crate::plugins::{
    app::AppState,
    bomb::Bomb,
    map::{is_blocked, tile_to_transform, GridPosition, StageMap},
};

pub struct PlayerPlugin;

impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_player).add_systems(
            Update,
            handle_player_movement.run_if(in_state(AppState::InGame)),
        );
    }
}

#[derive(Component, Debug, Clone)]
pub struct Player {
    pub bomb_capacity: u8,
    pub flame_length: u8,
    pub lives: u8,
}

fn spawn_player(mut commands: Commands, map: Res<StageMap>) {
    commands.spawn((
        Player {
            bomb_capacity: 1,
            flame_length: 1,
            lives: 3,
        },
        GridPosition(map.player_spawn),
        tile_to_transform(map.player_spawn),
        Name::new("Player"),
    ));
}

fn handle_player_movement(
    keyboard: Res<ButtonInput<KeyCode>>,
    map: Res<StageMap>,
    bombs: Query<&GridPosition, With<Bomb>>,
    mut player_query: Query<(&mut GridPosition, &mut Transform), With<Player>>,
) {
    let mut direction = IVec2::ZERO;
    if keyboard.just_pressed(KeyCode::ArrowUp) || keyboard.just_pressed(KeyCode::KeyW) {
        direction = IVec2::new(0, 1);
    } else if keyboard.just_pressed(KeyCode::ArrowDown) || keyboard.just_pressed(KeyCode::KeyS) {
        direction = IVec2::new(0, -1);
    } else if keyboard.just_pressed(KeyCode::ArrowLeft) || keyboard.just_pressed(KeyCode::KeyA) {
        direction = IVec2::new(-1, 0);
    } else if keyboard.just_pressed(KeyCode::ArrowRight) || keyboard.just_pressed(KeyCode::KeyD) {
        direction = IVec2::new(1, 0);
    }

    if direction == IVec2::ZERO {
        return;
    }

    let bomb_tiles: HashSet<IVec2> = bombs.iter().map(|p| p.0).collect();

    if let Ok((mut pos, mut transform)) = player_query.single_mut() {
        let target = pos.0 + direction;
        if !is_blocked(target, &map, &bomb_tiles) {
            pos.0 = target;
            *transform = tile_to_transform(target);
        }
    }
}
