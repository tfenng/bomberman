use std::collections::HashSet;

use bevy::prelude::IVec2;
use blast_maze::plugins::{
    game_state::LevelTimer,
    map::{is_blocked, StageMap},
};

#[test]
fn spawn_area_stays_safe() {
    let map = StageMap::default();

    for tile in [
        map.player_spawn,
        map.player_spawn + IVec2::X,
        map.player_spawn + IVec2::Y,
    ] {
        assert!(
            !map.hard_walls.contains(&tile),
            "spawn tile {:?} should not be a hard wall",
            tile
        );
        assert!(
            !map.soft_walls.contains(&tile),
            "spawn tile {:?} should not be a soft wall",
            tile
        );
    }
}

#[test]
fn blocked_tiles_respect_hard_walls_and_bombs() {
    let map = StageMap::default();
    let mut bomb_tiles = HashSet::new();
    let bomb_tile = IVec2::new(3, 3);
    bomb_tiles.insert(bomb_tile);

    assert!(is_blocked(IVec2::new(0, 0), &map, &bomb_tiles));
    assert!(is_blocked(bomb_tile, &map, &bomb_tiles));
    assert!(!is_blocked(IVec2::new(1, 1), &map, &bomb_tiles));
}

#[test]
fn level_timer_reset_restores_full_duration() {
    let mut timer = LevelTimer::default();
    timer.remaining_seconds = 12.0;
    timer.timeout_triggered = true;

    timer.reset(300);

    assert_eq!(timer.total_seconds, 300);
    assert_eq!(timer.remaining_seconds, 300.0);
    assert!(!timer.timeout_triggered);
}
