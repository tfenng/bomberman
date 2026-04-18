use bevy::prelude::*;

use crate::plugins::app::AppState;

#[derive(Resource, Debug, Default)]
pub struct EnemyCount {
    pub count: u32,
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
