# Repository Guidelines

## Project Structure & Module Organization

The root crate is `blast_maze`, a Bevy-based Bomberman-style game. Primary gameplay code lives in `src/`: `main.rs` boots the app, and `src/plugins/` contains feature-focused plugins such as `map.rs`, `player.rs`, `bomb.rs`, and `enemy.rs`. Runtime data lives in `assets/`; keep balance values in `assets/config/gameplay.json` and place LDtk level files in `assets/levels/` where the startup flow currently expects `stage_1.ldtk`. Design notes and planning live in `docs/` and `memory-bank/`. Treat `bevy-release-0.17.3/` as a vendored reference copy of Bevy, not the main application code.

## Build, Test, and Development Commands

Run commands from the repository root:

- `cargo run`: start the game locally.
- `cargo build --release`: produce an optimized build.
- `cargo test`: run unit and integration tests.
- `cargo check`: fast compile validation during iteration.
- `cargo clippy --all-targets --all-features`: lint gameplay and support code.
- `cargo fmt --check`: verify formatting before opening a PR.

The existing GitHub Actions workflow builds a Windows release target, so changes should continue to compile cleanly for `x86_64-pc-windows-msvc`.

## Coding Style & Naming Conventions

Follow standard Rust style: 4-space indentation, `snake_case` for functions/modules/files, `CamelCase` for types and plugins, and small, focused modules under `src/plugins/`. Prefer deriving traits (`Debug`, `Resource`, `States`) over manual boilerplate when practical. Use `cargo fmt` for formatting and fix Clippy warnings instead of suppressing them without a code-level reason.

## Testing Guidelines

There is no dedicated `tests/` directory yet, so add focused unit tests next to the affected module or create integration tests under `tests/` when cross-plugin behavior matters. Name tests after the behavior they verify, for example `bombs_expire_after_fuse`. Run `cargo test` before submitting, and pair gameplay logic changes with at least one test when the behavior can be exercised without a full graphical session.

## Commit & Pull Request Guidelines

Recent history uses short Conventional Commit prefixes such as `feat:`, `fix:`, `docs:`, and `chore:`. Keep that format and write concise, imperative summaries. Pull requests should explain the gameplay or tooling change, note any asset/config updates, link the relevant issue when available, and include screenshots or a short clip for visible gameplay changes.
