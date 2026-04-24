use std::collections::HashSet;

use bevy::prelude::*;

use crate::plugins::{
    app::AppState,
    assets::{sprite_with_size, SpriteAssets},
    bomb::Bomb,
    map::{is_blocked, tile_to_transform_z, ACTOR_Z, GridPosition, StageMap, TILE_SIZE},
};

pub struct PlayerPlugin;

impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_player)
            .add_systems(OnEnter(AppState::InGame), ensure_player_exists)
            .add_systems(
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

fn spawn_player(mut commands: Commands, map: Res<StageMap>, assets: Res<SpriteAssets>) {
    spawn_player_entity(&mut commands, &map, &assets);
}

pub fn spawn_player_entity(commands: &mut Commands, map: &StageMap, assets: &SpriteAssets) {
    commands.spawn((
        Player {
            bomb_capacity: 1,
            flame_length: 1,
            lives: 3,
        },
        GridPosition(map.player_spawn),
        tile_to_transform_z(map.player_spawn, ACTOR_Z),
        sprite_with_size(assets.player_texture(), TILE_SIZE * 0.75),
        Name::new("Player"),
    ));
}

fn ensure_player_exists(
    mut commands: Commands,
    map: Res<StageMap>,
    assets: Res<SpriteAssets>,
    players: Query<(), With<Player>>,
) {
    if players.is_empty() {
        spawn_player_entity(&mut commands, &map, &assets);
    }
}

fn handle_player_movement(
    keyboard: Res<ButtonInput<KeyCode>>,
    map: Res<StageMap>,
    mut queries: ParamSet<(
        Query<(Entity, &mut GridPosition, &mut Transform), With<Player>>,
        Query<&GridPosition, With<Bomb>>,
    )>,
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

    let bomb_tiles: HashSet<IVec2> = queries.p1().iter().map(|p| p.0).collect();

    if let Ok((_, mut pos, mut transform)) = queries.p0().single_mut() {
        let target = pos.0 + direction;
        if !is_blocked(target, &map, &bomb_tiles) {
            pos.0 = target;
            *transform = tile_to_transform_z(target, ACTOR_Z);
        }
    }
}
