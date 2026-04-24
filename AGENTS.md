# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

This is the **Bevy game engine** repository (v0.17.3). The actual engine code lives in the `bevy-release-0.17.3/` subdirectory. This is the engine itself, not a game project built with Bevy.

## Build Commands

All commands should be run from the `bevy-release-0.17.3/` subdirectory.

```sh
cd bevy-release-0.17.3

# Run an example
cargo run --example breakout

# Run all tests (except doc tests)
cargo run -p ci -- test

# Run lints (format + clippy)
cargo run -p ci -- lints

# Run a single test
cargo test -p <crate> --lib -- <test_name>

# Run clippy on a specific crate
cargo clippy -p <crate>

# Format check
cargo fmt --check
```

For faster iterative builds, copy the fast-build config:
```sh
cp .cargo/config_fast_builds.toml .cargo/config.toml
```

## Architecture

Bevy is built on an **Entity Component System (ECS)** paradigm. Key concepts:

- **Entities**: Unique IDs that hold Components
- **Components**: Plain Rust structs stored in a `World`
- **Systems**: Functions that process entity data via `Query`
- **Resources**: Singleton data (like `Time`, `AssetServer`)
- **Schedules**: Define execution order of Systems

### Core Crates

| Crate | Purpose |
|-------|---------|
| `bevy_ecs` | Core ECS implementation (World, Entity, Query, System) |
| `bevy_app` | Application layer (App, Plugin, Schedule) |
| `bevy_asset` | Asset loading and management |
| `bevy_render` | Rendering pipeline (camera, mesh, material) |
| `bevy_input` | Input handling (keyboard, mouse, gamepad) |
| `bevy_transform` | Transform/position hierarchy |
| `bevy_ui` | UI layout and rendering |
| `bevy_state` | State machine support |
| `bevy_reflect` | Dynamic type reflection |
| `bevy_pbr` | Physically-based rendering |
| `bevy_sprite` | 2D sprite rendering |
| `bevy_animation` | Skeletal animation |
| `bevy_gltf` | glTF model loading |
| `bevy_scene` | Scene serialization/deserialization |

### Render Architecture

The render pipeline uses:
1. `bevy_render` - core render graph
2. `bevy_core_pipeline` - built-in render passes (forward, deferred, post-processing)
3. `bevy_pbr` - PBR materials and lighting
4. `bevy_sprite_render` - 2D sprite batching
5. `bevy_ui_render` - UI rendering

### Key File Patterns

- `crates/*/src/lib.rs` - crate entry point, re-exports public API via `mod` hierarchy
- `crates/*/src/*.rs` - feature-gated modules
- `examples/**/*.rs` - runnable examples organized by category
- `tools/ci/src/commands/*.rs` - CI command definitions

## Important Notes

- **MSRV**: Bevy MSRV is close to "latest stable Rust" due to heavy use of modern Rust features
- **Edition 2024**: This version uses Rust edition 2024
- **Unsafe Code**: The codebase has `unsafe_code = deny` in lints; any unsafe code requires careful review
- **Compile-time Validation**: Error codes (in `errors/`) are validated at compile-time to ensure documentation stays in sync
