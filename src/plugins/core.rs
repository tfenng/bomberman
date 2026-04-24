use bevy::{prelude::*, window::PrimaryWindow};

use crate::plugins::{
    app::AppState,
    map::{map_world_size, TILE_SIZE},
};

pub struct CorePlugin;

const CAMERA_PADDING_TILES: f32 = 0.0;

impl Plugin for CorePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(ClearColor(Color::srgb(0.05, 0.05, 0.08)))
            .add_systems(Startup, setup_camera)
            .add_systems(Update, (fit_camera_to_window, handle_global_input));
    }
}

fn setup_camera(mut commands: Commands) {
    commands.spawn((Camera2d, Name::new("MainCamera")));
}

fn fit_camera_to_window(
    windows: Query<&Window, With<PrimaryWindow>>,
    mut cameras: Query<&mut Projection, With<Camera2d>>,
) {
    let Ok(window) = windows.single() else {
        return;
    };
    let Ok(mut projection) = cameras.single_mut() else {
        return;
    };

    let padded_world_size = map_world_size() + Vec2::splat(TILE_SIZE * CAMERA_PADDING_TILES * 2.0);
    let scale_x = padded_world_size.x / window.width().max(1.0);
    let scale_y = padded_world_size.y / window.height().max(1.0);
    let fit_scale = scale_x.max(scale_y).max(1.0);

    if let Projection::Orthographic(ref mut orthographic) = *projection {
        orthographic.scale = fit_scale;
    }
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
