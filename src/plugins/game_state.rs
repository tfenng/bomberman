use std::collections::HashSet;

use bevy::prelude::*;
use rand::seq::SliceRandom;

use crate::plugins::{
    app::AppState,
    assets::SpriteAssets,
    bomb::{Bomb, Flame},
    config::GameBalanceConfig,
    enemy::{spawn_punisher, Enemy, EnemyCount},
    map::{spawn_stage_map, tile_to_transform_z, ACTOR_Z, GridPosition, StageMap, StageTile},
    player::Player,
};

pub struct GameStatePlugin;

const PUNISHER_SAFE_DISTANCE: i32 = 3;

impl Plugin for GameStatePlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<GameState>()
            .init_resource::<LevelTimer>()
            .init_resource::<LevelResetRequest>()
            .add_systems(Startup, initialize_level_timer)
            .add_systems(OnEnter(AppState::MainMenu), reset_game_state)
            .add_systems(OnEnter(AppState::MainMenu), cleanup_level_entities)
            .add_systems(OnEnter(AppState::GameOver), cleanup_level_entities)
            .add_systems(OnEnter(AppState::Victory), cleanup_level_entities)
            .add_systems(
                Update,
                (tick_level_timer, process_level_reset).run_if(in_state(AppState::InGame)),
            );
    }
}

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
            total_levels: 4,
            lives: 3,
            score: 0,
        }
    }
}

#[derive(Resource, Debug, Clone)]
pub struct LevelTimer {
    pub total_seconds: u32,
    pub remaining_seconds: f32,
    pub timeout_triggered: bool,
}

impl Default for LevelTimer {
    fn default() -> Self {
        Self {
            total_seconds: 300,
            remaining_seconds: 300.0,
            timeout_triggered: false,
        }
    }
}

impl LevelTimer {
    pub fn reset(&mut self, total_seconds: u32) {
        self.total_seconds = total_seconds;
        self.remaining_seconds = total_seconds as f32;
        self.timeout_triggered = false;
    }
}

#[derive(Resource, Debug, Default)]
pub struct LevelResetRequest {
    pub pending: bool,
}

fn initialize_level_timer(mut level_timer: ResMut<LevelTimer>, config: Res<GameBalanceConfig>) {
    level_timer.reset(config.main_stage_timer_seconds);
}

fn reset_game_state(
    mut game_state: ResMut<GameState>,
    mut level_timer: ResMut<LevelTimer>,
    mut level_reset_request: ResMut<LevelResetRequest>,
    mut map: ResMut<StageMap>,
    mut enemy_count: ResMut<EnemyCount>,
    config: Res<GameBalanceConfig>,
) {
    *game_state = GameState::default();
    level_timer.reset(config.main_stage_timer_seconds);
    level_reset_request.pending = false;
    enemy_count.count = 0;
    map.restore_layout();
}

fn cleanup_level_entities(
    mut commands: Commands,
    stage_tiles: Query<Entity, With<StageTile>>,
    players: Query<Entity, With<Player>>,
    bombs: Query<Entity, With<Bomb>>,
    flames: Query<Entity, With<Flame>>,
    enemies: Query<Entity, With<Enemy>>,
) {
    despawn_entities(&mut commands, stage_tiles.iter());
    despawn_entities(&mut commands, players.iter());
    despawn_entities(&mut commands, bombs.iter());
    despawn_entities(&mut commands, flames.iter());
    despawn_entities(&mut commands, enemies.iter());
}

fn despawn_entities(commands: &mut Commands, entities: impl IntoIterator<Item = Entity>) {
    for entity in entities {
        commands.entity(entity).despawn();
    }
}

fn tick_level_timer(
    time: Res<Time>,
    assets: Res<SpriteAssets>,
    config: Res<GameBalanceConfig>,
    map: Res<StageMap>,
    mut level_timer: ResMut<LevelTimer>,
    mut commands: Commands,
    mut enemy_count: ResMut<EnemyCount>,
    player: Query<&GridPosition, With<Player>>,
    bombs: Query<&GridPosition, With<Bomb>>,
    flames: Query<&GridPosition, With<Flame>>,
    enemies: Query<&GridPosition, With<Enemy>>,
) {
    if level_timer.timeout_triggered {
        return;
    }

    level_timer.remaining_seconds = (level_timer.remaining_seconds - time.delta_secs()).max(0.0);
    if level_timer.remaining_seconds > 0.0 {
        return;
    }

    level_timer.timeout_triggered = true;

    let Ok(player_tile) = player.single() else {
        return;
    };

    let occupied_tiles = collect_occupied_tiles(&bombs, &flames, &enemies, player_tile.0);
    spawn_timeout_punishers(
        &mut commands,
        &map,
        player_tile.0,
        &occupied_tiles,
        &assets,
        config.punisher_spawn_count,
        &mut *enemy_count,
    );
}

fn collect_occupied_tiles(
    bombs: &Query<&GridPosition, With<Bomb>>,
    flames: &Query<&GridPosition, With<Flame>>,
    enemies: &Query<&GridPosition, With<Enemy>>,
    player_tile: IVec2,
) -> HashSet<IVec2> {
    let mut occupied_tiles = HashSet::new();
    occupied_tiles.insert(player_tile);
    occupied_tiles.extend(bombs.iter().map(|grid| grid.0));
    occupied_tiles.extend(flames.iter().map(|grid| grid.0));
    occupied_tiles.extend(enemies.iter().map(|grid| grid.0));
    occupied_tiles
}

fn spawn_timeout_punishers(
    commands: &mut Commands,
    map: &StageMap,
    player_tile: IVec2,
    occupied_tiles: &HashSet<IVec2>,
    assets: &SpriteAssets,
    spawn_count: u8,
    enemy_count: &mut EnemyCount,
) {
    let mut safe_candidates = Vec::new();
    let mut fallback_candidates = Vec::new();

    for y in 1..map.height - 1 {
        for x in 1..map.width - 1 {
            let tile = IVec2::new(x, y);

            if tile == map.exit_tile
                || map.hard_walls.contains(&tile)
                || map.soft_walls.contains(&tile)
                || occupied_tiles.contains(&tile)
            {
                continue;
            }

            let distance = manhattan_distance(tile, player_tile);
            if distance >= PUNISHER_SAFE_DISTANCE {
                safe_candidates.push(tile);
            } else {
                fallback_candidates.push(tile);
            }
        }
    }

    let mut rng = rand::thread_rng();
    safe_candidates.shuffle(&mut rng);
    fallback_candidates.shuffle(&mut rng);

    for tile in safe_candidates
        .into_iter()
        .chain(fallback_candidates.into_iter())
        .take(spawn_count as usize)
    {
        spawn_punisher(commands, assets, tile);
        enemy_count.count += 1;
    }
}

fn manhattan_distance(a: IVec2, b: IVec2) -> i32 {
    (a.x - b.x).abs() + (a.y - b.y).abs()
}

fn process_level_reset(
    mut commands: Commands,
    mut level_reset_request: ResMut<LevelResetRequest>,
    mut level_timer: ResMut<LevelTimer>,
    assets: Res<SpriteAssets>,
    config: Res<GameBalanceConfig>,
    mut map: ResMut<StageMap>,
    mut enemy_count: ResMut<EnemyCount>,
    mut players: Query<(&mut GridPosition, &mut Transform), With<Player>>,
    stage_tiles: Query<Entity, With<StageTile>>,
    bombs: Query<Entity, With<Bomb>>,
    flames: Query<Entity, With<Flame>>,
    enemies: Query<Entity, With<Enemy>>,
) {
    if !level_reset_request.pending {
        return;
    }

    level_reset_request.pending = false;
    level_timer.reset(config.main_stage_timer_seconds);
    enemy_count.count = 0;
    map.restore_layout();

    despawn_entities(&mut commands, stage_tiles.iter());
    despawn_entities(&mut commands, bombs.iter());
    despawn_entities(&mut commands, flames.iter());
    despawn_entities(&mut commands, enemies.iter());

    spawn_stage_map(&mut commands, &map, &assets);

    if let Ok((mut player_tile, mut transform)) = players.single_mut() {
        player_tile.0 = map.player_spawn;
        *transform = tile_to_transform_z(map.player_spawn, ACTOR_Z);
    }
}
