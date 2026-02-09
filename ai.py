"""
AI 辅助模块
提供敌人AI决策支持
《经典炸弹人》复刻版
"""

from typing import List, Tuple, Optional, Dict
from heapq import heappush, heappop
from pygame.math import Vector2

from grid import Grid
from constants import Direction, TileType


class AStarPathfinder:
    """A* 路径查找器"""

    def __init__(self, grid: Grid):
        self.grid = grid

    def find_path(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        avoid_bombs: bool = True
    ) -> Optional[List[Tuple[int, int]]]:
        """
        查找从起点到终点的路径
        返回路径点列表，如果无法到达则返回 None
        """
        # 使用 A* 算法
        frontier = []  # 优先队列
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        cost_so_far: Dict[Tuple[int, int], float] = {}

        heappush(frontier, (0, start))
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            _, current = heappop(frontier)

            if current == goal:
                return self._reconstruct_path(came_from, start, goal)

            for next_pos in self._get_neighbors(current, avoid_bombs):
                new_cost = cost_so_far[current] + 1

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self._heuristic(goal, next_pos)
                    heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        return None

    def _reconstruct_path(
        self,
        came_from: Dict,
        start: Tuple[int, int],
        goal: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """重建路径"""
        path = [goal]
        current = goal
        while current != start:
            current = came_from[current]
            if current is None:
                return []
            path.append(current)
        path.reverse()
        return path

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """曼哈顿距离启发式"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _get_neighbors(
        self,
        pos: Tuple[int, int],
        avoid_bombs: bool = True
    ) -> List[Tuple[int, int]]:
        """获取相邻的可通行格子"""
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            nx, ny = pos[0] + dx, pos[1] + dy

            if not self.grid.is_valid_grid(nx, ny):
                continue

            if self.grid.is_empty(nx, ny):
                if avoid_bombs and self.grid.has_bomb(nx, ny):
                    continue
                neighbors.append((nx, ny))

        return neighbors


class ThreatAnalyzer:
    """威胁分析器 - 分析地图上的危险区域"""

    def __init__(self, grid: Grid):
        self.grid = grid

    def get_safe_tiles(self, explosion_manager) -> List[Tuple[int, int]]:
        """获取所有安全格子（不会被爆炸波及的格子）"""
        safe_tiles = []

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self._is_tile_safe(x, y, explosion_manager):
                    safe_tiles.append((x, y))

        return safe_tiles

    def _is_tile_safe(
        self,
        grid_x: int,
        grid_y: int,
        explosion_manager
    ) -> bool:
        """检查指定格子是否安全"""
        # 检查当前格子
        offset_x = self.grid.offset_x
        offset_y = self.grid.offset_y
        if explosion_manager.check_any_hit_position(
            grid_x * self.grid.tile_size + self.grid.tile_size // 2 + offset_x,
            grid_y * self.grid.tile_size + self.grid.tile_size // 2 + offset_y,
            self.grid.tile_size // 2
        ):
            return False

        # 检查周围格子是否有炸弹
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in neighbors:
            nx, ny = grid_x + dx, grid_y + dy
            if self.grid.has_bomb(nx, ny):
                # 这个格子可能会被炸弹波及
                return False

        return True

    def find_nearest_safe_tile(
        self,
        start: Tuple[int, int],
        explosion_manager
    ) -> Optional[Tuple[int, int]]:
        """找到最近的安全格子"""
        safe_tiles = self.get_safe_tiles(explosion_manager)
        if not safe_tiles:
            return None

        # 使用曼哈顿距离找最近的
        nearest = None
        min_dist = float('inf')

        for tile in safe_tiles:
            dist = abs(tile[0] - start[0]) + abs(tile[1] - start[1])
            if dist < min_dist:
                min_dist = dist
                nearest = tile

        return nearest

    def get_escape_direction(
        self,
        current_pos: Tuple[int, int],
        explosion_manager
    ) -> Optional[Vector2]:
        """获取逃离危险的方向"""
        # 找到最近的安全格子
        safe_tile = self.find_nearest_safe_tile(current_pos, explosion_manager)
        if not safe_tile:
            return None

        # 计算方向
        dx = safe_tile[0] - current_pos[0]
        dy = safe_tile[1] - current_pos[1]

        if abs(dx) > abs(dy):
            return Vector2(1 if dx > 0 else -1, 0)
        else:
            return Vector2(0, 1 if dy > 0 else -1)


class SmartEnemyAI:
    """智能敌人AI - 结合追踪和避险"""

    def __init__(self, grid: Grid, enemy):
        self.grid = grid
        self.enemy = enemy
        self.pathfinder = AStarPathfinder(grid)
        self.threat_analyzer = ThreatAnalyzer(grid)

    def get_movement_direction(
        self,
        player,
        explosion_manager
    ) -> Vector2:
        """获取智能移动方向"""
        if not self.enemy.alive:
            return Vector2(0, 0)

        # 首先检查是否需要逃离危险
        escape_dir = self.threat_analyzer.get_escape_direction(
            (self.enemy.grid_x, self.enemy.grid_y),
            explosion_manager
        )

        # 如果有危险且能逃离，先逃离
        if escape_dir:
            return escape_dir

        # 如果玩家在范围内，追踪玩家
        if self._can_chase(player):
            path = self.pathfinder.find_path(
                (self.enemy.grid_x, self.enemy.grid_y),
                (player.grid_x, player.grid_y),
                avoid_bombs=True
            )

            if path and len(path) > 1:
                next_tile = path[1]
                dx = next_tile[0] - self.enemy.grid_x
                dy = next_tile[1] - self.enemy.grid_y
                return Vector2(dx, dy).normalize()

        # 否则随机移动
        return self._get_random_direction()

    def _can_chase(self, player) -> bool:
        """检查是否可以追踪玩家"""
        if not player or not player.alive:
            return False

        dx = abs(self.enemy.grid_x - player.grid_x)
        dy = abs(self.enemy.grid_y - player.grid_y)

        # 检查是否在追踪范围内
        if hasattr(self.enemy, 'chase_range'):
            return dx + dy <= self.enemy.chase_range
        return dx + dy <= 6

    def _get_random_direction(self) -> Vector2:
        """获取随机可用方向"""
        directions = [Vector2(0, -1), Vector2(0, 1), Vector2(-1, 0), Vector2(1, 0)]

        for direction in directions:
            test_x = self.enemy.grid_x + int(direction.x)
            test_y = self.enemy.grid_y + int(direction.y)

            if self.grid.is_empty(test_x, test_y):
                return direction

        return Vector2(0, 0)
