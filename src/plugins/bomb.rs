use std::collections::HashSet;

use bevy::prelude::*;

use crate::plugins::{
    app::AppState,
    map::{tile_to_transform, GridPosition, StageMap},
    player::Player,
};

pub struct BombPlugin;

impl Plugin for BombPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, place_bomb.run_if(in_state(AppState::InGame)))
            .add_systems(Update, tick_bombs.run_if(in_state(AppState::InGame)))
            .add_systems(Update, tick_flames.run_if(in_state(AppState::InGame)))
            .add_systems(
                Update,
                apply_flame_damage.run_if(in_state(AppState::InGame)),
            );
    }
}

#[derive(Component, Debug, Clone)]
pub struct Bomb {
    pub timer: Timer,
    pub flame_length: u8,
}

#[derive(Component, Debug, Clone)]
pub struct Flame {
    pub timer: Timer,
}

fn place_bomb(
    mut commands: Commands,
    keyboard: Res<ButtonInput<KeyCode>>,
    players: Query<(&GridPosition, &Player)>,
    bombs: Query<&GridPosition, With<Bomb>>,
) {
    if !keyboard.just_pressed(KeyCode::Space) {
        return;
    }

    let Ok((player_tile, player)) = players.single() else {
        return;
    };

    let active_bombs = bombs.iter().count() as u8;
    if active_bombs >= player.bomb_capacity {
        return;
    }

    if bombs.iter().any(|pos| pos.0 == player_tile.0) {
        return;
    }

    commands.spawn((
        Bomb {
            timer: Timer::from_seconds(2.25, TimerMode::Once),
            flame_length: player.flame_length,
        },
        GridPosition(player_tile.0),
        tile_to_transform(player_tile.0),
        Name::new("Bomb"),
    ));
}

fn tick_bombs(
    mut commands: Commands,
    time: Res<Time>,
    mut map: ResMut<StageMap>,
    mut bombs: Query<(Entity, &mut Bomb, &GridPosition)>,
) {
    let bomb_tiles: HashSet<IVec2> = bombs.iter().map(|(_, _, p)| p.0).collect();
    let mut to_explode = Vec::new();

    for (entity, mut bomb, pos) in &mut bombs {
        bomb.timer.tick(time.delta());
        if bomb.timer.is_finished() {
            to_explode.push((entity, pos.0, bomb.flame_length));
        }
    }

    for (entity, center, flame_length) in to_explode {
        explode_bomb(
            &mut commands,
            &mut map,
            center,
            flame_length,
            &bomb_tiles,
            &mut bombs,
        );
        commands.entity(entity).despawn();
    }
}

fn explode_bomb(
    commands: &mut Commands,
    map: &mut StageMap,
    center: IVec2,
    flame_length: u8,
    bomb_tiles: &HashSet<IVec2>,
    bombs: &mut Query<(Entity, &mut Bomb, &GridPosition)>,
) {
    spawn_flame(commands, center);

    let directions = [IVec2::X, IVec2::NEG_X, IVec2::Y, IVec2::NEG_Y];
    for dir in directions {
        for step in 1..=flame_length {
            let tile = center + dir * step as i32;

            if map.hard_walls.contains(&tile) {
                break;
            }

            spawn_flame(commands, tile);

            if map.soft_walls.remove(&tile) {
                break;
            }

            if bomb_tiles.contains(&tile) {
                for (_, mut bomb, pos) in bombs.iter_mut() {
                    if pos.0 == tile {
                        bomb.timer.set_elapsed(bomb.timer.duration());
                    }
                }
                break;
            }
        }
    }
}

fn spawn_flame(commands: &mut Commands, tile: IVec2) {
    commands.spawn((
        Flame {
            timer: Timer::from_seconds(0.45, TimerMode::Once),
        },
        GridPosition(tile),
        tile_to_transform(tile),
        Name::new("Flame"),
    ));
}

fn tick_flames(mut commands: Commands, time: Res<Time>, mut flames: Query<(Entity, &mut Flame)>) {
    for (entity, mut flame) in &mut flames {
        flame.timer.tick(time.delta());
        if flame.timer.is_finished() {
            commands.entity(entity).despawn();
        }
    }
}

fn apply_flame_damage(
    mut next_state: ResMut<NextState<AppState>>,
    players: Query<&GridPosition, With<Player>>,
    flames: Query<&GridPosition, With<Flame>>,
) {
    let Ok(player_pos) = players.single() else {
        return;
    };

    if flames.iter().any(|flame| flame.0 == player_pos.0) {
        info!("Player died in explosion");
        next_state.set(AppState::MainMenu);
    }
}
