use bevy::prelude::*;

use crate::plugins::{
    app::AppState,
    assets::{sprite_with_size, SpriteAssets},
    map::{tile_to_transform_z, ACTOR_Z, GridPosition, TILE_SIZE},
};

#[derive(Resource, Debug, Default)]
pub struct EnemyCount {
    pub count: u32,
}

#[derive(Component, Debug, Clone, Copy, PartialEq, Eq)]
pub struct Enemy {
    pub kind: EnemyKind,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EnemyKind {
    Drifter,
    SeekerY,
    SeekerX,
    Hunter,
    Phantom,
    Punisher,
}

pub struct EnemyPlugin;

impl Plugin for EnemyPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<EnemyCount>()
            .add_systems(OnEnter(AppState::InGame), reset_enemy_count);
    }
}

fn reset_enemy_count(mut enemy_count: ResMut<EnemyCount>) {
    enemy_count.count = 0;
}

pub fn spawn_enemy(
    commands: &mut Commands,
    assets: &SpriteAssets,
    tile: IVec2,
    kind: EnemyKind,
) {
    commands.spawn((
        Enemy { kind },
        GridPosition(tile),
        tile_to_transform_z(tile, ACTOR_Z),
        sprite_with_size(assets.enemy_texture(kind), TILE_SIZE * 0.75),
        Name::new(format!("{kind:?}")),
    ));
}

pub fn spawn_punisher(commands: &mut Commands, assets: &SpriteAssets, tile: IVec2) {
    spawn_enemy(commands, assets, tile, EnemyKind::Punisher);
}
