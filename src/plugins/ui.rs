use bevy::prelude::*;

use crate::plugins::{
    app::AppState,
    enemy::EnemyCount,
    game_state::{GameState, LevelTimer},
    player::Player,
};

pub struct UiPlugin;

#[derive(Component)]
struct HudRoot;

impl Plugin for UiPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(AppState::InGame), setup_hud)
            .add_systems(Update, update_hud.run_if(in_state(AppState::InGame)));
    }
}

fn setup_hud(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        HudRoot,
        DespawnOnExit(AppState::InGame),
        Text::new(""),
        TextFont {
            font: asset_server.load("fonts/FiraSans-Bold.ttf"),
            font_size: 20.0,
            ..default()
        },
        TextColor(Color::srgb(0.95, 0.95, 0.98)),
        Node {
            position_type: PositionType::Absolute,
            top: px(12.0),
            left: px(12.0),
            padding: UiRect::all(px(10.0)),
            ..default()
        },
        BackgroundColor(Color::srgba(0.05, 0.06, 0.09, 0.72)),
    ));
}

fn update_hud(
    game_state: Res<GameState>,
    level_timer: Res<LevelTimer>,
    enemy_count: Res<EnemyCount>,
    players: Query<&Player>,
    mut hud_text: Query<&mut Text, With<HudRoot>>,
) {
    let Ok(player) = players.single() else {
        return;
    };

    let Ok(mut text) = hud_text.single_mut() else {
        return;
    };

    let seconds_left = level_timer.remaining_seconds.ceil().max(0.0) as u32;
    text.0 = format!(
        "Level {:02}  Score {:05}\nLives {}  Enemies {}\nBombs {}  Fire {}  Time {:03}",
        game_state.current_level,
        game_state.score,
        game_state.lives,
        enemy_count.count,
        player.bomb_capacity,
        player.flame_length,
        seconds_left,
    );
}
