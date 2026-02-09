"""
游戏主场景模块
《经典炸弹人》复刻版
"""

from typing import Dict, List, Optional
import pygame
from pygame.math import Vector2

from constants import (
    GameState, Direction, WHITE, BLACK, UI_BG_COLOR,
    UI_TEXT_COLOR, HARD_WALL_COLOR, SOFT_WALL_COLOR, GROUND_COLOR,
    TileType
)
from base_scene import BaseScene
from grid import Grid
from spawner import Spawner
from player import Player, PlayerState
from enemy import Enemy
from explosion import ExplosionManager
from bomb import BombManager
from powerup import PowerupManager
from helpers import distance
from fonts import font_manager


class GameScene(BaseScene):
    """游戏主场景"""

    def __init__(self, game):
        super().__init__(game)

        # 游戏数据
        self.level_data: Optional[Dict] = None
        self.spawner: Optional[Spawner] = None
        self.grid: Optional[Grid] = None
        self.player: Optional[Player] = None
        self.enemies: List[Enemy] = []

        # 字体
        self.ui_font = font_manager.get_font(size=24, bold=True)
        self.status_font = font_manager.get_font(size=20)
        self.title_font = font_manager.get_font(size=64, bold=True)
        self.hint_font = font_manager.get_font(size=24)
        self.stats_font = font_manager.get_font(size=20)
        self.warning_font = font_manager.get_font(size=28, bold=True)

        # 输入状态
        self.keys_pressed = set()

        # 游戏统计
        self.kill_count = 0
        self.total_enemies = 0
        self.time_elapsed = 0.0

        # 游戏状态
        self.game_over = False
        self.victory = False
        self.exit_open = False
        self.exit_hint_timer = 0.0  # 出口提示显示时间

    def enter(self):
        """进入游戏场景"""
        self._load_level()

    def _load_level(self):
        """加载关卡"""
        # 创建网格
        self.grid = Grid(13, 11)

        # 创建生成器
        self.spawner = Spawner(self.grid)

        # 加载关卡数据
        self.level_data = self.spawner.load_level("level_01")

        # 获取敌人总数
        self.total_enemies = len(self.level_data.get("enemies", []))

        # 生成玩家
        player_start = self.level_data.get("player_start", {"col": 2, "row": 1})
        self.player = self.spawner.spawn_player(
            grid_x=player_start["col"],
            grid_y=player_start["row"],
            player_id=0
        )

        # 生成敌人
        self.enemies = self.spawner.spawn_enemies_from_level(self.level_data)

        # 检查出口位置
        exit_data = self.level_data.get("exit", {})
        exit_x = exit_data.get("col", 11)
        exit_y = exit_data.get("row", 5)
        self.exit_open = not exit_data.get("hidden_under_soft_wall", True)

        # 重置状态
        self.kill_count = 0
        self.time_elapsed = 0.0
        self.game_over = False
        self.victory = False

    def handle_event(self, event: pygame.event.Event):
        """处理游戏事件"""
        if self.game_over or self.victory:
            # 游戏结束状态下的操作
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._load_level()  # 重新开始
                elif event.key == pygame.K_ESCAPE:
                    self.set_next_state(GameState.MENU)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 放置炸弹
                if self.player and self.player.alive:
                    self.player.bomb_pressed = True

            elif event.key == pygame.K_r:
                # 重新开始
                self._load_level()

            elif event.key == pygame.K_ESCAPE:
                # 退出到菜单
                self.set_next_state(GameState.MENU)

    def handle_key_state(self, keys):
        """处理按键状态"""
        if self.game_over or self.victory or not self.player or not self.player.alive:
            return

        # 方向输入
        direction = Vector2(0, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction += Vector2(0, -1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction += Vector2(0, 1)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction += Vector2(-1, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += Vector2(1, 0)

        self.player.input_direction = direction.normalize() if direction.length() > 0 else Vector2(0, 0)

    def update(self, dt: float):
        """更新游戏状态"""
        if self.game_over or self.victory:
            return

        self.time_elapsed += dt

        # 更新玩家
        if self.player and self.player.alive:
            self._update_player(dt)

            # 放置炸弹
            if self.player.bomb_pressed and self.player.can_place_bomb():
                self.spawner.bomb_manager.create_bomb(
                    grid_x=self.player.grid_x,
                    grid_y=self.player.grid_y,
                    power=self.player.bomb_power,
                    owner_id=self.player.id
                )
                self.grid.add_bomb(self.player.grid_x, self.player.grid_y)
                self.player.placed_bombs += 1
            self.player.bomb_pressed = False

        # 更新敌人
        self._update_enemies(dt)

        # 更新爆炸（需要在炸弹更新之前）
        self.spawner.explosion_manager.update(dt)

        # 更新炸弹
        exit_data = self.level_data.get("exit", {})
        exit_pos = (exit_data.get("col", 11), exit_data.get("row", 9))
        exploded_bombs = self.spawner.bomb_manager.update(
            dt, grid=self.grid, explosion_manager=self.spawner.explosion_manager, exit_pos=exit_pos
        )

        # 炸弹爆炸时从被破坏的软墙生成道具
        destroyed_walls = []
        for bomb in exploded_bombs:
            destroyed_walls.extend(bomb.explosion_tiles)

        if destroyed_walls:
            self.spawner.spawn_powerups_from_soft_walls(
                self.level_data, destroyed_walls
            )

        # 处理炸弹爆炸回调
        for bomb in exploded_bombs:
            if bomb.owner_id == self.player.id:
                self.player.on_bomb_exploded()

        # 更新道具
        self.spawner.powerup_manager.update(dt)

        # 检查玩家与敌人碰撞
        self._check_player_enemy_collision()

        # 更新出口提示计时器
        if self.exit_hint_timer > 0:
            self.exit_hint_timer -= dt

        # 检查胜利条件
        self._check_victory_condition()

    def _update_player(self, dt: float):
        """更新玩家状态"""
        was_alive = self.player.alive

        self.player.update(
            dt=dt,
            grid=self.grid,
            bomb_manager=self.spawner.bomb_manager,
            explosion_manager=self.spawner.explosion_manager,
            powerup_manager=self.spawner.powerup_manager
        )

        # 检查玩家是否被炸死
        if was_alive and not self.player.alive:
            self.game_over = True

    def _update_enemies(self, dt: float):
        """更新敌人状态"""
        alive_enemies = []

        for enemy in self.enemies:
            if not enemy.alive:
                continue

            enemy.update(
                dt=dt,
                grid=self.grid,
                player=self.player,
                explosion_manager=self.spawner.explosion_manager
            )

            if enemy.alive:
                alive_enemies.append(enemy)
            else:
                # 敌人死亡
                self.kill_count += 1

        self.enemies = alive_enemies

    def _check_player_enemy_collision(self):
        """检查玩家与敌人碰撞"""
        if not self.player or not self.player.alive:
            return

        for enemy in self.enemies:
            if enemy.alive and enemy.check_player_collision(self.player):
                self.player.die()
                self.game_over = True
                break

    def _check_victory_condition(self):
        """检查胜利条件"""
        # 条件1: 消灭所有敌人
        all_enemies_dead = all(not e.alive for e in self.enemies)

        # 条件2: 玩家到达出口
        if self.player and self.player.alive:
            # 检查玩家是否在出口上
            exit_data = self.level_data.get("exit", {})
            exit_x = exit_data.get("col", 11)
            exit_y = exit_data.get("row", 9)

            if (self.player.grid_x == exit_x and self.player.grid_y == exit_y):
                if all_enemies_dead:
                    self.player.victory()
                    self.victory = True
                else:
                    # 玩家到达出口但还有敌人，显示提示
                    alive_enemies = sum(1 for e in self.enemies if e.alive)
                    if self.exit_hint_timer <= 0:
                        self.exit_hint_timer = 2.0

    def render(self, surface: pygame.Surface):
        """渲染游戏场景"""
        # 绘制背景
        surface.fill(GROUND_COLOR)

        # 绘制地图
        self._draw_map(surface)

        # 绘制道具
        self.spawner.powerup_manager.render(surface, self.grid.offset_x, self.grid.offset_y)

        # 绘制炸弹
        self.spawner.bomb_manager.render(surface, self.grid.offset_x, self.grid.offset_y)

        # 绘制敌人
        for enemy in self.enemies:
            enemy.render(surface, self.grid.offset_x, self.grid.offset_y)

        # 绘制玩家
        if self.player:
            self.player.render(surface, self.grid.offset_x, self.grid.offset_y)

        # 绘制爆炸
        self.spawner.explosion_manager.render(surface, self.grid.offset_x, self.grid.offset_y)

        # 绘制UI
        self._draw_ui(surface)

        # 绘制出口提示
        if self.exit_hint_timer > 0 and not self.victory:
            alive_enemies = sum(1 for e in self.enemies if e.alive)
            hint_text = f"还需消灭 {alive_enemies} 个敌人!"
            text = self.warning_font.render(hint_text, True, (255, 100, 100))
            text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() - 100))
            # 添加文字背景
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect)
            pygame.draw.rect(surface, (255, 100, 100), bg_rect, 2)
            surface.blit(text, text_rect)

        # 绘制游戏结束/胜利画面
        if self.game_over:
            self._draw_game_over(surface)
        elif self.victory:
            self._draw_victory(surface)

    def _draw_map(self, surface: pygame.Surface):
        """绘制地图"""
        offset_x = self.grid.offset_x
        offset_y = self.grid.offset_y

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                tile_type = self.grid.get_tile(x, y)
                rect = pygame.Rect(
                    x * self.grid.tile_size + offset_x,
                    y * self.grid.tile_size + offset_y,
                    self.grid.tile_size,
                    self.grid.tile_size
                )

                if tile_type == TileType.HARD_WALL:
                    # 硬墙
                    pygame.draw.rect(surface, HARD_WALL_COLOR, rect)
                    pygame.draw.rect(surface, (50, 50, 50), rect, 2)
                elif tile_type == TileType.SOFT_WALL:
                    # 软墙
                    pygame.draw.rect(surface, SOFT_WALL_COLOR, rect)
                    pygame.draw.rect(surface, (100, 60, 30), rect, 2)
                else:
                    # 地面
                    pygame.draw.rect(surface, (100, 180, 100), rect)
                    pygame.draw.rect(surface, (80, 160, 80), rect, 1)

                # 绘制出口
                if tile_type == TileType.EXIT:
                    pygame.draw.circle(surface, (100, 200, 255),
                                     rect.center, 20)
                    pygame.draw.circle(surface, (200, 255, 255),
                                     rect.center, 15, 2)

    def _draw_ui(self, surface: pygame.Surface):
        """绘制UI"""
        # 顶部信息栏
        ui_height = 50
        pygame.draw.rect(surface, UI_BG_COLOR, (0, 0, surface.get_width(), ui_height))

        # 分割线
        pygame.draw.line(surface, (60, 60, 70), (0, ui_height), (surface.get_width(), ui_height), 2)

        # 敌人数量
        alive_enemies = sum(1 for e in self.enemies if e.alive)
        enemy_text = self.ui_font.render(
            f"敌人: {alive_enemies}/{self.total_enemies}", True, WHITE
        )
        surface.blit(enemy_text, (20, 12))

        # 时间
        time_text = self.ui_font.render(
            f"时间: {self.time_elapsed:.1f}s", True, WHITE
        )
        time_rect = time_text.get_rect(center=(surface.get_width() // 2, ui_height // 2))
        surface.blit(time_text, time_rect)

        # 玩家状态
        if self.player:
            power_text = self.status_font.render(
                f"火力: {self.player.bomb_power}", True, (255, 100, 100)
            )
            surface.blit(power_text, (surface.get_width() - 150, 12))

            bomb_text = self.status_font.render(
                f"炸弹: {self.player.placed_bombs}/{self.player.bomb_count}", True, (100, 100, 255)
            )
            surface.blit(bomb_text, (surface.get_width() - 280, 12))

    def _draw_game_over(self, surface: pygame.Surface):
        """绘制游戏结束画面"""
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # 游戏结束文字
        text = self.title_font.render("游戏结束", True, (220, 60, 60))
        text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))
        surface.blit(text, text_rect)

        # 提示文字
        hint1 = self.hint_font.render("按 R 重新开始", True, WHITE)
        hint2 = self.hint_font.render("按 ESC 返回菜单", True, WHITE)

        surface.blit(hint1, (surface.get_width() // 2 - hint1.get_width() // 2, surface.get_height() // 2 + 20))
        surface.blit(hint2, (surface.get_width() // 2 - hint2.get_width() // 2, surface.get_height() // 2 + 60))

    def _draw_victory(self, surface: pygame.Surface):
        """绘制胜利画面"""
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # 胜利文字
        text = self.title_font.render("胜利!", True, (255, 200, 0))
        text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))
        surface.blit(text, text_rect)

        # 统计信息
        stats = [
            f"击杀敌人: {self.kill_count}/{self.total_enemies}",
            f"用时: {self.time_elapsed:.1f}秒"
        ]

        for i, stat in enumerate(stats):
            stat_text = self.stats_font.render(stat, True, WHITE)
            surface.blit(stat_text, (surface.get_width() // 2 - stat_text.get_width() // 2,
                                    surface.get_height() // 2 + 20 + i * 30))

        # 提示文字
        hint1 = self.hint_font.render("按 R 再玩一次", True, WHITE)
        hint2 = self.hint_font.render("按 ESC 返回菜单", True, WHITE)

        surface.blit(hint1, (surface.get_width() // 2 - hint1.get_width() // 2, surface.get_height() // 2 + 100))
        surface.blit(hint2, (surface.get_width() // 2 - hint2.get_width() // 2, surface.get_height() // 2 + 140))
