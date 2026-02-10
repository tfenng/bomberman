"""
网格系统模块
处理地图坐标转换和格子管理
《经典炸弹人》复刻版
"""

from typing import Tuple, Optional, List
from pygame.math import Vector2

from constants import TILE_SIZE, MAP_OFFSET_X, MAP_OFFSET_Y, TileType, TileChar


class Grid:
    """网格系统类"""

    def __init__(self, width: int, height: int, tile_size: int = TILE_SIZE):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.offset_x = MAP_OFFSET_X
        self.offset_y = MAP_OFFSET_Y

        # 初始化网格数据
        self._tiles: List[List[int]] = [
            [TileType.EMPTY for _ in range(width)] for _ in range(height)
        ]

        # 软墙列表（用于追踪可破坏的墙）
        self._soft_walls: set = set()

        # 炸弹列表
        self._bombs: set = set()

    # ============ 坐标转换 ============

    def pixel_to_grid(self, pixel_x: float, pixel_y: float) -> Tuple[int, int]:
        """像素坐标转换为网格坐标"""
        grid_x = int((pixel_x - self.offset_x) // self.tile_size)
        grid_y = int((pixel_y - self.offset_y) // self.tile_size)
        return self._clamp_grid(grid_x, grid_y)

    def grid_to_pixel(self, grid_x: int, grid_y: int, center: bool = True) -> Tuple[float, float]:
        """网格坐标转换为像素坐标"""
        x = self.offset_x + grid_x * self.tile_size
        y = self.offset_y + grid_y * self.tile_size
        if center:
            x += self.tile_size // 2
            y += self.tile_size // 2
        return x, y

    def pixel_to_grid_precise(self, pixel_x: float, pixel_y: float) -> Tuple[float, float]:
        """像素坐标精确转换为网格坐标（浮点数）"""
        grid_x = (pixel_x - self.offset_x) / self.tile_size
        grid_y = (pixel_y - self.offset_y) / self.tile_size
        return grid_x, grid_y

    def _clamp_grid(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """将网格坐标限制在有效范围内"""
        grid_x = max(0, min(grid_x, self.width - 1))
        grid_y = max(0, min(grid_y, self.height - 1))
        return grid_x, grid_y

    # ============ 格子访问 ============

    def get_tile(self, grid_x: int, grid_y: int) -> int:
        """获取指定格子的类型"""
        grid_x, grid_y = self._clamp_grid(grid_x, grid_y)
        return self._tiles[grid_y][grid_x]

    def set_tile(self, grid_x: int, grid_y: int, tile_type: int):
        """设置指定格子的类型"""
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            self._tiles[grid_y][grid_x] = tile_type

    def is_wall(self, grid_x: int, grid_y: int) -> bool:
        """检查是否为障碍物（硬墙或软墙）"""
        tile = self.get_tile(grid_x, grid_y)
        return tile in (TileType.HARD_WALL, TileType.SOFT_WALL)

    def is_hard_wall(self, grid_x: int, grid_y: int) -> bool:
        """检查是否为硬墙"""
        return self.get_tile(grid_x, grid_y) == TileType.HARD_WALL

    def is_soft_wall(self, grid_x: int, grid_y: int) -> bool:
        """检查是否为软墙"""
        return self.get_tile(grid_x, grid_y) == TileType.SOFT_WALL

    def is_empty(self, grid_x: int, grid_y: int) -> bool:
        """检查是否为空地（可通行，不包括墙）"""
        tile = self.get_tile(grid_x, grid_y)
        return tile == TileType.EMPTY or tile == TileType.EXIT

    def is_exit(self, grid_x: int, grid_y: int) -> bool:
        """检查是否为出口"""
        return self.get_tile(grid_x, grid_y) == TileType.EXIT

    def has_bomb(self, grid_x: int, grid_y: int) -> bool:
        """检查该格子是否有炸弹"""
        return (grid_x, grid_y) in self._bombs

    # ============ 软墙管理 ============

    def add_soft_wall(self, grid_x: int, grid_y: int):
        """添加软墙"""
        self.set_tile(grid_x, grid_y, TileType.SOFT_WALL)
        self._soft_walls.add((grid_x, grid_y))

    def remove_soft_wall(self, grid_x: int, grid_y: int):
        """移除软墙"""
        self.set_tile(grid_x, grid_y, TileType.EMPTY)
        self._soft_walls.discard((grid_x, grid_y))

    def destroy_soft_wall(self, grid_x: int, grid_y: int, exit_pos: tuple = None) -> bool:
        """破坏软墙，返回是否成功"""
        if self.is_soft_wall(grid_x, grid_y):
            # 检查是否是出口位置
            if exit_pos and grid_x == exit_pos[0] and grid_y == exit_pos[1]:
                self.set_tile(grid_x, grid_y, TileType.EXIT)
            else:
                self.set_tile(grid_x, grid_y, TileType.EMPTY)
            self._soft_walls.discard((grid_x, grid_y))
            return True
        return False

    def get_soft_walls(self) -> set:
        """获取所有软墙位置"""
        return self._soft_walls.copy()

    # ============ 炸弹管理 ============

    def add_bomb(self, grid_x: int, grid_y: int):
        """添加炸弹"""
        self._bombs.add((grid_x, grid_y))

    def remove_bomb(self, grid_x: int, grid_y: int):
        """移除炸弹"""
        self._bombs.discard((grid_x, grid_y))

    # ============ 碰撞检测辅助 ============

    def get_tile_rect(self, grid_x: int, grid_y: int) -> Tuple[float, float, float, float]:
        """获取格子的矩形边界（像素坐标）"""
        x = self.offset_x + grid_x * self.tile_size
        y = self.offset_y + grid_y * self.tile_size
        return x, y, self.tile_size, self.tile_size

    def is_position_walkable(
        self,
        pixel_x: float,
        pixel_y: float,
        entity_radius: float = 16
    ) -> bool:
        """检查像素位置是否可通行"""
        # 检查四个角点
        corners = [
            (pixel_x - entity_radius, pixel_y - entity_radius),
            (pixel_x + entity_radius, pixel_y - entity_radius),
            (pixel_x - entity_radius, pixel_y + entity_radius),
            (pixel_x + entity_radius, pixel_y + entity_radius)
        ]

        for cx, cy in corners:
            gx, gy = self.pixel_to_grid(cx, cy)
            if self.is_wall(gx, gy) or self.has_bomb(gx, gy):
                return False
        return True

    def can_place_bomb(self, grid_x: int, grid_y: int) -> bool:
        """检查是否可以放置炸弹"""
        return self.is_empty(grid_x, grid_y) and not self.has_bomb(grid_x, grid_y)

    # ============ 爆炸传播计算 ============

    def get_explosion_tiles(
        self,
        center_x: int,
        center_y: int,
        power: int
    ) -> List[Tuple[int, int]]:
        """计算爆炸覆盖的所有格子"""
        tiles = [(center_x, center_y)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            for i in range(1, power + 1):
                tx, ty = center_x + dx * i, center_y + dy * i

                if not self.is_valid_grid(tx, ty):
                    break

                tile = self.get_tile(tx, ty)

                if tile == TileType.HARD_WALL:
                    # 硬墙阻挡爆炸
                    break

                tiles.append((tx, ty))

                if tile == TileType.SOFT_WALL:
                    # 软墙被破坏，爆炸不再继续传播
                    break

        return tiles

    def is_valid_grid(self, grid_x: int, grid_y: int) -> bool:
        """检查网格坐标是否有效"""
        return 0 <= grid_x < self.width and 0 <= grid_y < self.height

    # ============ 地图数据 ============

    def load_from_data(self, level_data: dict):
        """从关卡数据加载地图"""
        tiles = level_data.get("tiles", [])
        tile_legend = level_data.get("tile_legend", None)  # 新格式可能没有 tile_legend

        # 支持两种格式：
        # 1. 新格式：直接使用 TileChar 字符映射
        # 2. 旧格式：使用 tile_legend 映射

        # 定义默认字符映射
        char_to_type = {
            TileChar.HARD_WALL: TileType.HARD_WALL,
            TileChar.SOFT_WALL: TileType.SOFT_WALL,
            TileChar.EMPTY: TileType.EMPTY,
            TileChar.EXIT: TileType.EXIT,
            TileChar.PLAYER: TileType.EMPTY,  # 玩家出生点标记设为空地
        }

        for row_idx, row in enumerate(tiles):
            for col_idx, char in enumerate(row):
                if col_idx >= self.width or row_idx >= self.height:
                    continue

                # 根据格式确定 tile 类型
                if tile_legend:
                    # 旧格式：使用 tile_legend
                    tile_type_str = tile_legend.get(char, "empty")
                    if tile_type_str == "hard_wall":
                        tile_type = TileType.HARD_WALL
                    elif tile_type_str == "soft_wall":
                        self.add_soft_wall(col_idx, row_idx)
                        continue
                    elif tile_type_str == "exit":
                        tile_type = TileType.EXIT
                    else:
                        tile_type = TileType.EMPTY
                else:
                    # 新格式：直接使用字符映射
                    tile_type = char_to_type.get(char, TileType.EMPTY)
                    if char == TileChar.SOFT_WALL:
                        self.add_soft_wall(col_idx, row_idx)
                        continue

                self.set_tile(col_idx, row_idx, tile_type)

    def create_default_map(self):
        """创建默认地图（四周硬墙）"""
        # 设置边界为硬墙
        for x in range(self.width):
            self.set_tile(x, 0, TileType.HARD_WALL)
            self.set_tile(x, self.height - 1, TileType.HARD_WALL)

        for y in range(self.height):
            self.set_tile(0, y, TileType.HARD_WALL)
            self.set_tile(self.width - 1, y, TileType.HARD_WALL)

        # 内部格子随机生成软墙
        import random
        for y in range(2, self.height - 2, 2):
            for x in range(2, self.width - 2, 2):
                if random.random() < 0.6:
                    self.add_soft_wall(x, y)

    # ============ 属性 ============

    @property
    def size(self) -> Tuple[int, int]:
        """获取网格尺寸"""
        return self.width, self.height

    @property
    def pixel_size(self) -> Tuple[int, int]:
        """获取像素尺寸"""
        return self.width * self.tile_size, self.height * self.tile_size
