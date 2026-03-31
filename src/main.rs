mod plugins;

use bevy::prelude::*;
use plugins::app::AppPlugin;

fn main() {
    App::new().add_plugins(AppPlugin).run();
}
