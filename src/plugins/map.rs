use std::collections::HashSet;

use bevy::prelude::*;

pub const TILE_SIZE: f32 = 32.0;

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
        let width = 15;
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

                // 简单模板式软墙分布
                if (x + y) % 3 != 0 {
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
    for tile in &map.hard_walls {
        commands.spawn((
            GridPosition(*tile),
            TileKind::HardWall,
            tile_to_transform(*tile),
            Name::new("HardWall"),
        ));
    }

    for tile in &map.soft_walls {
        commands.spawn((
            GridPosition(*tile),
            TileKind::SoftWall,
            tile_to_transform(*tile),
            Name::new("SoftWall"),
        ));
    }

    commands.spawn((
        GridPosition(map.exit_tile),
        TileKind::Exit,
        tile_to_transform(map.exit_tile),
        Name::new("HiddenExit"),
    ));
}

pub fn tile_to_transform(tile: IVec2) -> Transform {
    Transform::from_xyz(tile.x as f32 * TILE_SIZE, tile.y as f32 * TILE_SIZE, 0.0)
}

pub fn is_blocked(tile: IVec2, map: &StageMap, bomb_tiles: &HashSet<IVec2>) -> bool {
    map.hard_walls.contains(&tile) || map.soft_walls.contains(&tile) || bomb_tiles.contains(&tile)
}
