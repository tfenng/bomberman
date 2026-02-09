"""
炸弹实体模块
《经典炸弹人》复刻版
"""

from typing import Optional, List, Tuple
import pygame

from constants import (
    BOMB_COLOR, BOMB_CORE_COLOR, BOMB_SIZE, BOMB_FUSE_TIME,
    EXPLOSION_DURATION, BOMB_ANIMATION_SPEED, Direction
)
from helpers import Timer, Cooldown
from grid import Grid
from assets import assets


class Bomb:
    """炸弹实体类"""

    def __init__(
        self,
        grid_x: int,
        grid_y: int,
        power: int = 1,
        fuse_time: float = BOMB_FUSE_TIME,
        owner_id: Optional[int] = None
    ):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.power = power
        self.owner_id = owner_id

        # 计算像素位置（炸弹放在格子中心）
        self.position = pygame.math.Vector2(0, 0)

        # 计时器
        self.fuse_timer = Timer(fuse_time)
        self.animation_timer = 0.0

        # 状态
        self._exploded = False
        self._triggered = False

        # 爆炸覆盖的格子
        self._explosion_tiles: List[Tuple[int, int]] = []

        # 大小
        self.size = BOMB_SIZE

    @property
    def is_ready_to_explode(self) -> bool:
        """是否准备好爆炸"""
        return self.fuse_timer.update(0) and not self._exploded

    @property
    def exploded(self) -> bool:
        """是否已爆炸"""
        return self._exploded

    @property
    def explosion_tiles(self) -> List[Tuple[int, int]]:
        """获取爆炸覆盖的格子"""
        return self._explosion_tiles.copy()

    @property
    def time_remaining(self) -> float:
        """获取剩余引爆时间"""
        return self.fuse_timer.time_remaining()

    def trigger(self):
        """立即引爆炸弹"""
        self._triggered = True

    def explode(self, grid: Grid):
        """执行爆炸"""
        if self._exploded:
            return

        self._exploded = True
        self._explosion_tiles = grid.get_explosion_tiles(
            self.grid_x, self.grid_y, self.power
        )

        # 从网格中移除炸弹
        grid.remove_bomb(self.grid_x, self.grid_y)

    def update(self, dt: float, grid: Grid):
        """更新炸弹状态"""
        if self._exploded:
            return

        # 更新引信计时器
        self.animation_timer += dt
        if self.animation_timer >= BOMB_ANIMATION_SPEED * 4:
            self.animation_timer = 0

        # 检查是否需要爆炸
        self.fuse_timer.update(dt)
        if self.fuse_timer.elapsed >= self.fuse_timer.duration or self._triggered:
            self.explode(grid)

    def render(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """渲染炸弹"""
        if self._exploded:
            return

        # 计算绘制位置
        center_x = self.grid_x * grid.TILE_SIZE + grid.TILE_SIZE // 2 + offset_x
        center_y = self.grid_y * grid.TILE_SIZE + grid.TILE_SIZE // 2 + offset_y

        # 计算脉冲动画
        pulse = (self.animation_timer / (BOMB_ANIMATION_SPEED * 4))
        scale = 1.0 + 0.15 * pulse
        radius = int(self.size // 2 * scale)

        # 绘制阴影
        shadow_color = (0, 0, 0, 100)
        shadow_surface = pygame.Surface((radius * 2 + 8, radius * 2 + 8), pygame.SRCALPHA)
        pygame.draw.circle(
            shadow_surface, shadow_color,
            (radius + 4, radius + 4), radius
        )
        surface.blit(shadow_surface, (center_x - radius - 4, center_y - radius - 4 + 4))

        # 绘制主体
        pygame.draw.circle(surface, BOMB_COLOR, (center_x, center_y), radius)

        # 绘制高光
        highlight_pos = (center_x - radius // 3, center_y - radius // 3)
        pygame.draw.circle(surface, (100, 100, 100), highlight_pos, radius // 4)

        # 绘制核心（随脉冲闪烁）
        if int(self.animation_timer / BOMB_ANIMATION_SPEED) % 2 == 0:
            pygame.draw.circle(
                surface, BOMB_CORE_COLOR,
                (center_x + radius // 3, center_y + radius // 3),
                radius // 3
            )

        # 绘制引信
        fuse_x = center_x + radius // 2
        fuse_y = center_y - radius // 2
        pygame.draw.line(
            surface, (80, 60, 40),
            (center_x, center_y - radius // 2),
            (fuse_x, fuse_y - 8), 3
        )

        # 绘制火花
        spark_size = 4
        spark_offset = (self.animation_timer * 30) % 10
        pygame.draw.circle(
            surface, (255, 200, 0),
            (fuse_x + spark_offset, fuse_y - 8), spark_size
        )

    def get_rect(self) -> pygame.Rect:
        """获取碰撞矩形"""
        return pygame.Rect(
            self.grid_x * grid.TILE_SIZE,
            self.grid_y * grid.TILE_SIZE,
            grid.TILE_SIZE,
            grid.TILE_SIZE
        )


# 导入grid的TILE_SIZE
from constants import TILE_SIZE as GRID_TILE_SIZE
grid = type('Grid', (), {'TILE_SIZE': GRID_TILE_SIZE})()


class BombManager:
    """炸弹管理器"""

    def __init__(self):
        self._bombs: List[Bomb] = []
        self._next_id = 0

    def create_bomb(
        self,
        grid_x: int,
        grid_y: int,
        power: int = 1,
        fuse_time: float = BOMB_FUSE_TIME,
        owner_id: Optional[int] = None
    ) -> Bomb:
        """创建新炸弹"""
        bomb = Bomb(grid_x, grid_y, power, fuse_time, owner_id)
        self._bombs.append(bomb)
        self._next_id += 1
        return bomb

    def remove_bomb(self, bomb: Bomb):
        """移除炸弹"""
        if bomb in self._bombs:
            self._bombs.remove(bomb)

    def get_bomb_at(self, grid_x: int, grid_y: int) -> Optional[Bomb]:
        """获取指定位置的炸弹"""
        for bomb in self._bombs:
            if bomb.grid_x == grid_x and bomb.grid_y == grid_y:
                return bomb
        return None

    def get_all_bombs(self) -> List[Bomb]:
        """获取所有炸弹"""
        return self._bombs.copy()

    def trigger_all(self):
        """引爆所有炸弹"""
        for bomb in self._bombs:
            bomb.trigger()

    def update(self, dt: float, grid: Grid, explosion_manager=None, powerup_manager=None, exit_pos=None):
        """更新所有炸弹"""
        # 使用列表副本避免迭代时修改
        bombs_to_remove = []
        exploded_bombs = []
        destroyed_walls = []

        for bomb in self._bombs[:]:
            if bomb.exploded:
                bombs_to_remove.append(bomb)
            else:
                bomb.update(dt, grid)
                if bomb.exploded:
                    # 炸弹爆炸，销毁波及的软墙
                    for tx, ty in bomb.explosion_tiles:
                        if grid.destroy_soft_wall(tx, ty, exit_pos):
                            destroyed_walls.append((tx, ty))

                    # 创建爆炸效果
                    if explosion_manager:
                        explosion_manager.create_explosion(
                            grid=grid,
                            center_x=bomb.grid_x,
                            center_y=bomb.grid_y,
                            power=bomb.power
                        )
                    bombs_to_remove.append(bomb)
                    exploded_bombs.append(bomb)

        # 移除已爆炸的炸弹
        for bomb in bombs_to_remove:
            self.remove_bomb(bomb)

        return exploded_bombs

    def render(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """渲染所有炸弹"""
        for bomb in self._bombs:
            bomb.render(surface, offset_x, offset_y)

    def clear(self):
        """清空所有炸弹"""
        self._bombs.clear()
