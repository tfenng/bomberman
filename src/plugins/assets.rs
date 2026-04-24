use bevy::prelude::*;

use crate::plugins::{enemy::EnemyKind, map::TileKind};

pub struct SpriteAssetsPlugin;

impl Plugin for SpriteAssetsPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<SpriteAssets>();
    }
}

#[derive(Resource, Debug, Clone)]
pub struct SpriteAssets {
    #[allow(dead_code)]
    floor: Handle<Image>,
    hard_wall: Handle<Image>,
    soft_wall: Handle<Image>,
    exit: Handle<Image>,
    player: Handle<Image>,
    drifter: Handle<Image>,
    seeker_y: Handle<Image>,
    seeker_x: Handle<Image>,
    hunter: Handle<Image>,
    phantom: Handle<Image>,
    punisher: Handle<Image>,
    bomb: Handle<Image>,
    flame: Handle<Image>,
}

impl FromWorld for SpriteAssets {
    fn from_world(world: &mut World) -> Self {
        let asset_server = world.resource::<AssetServer>();

        Self {
            floor: asset_server.load("images/floor.png"),
            hard_wall: asset_server.load("images/hard-wall.png"),
            soft_wall: asset_server.load("images/soft-wall.png"),
            exit: asset_server.load("images/exit.png"),
            player: asset_server.load("images/player.png"),
            drifter: asset_server.load("images/enemy-drifter.png"),
            seeker_y: asset_server.load("images/enemy-seeker-y.png"),
            seeker_x: asset_server.load("images/enemy-seeker-x.png"),
            hunter: asset_server.load("images/enemy-hunter.png"),
            phantom: asset_server.load("images/enemy-phantom.png"),
            punisher: asset_server.load("images/enemy-punisher.png"),
            bomb: asset_server.load("images/bomb.png"),
            flame: asset_server.load("images/flame.png"),
        }
    }
}

impl SpriteAssets {
    pub fn tile_texture(&self, kind: TileKind) -> Handle<Image> {
        match kind {
            TileKind::HardWall => self.hard_wall.clone(),
            TileKind::SoftWall => self.soft_wall.clone(),
            TileKind::Exit => self.exit.clone(),
        }
    }

    pub fn player_texture(&self) -> Handle<Image> {
        self.player.clone()
    }

    pub fn enemy_texture(&self, kind: EnemyKind) -> Handle<Image> {
        match kind {
            EnemyKind::Drifter => self.drifter.clone(),
            EnemyKind::SeekerY => self.seeker_y.clone(),
            EnemyKind::SeekerX => self.seeker_x.clone(),
            EnemyKind::Hunter => self.hunter.clone(),
            EnemyKind::Phantom => self.phantom.clone(),
            EnemyKind::Punisher => self.punisher.clone(),
        }
    }

    pub fn bomb_texture(&self) -> Handle<Image> {
        self.bomb.clone()
    }

    pub fn flame_texture(&self) -> Handle<Image> {
        self.flame.clone()
    }
}

pub fn sprite_with_size(texture: Handle<Image>, size: f32) -> Sprite {
    let mut sprite = Sprite::from_image(texture);
    sprite.custom_size = Some(Vec2::splat(size));
    sprite
}
