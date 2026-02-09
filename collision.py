"""
碰撞检测系统模块
《经典炸弹人》复刻版
"""

from typing import Tuple, Optional, List
import pygame
from pygame.math import Vector2

from constants import CollisionType, TILE_SIZE
from grid import Grid
from helpers import clamp, circle_rect_collision, circle_collision


class CollisionInfo:
    """碰撞信息类"""

    def __init__(
        self,
        collision_type: int = CollisionType.NONE,
        direction: Vector2 = Vector2(0, 0),
        position: Tuple[float, float] = (0, 0),
        tile_pos: Tuple[int, int] = (-1, -1)
    ):
        self.type = collision_type
        self.direction = direction
        self.position = position
        self.tile_pos = tile_pos
        self.normal = Vector2(0, 0)

    def __bool__(self):
        return self.type != CollisionType.NONE


class CollisionSystem:
    """碰撞检测系统"""

    def __init__(self, grid: Grid):
        self.grid = grid

    def check_circle_to_grid(
        self,
        center_x: float,
        center_y: float,
        radius: float,
        check_bombs: bool = True
    ) -> CollisionInfo:
        """检测圆形与网格的碰撞"""
        # 转换为网格坐标
        grid_x, grid_y = self.grid.pixel_to_grid(center_x, center_y)

        # 检查当前格子是否是墙
        if self.grid.is_wall(grid_x, grid_y):
            return self._create_wall_collision(
                center_x, center_y, radius, grid_x, grid_y
            )

        # 检查炸弹
        if check_bombs and self.grid.has_bomb(grid_x, grid_y):
            return CollisionInfo(
                CollisionType.BOMB,
                Vector2(0, 0),
                (center_x, center_y),
                (grid_x, grid_y)
            )

        # 检查玩家圆形是否与相邻墙重叠
        # 只检查玩家可能接触到的墙
        neighbors = [
            (grid_x - 1, grid_y),  # 左
            (grid_x + 1, grid_y),  # 右
            (grid_x, grid_y - 1),  # 上
            (grid_x, grid_y + 1),  # 下
        ]

        for nx, ny in neighbors:
            if not self.grid.is_valid_grid(nx, ny):
                continue

            if self.grid.is_wall(nx, ny):
                # 计算玩家是否真正碰到这面墙
                if self._circle_overlaps_tile(center_x, center_y, radius, nx, ny):
                    return self._create_wall_collision(
                        center_x, center_y, radius, nx, ny
                    )

            if check_bombs and self.grid.has_bomb(nx, ny):
                return CollisionInfo(
                    CollisionType.BOMB,
                    Vector2(0, 0),
                    (center_x, center_y),
                    (nx, ny)
                )

        return CollisionInfo()

    def _circle_overlaps_tile(self, cx: float, cy: float, radius: float, tile_x: int, tile_y: int) -> bool:
        """检查圆形是否与指定格子重叠"""
        # 格子的像素范围
        tile_px = self.grid.offset_x + tile_x * self.grid.tile_size
        tile_py = self.grid.offset_y + tile_y * self.grid.tile_size
        tile_size = self.grid.tile_size

        # 找到圆形上距离格子中心最近的点
        closest_x = max(tile_px, min(cx, tile_px + tile_size))
        closest_y = max(tile_py, min(cy, tile_py + tile_size))

        # 计算距离
        dist_x = cx - closest_x
        dist_y = cy - closest_y
        dist_sq = dist_x * dist_x + dist_y * dist_y

        return dist_sq < radius * radius

    def _create_wall_collision(
        self,
        center_x: float,
        center_y: float,
        radius: float,
        wall_x: int,
        wall_y: int
    ) -> CollisionInfo:
        """创建与墙的碰撞信息"""
        wall_pixel_x = self.grid.offset_x + wall_x * self.grid.tile_size
        wall_pixel_y = self.grid.offset_y + wall_y * self.grid.tile_size

        # 找到圆形上距离墙最近的点
        closest_x = clamp(center_x, wall_pixel_x, wall_pixel_x + TILE_SIZE)
        closest_y = clamp(center_y, wall_pixel_y, wall_pixel_y + TILE_SIZE)

        # 计算碰撞方向
        direction = Vector2(center_x - closest_x, center_y - closest_y)
        if direction.length() > 0:
            direction = direction.normalize()

        return CollisionInfo(
            CollisionType.WALL,
            direction,
            (closest_x, closest_y),
            (wall_x, wall_y)
        )

    def check_rect_to_grid(
        self,
        rect: pygame.Rect,
        check_bombs: bool = True
    ) -> List[CollisionInfo]:
        """检测矩形与网格的碰撞"""
        collisions = []

        # 获取矩形覆盖的所有格子
        grid_left, grid_top = self.grid.pixel_to_grid(rect.left, rect.top)
        grid_right, grid_bottom = self.grid.pixel_to_grid(rect.right, rect.bottom)

        for gx in range(grid_left, grid_right + 1):
            for gy in range(grid_top, grid_bottom + 1):
                if not self.grid.is_valid_grid(gx, gy):
                    continue

                if self.grid.is_wall(gx, gy):
                    collisions.append(CollisionInfo(
                        CollisionType.WALL,
                        Vector2(0, 0),
                        (gx * TILE_SIZE, gy * TILE_SIZE),
                        (gx, gy)
                    ))

                if check_bombs and self.grid.has_bomb(gx, gy):
                    collisions.append(CollisionInfo(
                        CollisionType.BOMB,
                        Vector2(0, 0),
                        (gx * TILE_SIZE, gy * TILE_SIZE),
                        (gx, gy)
                    ))

        return collisions

    def predict_position(
        self,
        current_pos: Tuple[float, float],
        velocity: Vector2,
        radius: float,
        check_bombs: bool = True
    ) -> Tuple[float, float, bool]:
        """
        预测移动后的位置和碰撞状态
        返回: (新位置x, 新位置y, 是否发生碰撞)
        """
        new_x = current_pos[0] + velocity.x
        new_y = current_pos[1] + velocity.y

        collision = self.check_circle_to_grid(new_x, new_y, radius, check_bombs)

        if collision:
            # 发生碰撞，需要调整位置
            return current_pos[0], current_pos[1], True

        return new_x, new_y, False

    def resolve_collision(
        self,
        position: Tuple[float, float],
        velocity: Vector2,
        radius: float,
        check_bombs: bool = True
    ) -> Tuple[float, float, Vector2]:
        """
        解决碰撞，返回调整后的位置和碰撞法线
        """
        new_x, new_y, collided = self.predict_position(
            position, velocity, radius, check_bombs
        )

        if collided:
            # 尝试只移动X
            test_x, _, _ = self.predict_position(
                position, Vector2(velocity.x, 0), radius, check_bombs
            )

            # 尝试只移动Y
            _, test_y, _ = self.predict_position(
                position, Vector2(0, velocity.y), radius, check_bombs
            )

            # 选择碰撞较小的方向
            collision_x = self.check_circle_to_grid(test_x, position[1], radius, check_bombs)
            collision_y = self.check_circle_to_grid(position[0], test_y, radius, check_bombs)

            if not collision_x and collision_y:
                new_x = test_x
                normal = Vector2(1, 0) if velocity.x > 0 else Vector2(-1, 0)
            elif collision_x and not collision_y:
                new_y = test_y
                normal = Vector2(0, 1) if velocity.y > 0 else Vector2(0, -1)
            elif not collision_x and not collision_y:
                new_x = test_x
                new_y = test_y
                normal = Vector2(0, 0)
            else:
                # 两个方向都碰撞，回到原位
                new_x, new_y = position
                normal = velocity.normalize() * -1 if velocity.length() > 0 else Vector2(0, 0)

            return new_x, new_y, normal

        return new_x, new_y, Vector2(0, 0)

    def is_path_clear(
        self,
        start_pos: Tuple[float, float],
        end_pos: Tuple[float, float],
        radius: float
    ) -> bool:
        """检查两点之间的路径是否畅通"""
        steps = 10
        for i in range(steps + 1):
            t = i / steps
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
            if self.check_circle_to_grid(x, y, radius, check_bombs=False):
                return False
        return True

    def check_entity_collision(
        self,
        pos1: Tuple[float, float],
        radius1: float,
        pos2: Tuple[float, float],
        radius2: float
    ) -> bool:
        """检测两个实体之间的碰撞"""
        return circle_collision(pos1, radius1, pos2, radius2)

    def get_tile_center(self, grid_x: int, grid_y: int) -> Tuple[float, float]:
        """获取格子中心像素坐标"""
        return self.grid.grid_to_pixel(grid_x, grid_y, center=True)

    def pixel_to_tile(self, pixel_x: float, pixel_y: float) -> Tuple[int, int]:
        """像素坐标转网格坐标"""
        return self.grid.pixel_to_grid(pixel_x, pixel_y)
