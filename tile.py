"""
瓦片实体模块
《经典炸弹人》复刻版
"""

from typing import Optional
import pygame

from constants import (
    TileType, HARD_WALL_COLOR, SOFT_WALL_COLOR, GROUND_COLOR,
    EXIT_COLOR, TILE_SIZE
)
from assets import assets


class Tile:
    """瓦片类"""

    def __init__(
        self,
        tile_type: int,
        grid_x: int,
        grid_y: int,
        tile_size: int = TILE_SIZE
    ):
        self.type = tile_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size

        # 计算像素位置
        self.rect = pygame.Rect(
            grid_x * tile_size,
            grid_y * tile_size,
            tile_size,
            tile_size
        )

        # 动画相关
        self.animation_offset = 0
        self._destroyed = False

    @property
    def is_wall(self) -> bool:
        """是否为墙"""
        return self.type in (TileType.HARD_WALL, TileType.SOFT_WALL)

    @property
    def is_destructible(self) -> bool:
        """是否可破坏"""
        return self.type == TileType.SOFT_WALL

    @property
    def is_destroyed(self) -> bool:
        """是否已破坏"""
        return self._destroyed

    def destroy(self) -> bool:
        """破坏瓦片（仅软墙）"""
        if self.is_destructible and not self._destroyed:
            self._destroyed = True
            self.type = TileType.EMPTY
            return True
        return False

    def update(self, dt: float):
        """更新瓦片状态"""
        pass

    def render(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """渲染瓦片"""
        draw_rect = pygame.Rect(
            self.rect.x + offset_x,
            self.rect.y + offset_y,
            self.tile_size,
            self.tile_size
        )

        if self.type == TileType.HARD_WALL:
            self._draw_hard_wall(surface, draw_rect)
        elif self.type == TileType.SOFT_WALL:
            self._draw_soft_wall(surface, draw_rect)
        elif self.type == TileType.EXIT:
            self._draw_exit(surface, draw_rect)
        else:
            self._draw_ground(surface, draw_rect)

    def _draw_hard_wall(self, surface: pygame.Surface, rect: pygame.Rect):
        """绘制硬墙"""
        # 主体
        pygame.draw.rect(surface, HARD_WALL_COLOR, rect)

        # 边框效果
        border_color = tuple(max(0, c - 30) for c in HARD_WALL_COLOR)
        pygame.draw.rect(surface, border_color, rect, 2)

        # 内部纹理效果
        inner_rect = rect.inflate(-8, -8)
        texture_color = tuple(max(0, c - 20) for c in HARD_WALL_COLOR)
        pygame.draw.rect(surface, texture_color, inner_rect)

        # 砖块线条
        line_color = tuple(max(0, c - 40) for c in HARD_WALL_COLOR)
        mid_y = rect.y + rect.height // 2
        pygame.draw.line(surface, line_color, (rect.x, mid_y), (rect.right, mid_y), 2)

    def _draw_soft_wall(self, surface: pygame.Surface, rect: pygame.Rect):
        """绘制软墙（可破坏）"""
        if self._destroyed:
            return

        # 主体
        pygame.draw.rect(surface, SOFT_WALL_COLOR, rect)

        # 边框
        border_color = tuple(max(0, c - 40) for c in SOFT_WALL_COLOR)
        pygame.draw.rect(surface, border_color, rect, 3)

        # 砖块纹理
        brick_color = tuple(max(0, c - 30) for c in SOFT_WALL_COLOR)
        brick_height = rect.height // 3
        for i in range(3):
            y = rect.y + i * brick_height
            pygame.draw.line(surface, brick_color, (rect.x, y), (rect.right, y), 2)

            # 错位
            offset = 8 if i % 2 == 0 else -8
            pygame.draw.line(surface, brick_color, (rect.x + offset, y), (rect.x + offset, y + brick_height), 2)

    def _draw_ground(self, surface: pygame.Surface, rect: pygame.Rect):
        """绘制地面"""
        pygame.draw.rect(surface, GROUND_COLOR, rect)

        # 草地纹理
        grass_color = tuple(min(255, c + 20) for c in GROUND_COLOR)
        for i in range(0, rect.width, 8):
            for j in range(0, rect.height, 8):
                if (i + j) % 16 == 0:
                    pygame.draw.circle(surface, grass_color, (rect.x + i, rect.y + j), 2)

    def _draw_exit(self, surface: pygame.Surface, rect: pygame.Rect):
        """绘制出口"""
        # 地面
        pygame.draw.rect(surface, GROUND_COLOR, rect)

        # 出口发光效果
        glow_rect = rect.inflate(4, 4)
        pygame.draw.rect(surface, EXIT_COLOR, glow_rect, 2)

        # 出口标志
        center = rect.center
        pygame.draw.circle(surface, EXIT_COLOR, center, rect.width // 3, 3)

        # 闪烁效果
        import time
        pulse = (time.time() % 1.0) * 0.5 + 0.5
        fill_color = tuple(int(c * pulse) for c in EXIT_COLOR)
        pygame.draw.circle(surface, fill_color, center, rect.width // 4)


class TileFactory:
    """瓦片工厂类"""

    _instance: Optional['TileFactory'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_tile(self, tile_type: int, grid_x: int, grid_y: int) -> Tile:
        """创建瓦片实例"""
        return Tile(tile_type, grid_x, grid_y)

    def create_from_legend(self, legend_char: str, grid_x: int, grid_y: int, tile_legend: dict) -> Tile:
        """根据图例字符创建瓦片"""
        tile_type_str = tile_legend.get(legend_char, "empty")

        type_map = {
            "hard_wall": TileType.HARD_WALL,
            "soft_wall": TileType.SOFT_WALL,
            "exit": TileType.EXIT,
            "empty": TileType.EMPTY
        }

        tile_type = type_map.get(tile_type_str, TileType.EMPTY)
        return self.create_tile(tile_type, grid_x, grid_y)
