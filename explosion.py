"""
爆炸实体模块
《经典炸弹人》复刻版
"""

from typing import List, Tuple, Optional, Set
import pygame
import math

from constants import (
    EXPLOSION_COLOR, EXPLOSION_DURATION, TILE_SIZE,
    Direction, WHITE
)
from helpers import Timer
from grid import Grid
from tile import TileType


class Explosion:
    """爆炸实体类"""

    def __init__(
        self,
        center_x: int,
        center_y: int,
        tiles: List[Tuple[int, int]],
        duration: float = EXPLOSION_DURATION
    ):
        self.center_x = center_x
        self.center_y = center_y
        self.tiles = tiles
        self.duration = duration
        self.timer = Timer(duration)

        # 动画状态
        self.animation_phase = 0.0

        # 方向标记（用于渲染爆炸臂）
        self._directions: Set[Tuple[int, int]] = set()
        for tx, ty in tiles:
            if (tx, ty) != (center_x, center_y):
                dx = tx - center_x
                dy = ty - center_y
                if dx != 0:
                    dx = 1 if dx > 0 else -1
                if dy != 0:
                    dy = 1 if dy > 0 else -1
                self._directions.add((dx, dy))

    @property
    def is_active(self) -> bool:
        """爆炸是否仍然活跃"""
        return not self.timer.update(0)

    @property
    def progress(self) -> float:
        """获取爆炸进度 (0.0 = 开始, 1.0 = 结束)"""
        return self.timer.get_progress()

    def update(self, dt: float):
        """更新爆炸状态"""
        self.animation_phase += dt * 10
        if self.animation_phase > math.pi * 2:
            self.animation_phase -= math.pi * 2
        self.timer.update(dt)

    def render(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """渲染爆炸"""
        if not self.is_active:
            return

        # 计算淡出效果
        fade_factor = 1.0 - self.timer.get_progress()

        # 计算脉冲效果
        pulse = 0.8 + 0.2 * math.sin(self.animation_phase)

        for tx, ty in self.tiles:
            self._draw_explosion_cell(
                surface, tx, ty, fade_factor * pulse, offset_x, offset_y
            )

    def _draw_explosion_cell(
        self,
        surface: pygame.Surface,
        grid_x: int,
        grid_y: int,
        alpha: float,
        offset_x: int,
        offset_y: int
    ):
        """绘制单个爆炸格子"""
        x = grid_x * TILE_SIZE + offset_x
        y = grid_y * TILE_SIZE + offset_y

        # 检查是否为爆炸中心
        is_center = (grid_x == self.center_x and grid_y == self.center_y)

        # 计算颜色（带淡出）
        base_color = list(EXPLOSION_COLOR)
        faded_color = [
            int(c * alpha) for c in base_color
        ]

        # 绘制爆炸主体
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, tuple(faded_color), rect)

        # 绘制中心高亮
        if is_center:
            inner_size = int(TILE_SIZE * 0.6 * alpha)
            center_x = x + TILE_SIZE // 2
            center_y = y + TILE_SIZE // 2
            pygame.draw.circle(
                surface, WHITE,
                (center_x, center_y), inner_size // 2
            )

        # 绘制边缘效果
        border_rect = rect.inflate(-8, -8)
        border_color = [
            min(255, int(c * 1.2)) for c in faded_color
        ]
        pygame.draw.rect(surface, tuple(border_color), border_rect, 2)

        # 绘制火花效果
        if alpha > 0.5:
            num_sparks = 3 if is_center else 2
            for i in range(num_sparks):
                spark_angle = self.animation_phase + (i * 2 * math.pi / num_sparks)
                spark_dist = TILE_SIZE * 0.3
                spark_x = x + TILE_SIZE // 2 + int(math.cos(spark_angle) * spark_dist)
                spark_y = y + TILE_SIZE // 2 + int(math.sin(spark_angle) * spark_dist)
                spark_size = 3
                pygame.draw.circle(
                    surface, (255, 255, 0),
                    (spark_x, spark_y), spark_size
                )

    def check_hit(self, rect: pygame.Rect, offset_x: int = 0, offset_y: int = 0) -> bool:
        """检查爆炸是否击中矩形区域"""
        for tx, ty in self.tiles:
            tile_rect = pygame.Rect(
                tx * TILE_SIZE + offset_x,
                ty * TILE_SIZE + offset_y,
                TILE_SIZE,
                TILE_SIZE
            )
            if tile_rect.colliderect(rect):
                return True
        return False

    def check_hit_position(self, pixel_x: float, pixel_y: float, radius: float, offset_x: int = 0, offset_y: int = 0) -> bool:
        """检查爆炸是否击中指定位置"""
        for tx, ty in self.tiles:
            center_x = tx * TILE_SIZE + TILE_SIZE // 2 + offset_x
            center_y = ty * TILE_SIZE + TILE_SIZE // 2 + offset_y
            dist_sq = (pixel_x - center_x) ** 2 + (pixel_y - center_y) ** 2
            if dist_sq < (radius + TILE_SIZE // 2) ** 2:
                return True
        return False


class ExplosionManager:
    """爆炸管理器"""

    def __init__(self):
        self._explosions: List[Explosion] = []

    def create_explosion(
        self,
        grid: Grid,
        center_x: int,
        center_y: int,
        power: int,
        duration: float = EXPLOSION_DURATION
    ) -> Explosion:
        """创建爆炸"""
        tiles = grid.get_explosion_tiles(center_x, center_y, power)
        explosion = Explosion(center_x, center_y, tiles, duration)
        self._explosions.append(explosion)
        return explosion

    def update(self, dt: float):
        """更新所有爆炸"""
        # 使用列表副本避免迭代时修改
        explosions_to_remove = []

        for explosion in self._explosions[:]:
            explosion.update(dt)
            if not explosion.is_active:
                explosions_to_remove.append(explosion)

        for explosion in explosions_to_remove:
            self._explosions.remove(explosion)

    def render(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """渲染所有爆炸"""
        for explosion in self._explosions:
            explosion.render(surface, offset_x, offset_y)

    def check_any_hit(self, rect: pygame.Rect, offset_x: int = 0, offset_y: int = 0) -> bool:
        """检查任何爆炸是否击中矩形"""
        for explosion in self._explosions:
            if explosion.check_hit(rect, offset_x, offset_y):
                return True
        return False

    def check_any_hit_position(self, pixel_x: float, pixel_y: float, radius: float, offset_x: int = 0, offset_y: int = 0) -> bool:
        """检查任何爆炸是否击中指定位置"""
        for explosion in self._explosions:
            if explosion.check_hit_position(pixel_x, pixel_y, radius, offset_x, offset_y):
                return True
        return False

    def get_active_explosions(self) -> List[Explosion]:
        """获取所有活跃的爆炸"""
        return [e for e in self._explosions if e.is_active]

    def clear(self):
        """清空所有爆炸"""
        self._explosions.clear()
