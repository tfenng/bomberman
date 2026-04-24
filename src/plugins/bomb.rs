use std::collections::HashSet;

use bevy::prelude::*;

use crate::plugins::{
    app::AppState,
    assets::{sprite_with_size, SpriteAssets},
    config::GameBalanceConfig,
    enemy::{Enemy, EnemyCount},
    game_state::{GameState, LevelResetRequest},
    map::{tile_to_transform_z, BOMB_Z, FLAME_Z, GridPosition, StageMap, TILE_SIZE},
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
            )
            .add_systems(Update, check_exit.run_if(in_state(AppState::InGame)));
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
    assets: Res<SpriteAssets>,
    config: Res<GameBalanceConfig>,
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
            timer: Timer::from_seconds(config.bomb_fuse_seconds, TimerMode::Once),
            flame_length: player.flame_length,
        },
        GridPosition(player_tile.0),
        tile_to_transform_z(player_tile.0, BOMB_Z),
        sprite_with_size(assets.bomb_texture(), TILE_SIZE - 4.0),
        Name::new("Bomb"),
    ));
}

fn tick_bombs(
    mut commands: Commands,
    assets: Res<SpriteAssets>,
    time: Res<Time>,
    config: Res<GameBalanceConfig>,
    mut map: ResMut<StageMap>,
    mut bombs: Query<(Entity, &mut Bomb, &GridPosition)>,
    soft_walls: Query<(Entity, &GridPosition), With<crate::plugins::map::TileKind>>,
) {
    // Collect all bomb data first to avoid borrow conflicts
    let bomb_data: Vec<(Entity, IVec2, u8)> = bombs
        .iter()
        .map(|(e, b, p)| (e, p.0, b.flame_length))
        .collect();

    // Collect soft wall entities
    let soft_wall_data: Vec<(Entity, IVec2)> = soft_walls.iter().map(|(e, p)| (e, p.0)).collect();

    // Collect bombs that finished their fuse
    let mut exploding = Vec::new();
    for (entity, mut bomb, pos) in &mut bombs {
        bomb.timer.tick(time.delta());
        if bomb.timer.is_finished() {
            exploding.push((entity, pos.0, bomb.flame_length));
        }
    }

    // Track which tiles have already exploded this tick
    let mut exploded_tiles: HashSet<IVec2> = HashSet::new();
    let mut processed_bombs: HashSet<Entity> = HashSet::new();
    let mut chain_queue: Vec<IVec2> = Vec::new();

    // Process each exploding bomb
    for (entity, center, flame_len) in exploding {
        process_explosion(
            &mut commands,
            &assets,
            &config,
            &mut map,
            &bomb_data,
            &soft_wall_data,
            center,
            flame_len,
            &mut exploded_tiles,
            &mut processed_bombs,
            &mut chain_queue,
        );
        processed_bombs.insert(entity);
        commands.entity(entity).despawn();
    }

    // Process chain explosions
    while let Some(target_tile) = chain_queue.pop() {
        if exploded_tiles.contains(&target_tile) {
            continue;
        }

        // Find bomb at this tile
        if let Some(&(entity, pos, flame_len)) =
            bomb_data.iter().find(|(_, p, _)| *p == target_tile)
        {
            if processed_bombs.contains(&entity) {
                continue;
            }

            process_explosion(
                &mut commands,
                &assets,
                &config,
                &mut map,
                &bomb_data,
                &soft_wall_data,
                pos,
                flame_len,
                &mut exploded_tiles,
                &mut processed_bombs,
                &mut chain_queue,
            );
            processed_bombs.insert(entity);
            commands.entity(entity).despawn();
        }
    }
}

fn process_explosion(
    commands: &mut Commands,
    assets: &SpriteAssets,
    config: &GameBalanceConfig,
    map: &mut StageMap,
    bomb_data: &[(Entity, IVec2, u8)],
    soft_wall_data: &[(Entity, IVec2)],
    center: IVec2,
    flame_length: u8,
    exploded_tiles: &mut HashSet<IVec2>,
    processed_bombs: &mut HashSet<Entity>,
    chain_queue: &mut Vec<IVec2>,
) {
    let directions = [IVec2::X, IVec2::NEG_X, IVec2::Y, IVec2::NEG_Y];

    // Spawn center flame
    spawn_flame(commands, assets, config, center);
    exploded_tiles.insert(center);

    for dir in directions {
        for step in 1..=flame_length {
            let tile = center + dir * step as i32;

            // Stop at hard wall
            if map.hard_walls.contains(&tile) {
                break;
            }

            // Spawn flame at this tile
            spawn_flame(commands, assets, config, tile);

            // Check for already exploded tile
            if exploded_tiles.contains(&tile) {
                break;
            }
            exploded_tiles.insert(tile);

            // Check for soft wall - destroy and stop
            if map.soft_walls.remove(&tile) {
                // Despawn the soft wall entity
                if let Some(&(entity, _)) = soft_wall_data.iter().find(|(_, p)| *p == tile) {
                    commands.entity(entity).despawn();
                }
                break;
            }

            // Check for bomb - queue for chain explosion
            if let Some(&(entity, _, _)) = bomb_data.iter().find(|(_, p, _)| *p == tile) {
                if !processed_bombs.contains(&entity) {
                    chain_queue.push(tile);
                }
                break;
            }
        }
    }
}

fn spawn_flame(
    commands: &mut Commands,
    assets: &SpriteAssets,
    config: &GameBalanceConfig,
    tile: IVec2,
) {
    commands.spawn((
        Flame {
            timer: Timer::from_seconds(config.flame_duration_seconds, TimerMode::Once),
        },
        GridPosition(tile),
        tile_to_transform_z(tile, FLAME_Z),
        sprite_with_size(assets.flame_texture(), TILE_SIZE - 4.0),
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
    mut level_reset_request: ResMut<LevelResetRequest>,
    mut players: Query<(&GridPosition, &mut Player)>,
    flames: Query<&GridPosition, With<Flame>>,
    mut game_state: ResMut<GameState>,
    mut enemy_count: ResMut<EnemyCount>,
    mut commands: Commands,
    enemies: Query<(Entity, &GridPosition), With<Enemy>>,
) {
    let Ok((player_grid_pos, mut player)) = players.single_mut() else {
        return;
    };

    // Check if player is on flame
    if flames.iter().any(|flame| flame.0 == player_grid_pos.0) {
        info!("Player died in explosion");
        game_state.lives -= 1;
        player.lives = game_state.lives;

        if game_state.lives == 0 {
            info!("Game Over - no lives left");
            level_reset_request.pending = false;
            next_state.set(AppState::GameOver);
        } else {
            info!("Respawning level, {} lives remaining", game_state.lives);
            level_reset_request.pending = true;
        }
    }

    let mut enemy_entities_to_remove = Vec::new();
    for (entity, enemy_tile) in &enemies {
        if flames.iter().any(|flame| flame.0 == enemy_tile.0) {
            enemy_entities_to_remove.push(entity);
        }
    }

    for entity in enemy_entities_to_remove {
        commands.entity(entity).despawn();
        enemy_count.count = enemy_count.count.saturating_sub(1);
    }
}

fn check_exit(
    mut next_state: ResMut<NextState<AppState>>,
    mut game_state: ResMut<GameState>,
    mut level_reset_request: ResMut<LevelResetRequest>,
    players: Query<&GridPosition, With<Player>>,
    enemy_count: Res<EnemyCount>,
    map: Res<StageMap>,
) {
    let Ok(player_pos) = players.single() else {
        return;
    };

    if player_pos.0 == map.exit_tile {
        if enemy_count.count > 0 {
            info!("Cannot exit - {} enemies remaining!", enemy_count.count);
            return;
        }

        info!("Level {} complete!", game_state.current_level);
        game_state.current_level += 1;

        if game_state.current_level > game_state.total_levels {
            info!("All levels complete - Victory!");
            level_reset_request.pending = false;
            next_state.set(AppState::Victory);
        } else {
            info!("Advancing to level {}", game_state.current_level);
            level_reset_request.pending = true;
        }
    }
}
