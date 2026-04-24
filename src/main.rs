use bevy::prelude::*;
use blast_maze::plugins::app::AppPlugin;

fn main() {
    App::new().add_plugins(AppPlugin).run();
}
