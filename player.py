"""
玩家实体模块
《经典炸弹人》复刻版
"""

from typing import Optional, List, Tuple
import pygame
from pygame.math import Vector2

from constants import (
    PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED_DEFAULT,
    Direction, CollisionType, WHITE, BLACK,
    INITIAL_BOMB_POWER, INITIAL_BOMB_COUNT,
    MAX_BOMB_POWER, MAX_BOMB_COUNT
)
from helpers import Cooldown
from collision import CollisionSystem, CollisionInfo
from grid import Grid
from bomb import BombManager
from explosion import ExplosionManager
from powerup import PowerupManager


class PlayerState:
    """玩家状态枚举"""

    IDLE = "idle"
    MOVING = "moving"
    PLACING_BOMB = "placing_bomb"
    DEAD = "dead"
    VICTORIOUS = "victorious"


class Player:
    """玩家实体类"""

    def __init__(
        self,
        grid_x: int,
        grid_y: int,
        player_id: int = 0,
        collision_system: Optional[CollisionSystem] = None
    ):
        self.id = player_id
        self.state = PlayerState.IDLE

        # 网格位置
        self.grid_x = grid_x
        self.grid_y = grid_y

        # 像素位置
        self.position = pygame.math.Vector2(0, 0)

        # 移动速度
        self.speed = PLAYER_SPEED_DEFAULT
        self.velocity = pygame.math.Vector2(0, 0)

        # 大小
        self.size = PLAYER_SIZE
        self.radius = PLAYER_SIZE // 2 - 2  # 稍微减小碰撞半径，便于移动

        # 炸弹相关
        self.bomb_power = INITIAL_BOMB_POWER
        self.bomb_count = INITIAL_BOMB_COUNT
        self.placed_bombs = 0
        self._bomb_cooldown = Cooldown(0.2)  # 防止连续放置

        # 道具加成
        self._powerup_bonuses = {
            "fire_bonus": 0,
            "bomb_bonus": 0,
            "speed_multiplier": 1.0
        }

        # 碰撞系统
        self.collision = collision_system

        # 输入状态
        self.input_direction = pygame.math.Vector2(0, 0)
        self.bomb_pressed = False

        # 动画
        self.animation_frame = 0
        self.animation_timer = 0

        # 存活状态
        self.alive = True

        # 初始化位置
        self._update_pixel_position()

    def set_collision_system(self, collision_system: CollisionSystem):
        """设置碰撞系统"""
        self.collision = collision_system
        # 更新像素位置
        self._update_pixel_position()

    def set_position(self, grid_x: int, grid_y: int):
        """设置玩家位置"""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self._update_pixel_position()

    def _update_pixel_position(self):
        """更新像素位置"""
        if self.collision:
            self.position = pygame.math.Vector2(
                self.collision.get_tile_center(self.grid_x, self.grid_y)
            )

    def can_place_bomb(self) -> bool:
        """检查是否可以放置炸弹"""
        return (
            self.alive and
            self.placed_bombs < self.bomb_count and
            self._bomb_cooldown.is_ready() and
            self.collision and
            self.collision.grid.can_place_bomb(self.grid_x, self.grid_y)
        )

    def place_bomb(self, bomb_manager: BombManager) -> bool:
        """放置炸弹"""
        if not self.can_place_bomb():
            return False

        bomb = bomb_manager.create_bomb(
            grid_x=self.grid_x,
            grid_y=self.grid_y,
            power=self.bomb_power,
            owner_id=self.id
        )

        if bomb:
            self.placed_bombs += 1
            self.collision.grid.add_bomb(self.grid_x, self.grid_y)
            self._bomb_cooldown.use()
            # 播放放置炸弹音效
            from assets import assets
            assets.play_sound("place_bomb")
            return True
        return False

    def add_bomb_bonus(self):
        """增加炸弹数量上限"""
        self.bomb_count = min(self.bomb_count + 1, MAX_BOMB_COUNT)

    def add_fire_bonus(self):
        """增加爆炸威力"""
        self.bomb_power = min(self.bomb_power + 1, MAX_BOMB_POWER)

    def add_speed_bonus(self):
        """增加移动速度"""
        bonus = PLAYER_SPEED_DEFAULT * 0.2
        self.speed = min(self.speed + bonus, PLAYER_SPEED_DEFAULT * 1.5)

    def on_bomb_exploded(self):
        """炸弹爆炸回调"""
        if self.placed_bombs > 0:
            self.placed_bombs -= 1

    def update(
        self,
        dt: float,
        grid: Grid,
        bomb_manager: BombManager,
        explosion_manager: ExplosionManager,
        powerup_manager: PowerupManager
    ):
        """更新玩家状态"""
        if not self.alive:
            return

        # 更新冷却
        self._bomb_cooldown.update(dt)

        # 更新道具效果
        bonuses = powerup_manager.get_total_bonus()
        self._powerup_bonuses = bonuses
        self.bomb_count = INITIAL_BOMB_COUNT + bonuses["bomb_bonus"]
        self.bomb_power = INITIAL_BOMB_POWER + bonuses["fire_bonus"]
        self.speed = PLAYER_SPEED_DEFAULT * bonuses["speed_multiplier"]

        # 处理移动
        self._update_movement(dt, grid, bomb_manager)

        # 更新动画
        self._update_animation(dt)

        # 检查与爆炸的碰撞
        self._check_explosion_collision(explosion_manager)

        # 检查与道具的碰撞
        self._check_powerup_collision(powerup_manager)

        # 更新状态
        if self.velocity.length() > 0:
            self.state = PlayerState.MOVING
        else:
            self.state = PlayerState.IDLE

    def _update_movement(self, dt: float, grid: Grid, bomb_manager: BombManager):
        """更新移动"""
        if not self.collision:
            return

        # 计算实际速度
        actual_speed = self.speed * dt
        move_vector = self.input_direction * actual_speed

        if move_vector.length() > 0:
            move_vector = move_vector.normalize() * actual_speed

            # 玩家当前是否在炸弹格子上
            on_bomb = grid.has_bomb(self.grid_x, self.grid_y)

            # 分别检查X和Y方向
            # 玩家当前位置有炸弹时：可以向任意方向移动
            # 玩家当前位置没有炸弹时：不能走进有炸弹的格子

            # 计算新位置
            new_x = self.position.x + move_vector.x
            new_y = self.position.y + move_vector.y

            # 计算新位置的网格坐标
            new_grid_x, new_grid_y = self.collision.pixel_to_tile(new_x, new_y)

            # 检查墙壁碰撞（只关心Wall类型）
            collision_x = self.collision.check_circle_to_grid(new_x, self.position.y, self.radius * 0.8)
            collision_y = self.collision.check_circle_to_grid(self.position.x, new_y, self.radius * 0.8)

            # Wall碰撞阻止移动
            can_move_x = collision_x.type != 1  # type 1 = WALL
            can_move_y = collision_y.type != 1

            # 如果玩家不在炸弹格子上，不能走进有炸弹的格子
            if not on_bomb and grid.has_bomb(new_grid_x, new_grid_y):
                if move_vector.x != 0:
                    can_move_x = False
                if move_vector.y != 0:
                    can_move_y = False

            # 应用移动
            if can_move_x:
                self.position.x = new_x
            if can_move_y:
                self.position.y = new_y

            # 更新网格位置
            new_grid_x, new_grid_y = self.collision.pixel_to_tile(self.position.x, self.position.y)
            if grid.is_valid_grid(new_grid_x, new_grid_y):
                self.grid_x = new_grid_x
                self.grid_y = new_grid_y

    def _update_animation(self, dt: float):
        """更新动画"""
        self.animation_timer += dt
        if self.animation_timer >= 0.1:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4

    def _check_explosion_collision(self, explosion_manager: ExplosionManager):
        """检查与爆炸的碰撞"""
        if self.collision:
            offset_x = self.collision.grid.offset_x
            offset_y = self.collision.grid.offset_y
        else:
            offset_x = 0
            offset_y = 0

        if explosion_manager.check_any_hit_position(
            self.position.x, self.position.y, self.radius * 0.7, offset_x, offset_y
        ):
            self.die()

    def _check_powerup_collision(self, powerup_manager: PowerupManager):
        """检查与道具的碰撞"""
        powerup = powerup_manager.get_powerup_at(self.grid_x, self.grid_y)
        if powerup:
            powerup_manager.add_effect(powerup)
            # 播放拾取音效
            from assets import assets
            assets.play_sound("pickup")

    def die(self):
        """玩家死亡"""
        if self.alive:
            self.alive = False
            self.state = PlayerState.DEAD

    def victory(self):
        """玩家胜利"""
        self.state = PlayerState.VICTORIOUS

    def render(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """渲染玩家"""
        if not self.alive:
            return

        # 玩家位置已包含偏移量，无需再次添加
        draw_x = self.position.x
        draw_y = self.position.y

        # 绘制阴影
        shadow_radius = int(self.radius * 0.8)
        shadow_offset = 4
        pygame.draw.circle(
            surface, (0, 0, 0, 80),
            (draw_x, draw_y + shadow_offset), shadow_radius
        )

        # 绘制身体
        pygame.draw.circle(surface, PLAYER_COLOR, (draw_x, draw_y), self.radius)

        # 绘制边框
        pygame.draw.circle(surface, WHITE, (draw_x, draw_y), self.radius, 2)

        # 绘制眼睛
        eye_offset = 6
        eye_radius = 4
        eye_color = WHITE

        # 根据方向移动眼睛
        look_x = self.input_direction.x * 2
        look_y = self.input_direction.y * 2

        # 左眼
        pygame.draw.circle(
            surface, eye_color,
            (draw_x - eye_offset + look_x, draw_y - 2 + look_y), eye_radius
        )
        pygame.draw.circle(
            surface, BLACK,
            (draw_x - eye_offset + look_x + 1, draw_y - 2 + look_y), 2
        )

        # 右眼
        pygame.draw.circle(
            surface, eye_color,
            (draw_x + eye_offset + look_x, draw_y - 2 + look_y), eye_radius
        )
        pygame.draw.circle(
            surface, BLACK,
            (draw_x + eye_offset + look_x + 1, draw_y - 2 + look_y), 2
        )

        # 绘制嘴巴
        mouth_y = draw_y + 6
        if self.state == PlayerState.MOVING:
            pygame.draw.arc(
                surface, BLACK,
                (draw_x - 6, mouth_y - 2, 12, 6),
                0, 3.14, 2
            )
        else:
            pygame.draw.line(surface, BLACK, (draw_x - 4, mouth_y), (draw_x + 4, mouth_y), 2)

        # 绘制移动方向指示器
        if self.input_direction.length() > 0:
            indicator_length = self.radius + 8
            end_x = draw_x + self.input_direction.x * indicator_length
            end_y = draw_y + self.input_direction.y * indicator_length
            pygame.draw.line(
                surface, (100, 180, 255),
                (draw_x, draw_y), (end_x, end_y), 3
            )
            pygame.draw.circle(surface, (100, 180, 255), (end_x, end_y), 4)

    def get_rect(self) -> pygame.Rect:
        """获取碰撞矩形"""
        return pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
