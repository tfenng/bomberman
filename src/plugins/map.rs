use std::collections::HashSet;

use bevy::prelude::*;

pub const TILE_SIZE: f32 = 55.0;

pub struct MapPlugin;

impl Plugin for MapPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<StageMap>()
            .add_systems(Startup, setup_stage_map);
    }
}

#[derive(Resource, Debug, Clone)]
pub struct StageMap {
    pub width: i32,
    pub height: i32,
    pub hard_walls: HashSet<IVec2>,
    pub soft_walls: HashSet<IVec2>,
    pub exit_tile: IVec2,
    pub player_spawn: IVec2,
}

impl Default for StageMap {
    fn default() -> Self {
        let width = 21;
        let height = 13;
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
            soft_walls,
            exit_tile: IVec2::new(width - 2, height - 2),
            player_spawn: IVec2::new(1, 1),
        }
    }
}

#[derive(Component, Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct GridPosition(pub IVec2);

#[derive(Component, Debug, Clone, Copy, PartialEq, Eq)]
pub enum TileKind {
    HardWall,
    SoftWall,
    Exit,
}

fn setup_stage_map(mut commands: Commands, map: Res<StageMap>) {
    // Floor - dark background (0.15, 0.15, 0.2)
    for y in 0..map.height {
        for x in 0..map.width {
            let tile = IVec2::new(x, y);
            commands.spawn((
                GridPosition(tile),
                tile_to_transform(tile),
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
            GridPosition(*tile),
            TileKind::HardWall,
            tile_to_transform(*tile),
            Sprite {
                color: Color::srgb(0.3, 0.3, 0.35),
                custom_size: Some(Vec2::splat(TILE_SIZE - 2.0)),
                ..default()
            },
            Name::new("HardWall"),
        ));
    }

    // Soft walls - light tan (0.85, 0.75, 0.55)
    for tile in &map.soft_walls {
        commands.spawn((
            GridPosition(*tile),
            TileKind::SoftWall,
            tile_to_transform(*tile),
            Sprite {
                color: Color::srgb(0.85, 0.75, 0.55),
                custom_size: Some(Vec2::splat(TILE_SIZE - 2.0)),
                ..default()
            },
            Name::new("SoftWall"),
        ));
    }

    // Exit - green (0.2, 0.8, 0.2)
    commands.spawn((
        GridPosition(map.exit_tile),
        TileKind::Exit,
        tile_to_transform(map.exit_tile),
        Sprite {
            color: Color::srgb(0.2, 0.8, 0.2),
            custom_size: Some(Vec2::splat(TILE_SIZE - 2.0)),
            ..default()
        },
        Name::new("Exit"),
    ));
}

pub fn tile_to_transform(tile: IVec2) -> Transform {
    Transform::from_xyz(tile.x as f32 * TILE_SIZE, tile.y as f32 * TILE_SIZE, 0.0)
}

pub fn is_blocked(tile: IVec2, map: &StageMap, bomb_tiles: &HashSet<IVec2>) -> bool {
    map.hard_walls.contains(&tile) || map.soft_walls.contains(&tile) || bomb_tiles.contains(&tile)
}
