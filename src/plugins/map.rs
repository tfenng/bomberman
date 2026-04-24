use std::collections::HashSet;

use bevy::prelude::*;

use crate::plugins::{
    app::AppState,
    assets::{sprite_with_size, SpriteAssets},
};

pub const MAP_WIDTH: i32 = 21;
pub const MAP_HEIGHT: i32 = 17;
pub const TILE_SIZE: f32 = 64.0;
pub const FLOOR_Z: f32 = 0.0;
pub const TILE_Z: f32 = 1.0;
pub const ACTOR_Z: f32 = 10.0;
pub const BOMB_Z: f32 = 15.0;
pub const FLAME_Z: f32 = 20.0;

pub struct MapPlugin;

impl Plugin for MapPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<StageMap>()
            .add_systems(Startup, setup_stage_map)
            .add_systems(OnEnter(AppState::InGame), ensure_stage_map_exists);
    }
}

#[derive(Resource, Debug, Clone)]
pub struct StageMap {
    pub width: i32,
    pub height: i32,
    pub hard_walls: HashSet<IVec2>,
    pub soft_walls: HashSet<IVec2>,
    pub initial_soft_walls: HashSet<IVec2>,
    pub exit_tile: IVec2,
    pub player_spawn: IVec2,
}

impl Default for StageMap {
    fn default() -> Self {
        let width = MAP_WIDTH;
        let height = MAP_HEIGHT;
        let mut hard_walls = HashSet::new();
        let mut soft_walls = HashSet::new();

        for y in 0..height {
            for x in 0..width {
                let pos = IVec2::new(x, y);

                let is_border = x == 0 || y == 0 || x == width - 1 || y == height - 1;
                let is_pillar = x % 2 == 0 && y % 2 == 0;

                if is_border || is_pillar {
                    hard_walls.insert(pos);
                }
            }
        }

        for y in 1..height - 1 {
            for x in 1..width - 1 {
                let pos = IVec2::new(x, y);
                if hard_walls.contains(&pos) {
                    continue;
                }

                // 保留出生区 2x2 安全区
                if x <= 2 && y <= 2 {
                    continue;
                }

                // 软墙分布 - 稀疏一些，约 1/3 概率
                if (x + y) % 5 != 0 {
                    soft_walls.insert(pos);
                }
            }
        }

        Self {
            width,
            height,
            hard_walls,
            initial_soft_walls: soft_walls.clone(),
            soft_walls,
            exit_tile: IVec2::new(width - 2, height - 2),
            player_spawn: IVec2::new(1, 1),
        }
    }
}

#[derive(Component, Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct GridPosition(pub IVec2);

#[derive(Component, Debug, Clone, Copy)]
pub struct StageTile;

#[derive(Component, Debug, Clone, Copy, PartialEq, Eq)]
pub enum TileKind {
    HardWall,
    SoftWall,
    Exit,
}

fn setup_stage_map(mut commands: Commands, map: Res<StageMap>, assets: Res<SpriteAssets>) {
    spawn_stage_map(&mut commands, &map, &assets);
}

fn ensure_stage_map_exists(
    mut commands: Commands,
    map: Res<StageMap>,
    assets: Res<SpriteAssets>,
    stage_tiles: Query<(), With<StageTile>>,
) {
    if stage_tiles.is_empty() {
        spawn_stage_map(&mut commands, &map, &assets);
    }
}

pub fn spawn_stage_map(commands: &mut Commands, map: &StageMap, assets: &SpriteAssets) {
    // Floor - dark background (0.15, 0.15, 0.2)
    for y in 0..map.height {
        for x in 0..map.width {
            let tile = IVec2::new(x, y);
            commands.spawn((
                StageTile,
                GridPosition(tile),
                tile_to_transform_z(tile, FLOOR_Z),
                Sprite {
                    color: Color::srgb(0.15, 0.15, 0.2),
                    custom_size: Some(Vec2::splat(TILE_SIZE - 1.0)),
                    ..default()
                },
                Name::new("Floor"),
            ));
        }
    }

    // Hard walls - dark gray (0.3, 0.3, 0.35)
    for tile in &map.hard_walls {
        commands.spawn((
            StageTile,
            GridPosition(*tile),
            TileKind::HardWall,
            tile_to_transform_z(*tile, TILE_Z),
            sprite_with_size(assets.tile_texture(TileKind::HardWall), TILE_SIZE - 2.0),
            Name::new("HardWall"),
        ));
    }

    // Soft walls - light tan (0.85, 0.75, 0.55)
    for tile in &map.soft_walls {
        commands.spawn((
            StageTile,
            GridPosition(*tile),
            TileKind::SoftWall,
            tile_to_transform_z(*tile, TILE_Z),
            sprite_with_size(assets.tile_texture(TileKind::SoftWall), TILE_SIZE - 2.0),
            Name::new("SoftWall"),
        ));
    }

    // Exit - green (0.2, 0.8, 0.2)
    commands.spawn((
        StageTile,
        GridPosition(map.exit_tile),
        TileKind::Exit,
        tile_to_transform_z(map.exit_tile, TILE_Z),
        sprite_with_size(assets.tile_texture(TileKind::Exit), TILE_SIZE - 2.0),
        Name::new("Exit"),
    ));
}

pub fn tile_to_transform(tile: IVec2) -> Transform {
    let centered_x = (tile.x as f32 - (MAP_WIDTH - 1) as f32 / 2.0) * TILE_SIZE;
    let centered_y = (tile.y as f32 - (MAP_HEIGHT - 1) as f32 / 2.0) * TILE_SIZE;

    Transform::from_xyz(centered_x, centered_y, 0.0)
}

pub fn tile_to_transform_z(tile: IVec2, z: f32) -> Transform {
    let mut transform = tile_to_transform(tile);
    transform.translation.z = z;
    transform
}

pub fn map_world_size() -> Vec2 {
    Vec2::new(MAP_WIDTH as f32 * TILE_SIZE, MAP_HEIGHT as f32 * TILE_SIZE)
}

pub fn is_blocked(tile: IVec2, map: &StageMap, bomb_tiles: &HashSet<IVec2>) -> bool {
    map.hard_walls.contains(&tile) || map.soft_walls.contains(&tile) || bomb_tiles.contains(&tile)
}

impl StageMap {
    pub fn restore_layout(&mut self) {
        self.soft_walls = self.initial_soft_walls.clone();
    }
}
