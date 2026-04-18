use bevy::prelude::*;

use crate::plugins::app::AppState;

pub struct CorePlugin;

impl Plugin for CorePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(ClearColor(Color::srgb(0.05, 0.05, 0.08)))
            .add_systems(Startup, setup_camera)
            .add_systems(Update, handle_global_input);
    }
}

fn setup_camera(mut commands: Commands) {
    // Map is 21x13 tiles at 55px = 1155x715 pixels, center at (577.5, 357.5)
    commands.spawn((
        Camera2d,
        Transform::from_xyz(577.5, 357.5, 0.0),
        Name::new("MainCamera"),
    ));
}

fn handle_global_input(
    keyboard: Res<ButtonInput<KeyCode>>,
    state: Res<State<AppState>>,
    mut next_state: ResMut<NextState<AppState>>,
) {
    if keyboard.just_pressed(KeyCode::Escape) {
        match state.get() {
            AppState::InGame => next_state.set(AppState::Paused),
            AppState::Paused => next_state.set(AppState::InGame),
            AppState::MainMenu | AppState::GameOver | AppState::Victory => {}
        }
    }

    if keyboard.just_pressed(KeyCode::Enter) {
        match state.get() {
            AppState::MainMenu => next_state.set(AppState::InGame),
            AppState::GameOver | AppState::Victory => next_state.set(AppState::MainMenu),
            AppState::InGame | AppState::Paused => {}
        }
    }
}
