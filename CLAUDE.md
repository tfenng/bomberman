# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Boomer** is a classic Bomberman (《经典炸弹人》) game clone built with Python and Pygame. It is a simplified demo version focusing on core gameplay mechanics.

- **Language**: Python 3.10+
- **Framework**: Pygame 2.5.0+

## Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run game:**
```bash
python main.py
```

**Build standalone executable:**
```bash
python build_config.py
```
Output: `dist/Bomberman` (or `.exe` on Windows)

## Controls

| Key | Action |
|-----|--------|
| W/A/S/D | Move |
| Space | Place bomb |
| R | Restart |
| Esc | Exit |

## Architecture (Planned)

Based on the PRD, the intended architecture follows these layers:

| Layer | Modules |
|-------|---------|
| Entry Point | `main.py` |
| Game Loop | `game.py` |
| Entities | `player.py`, `enemy.py`, `bomb.py`, `explosion.py`, `powerup.py`, `tile.py` |
| Systems | `grid.py`, `collision.py`, `spawner.py`, `ai.py` |
| Scenes | `base_scene.py`, `game_scene.py`, `menu_scene.py`, `result_scene.py` |
| UI | `hud.py`, `text_render.py` |
| Utils | `assets.py`, `constants.py`, `helpers.py` |

## Level Configuration

Level file: `assets/maps/level_01.json`
- Grid: 13 columns x 11 rows
- Tile size: 48 pixels
- 4 enemies (1 chase, 3 basic)
- Bomb fuse: 2s, Explosion duration: 0.3s, Initial power: 1

## Key Game Features

- Single-player puzzle mode
- Destructible soft walls (50% powerup drop rate)
- Powerups: Fire (+1 range), Bomb (+1 count), Speed (+20%)
- 2 enemy AI types: Basic (random), Chase (player tracking)
- Win: Kill all enemies + reach exit
- Lose: Hit by explosion or enemy
