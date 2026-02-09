"""
敌人实体模块
《经典炸弹人》复刻版
"""

from typing import Optional, Tuple
import pygame
from pygame.math import Vector2

from constants import (
    ENEMY_SIZE, ENEMY_BASIC_COLOR, ENEMY_CHASE_COLOR,
    Direction, CollisionType, WHITE, BLACK, EnemyType
)
from helpers import Cooldown, random_choice_excluding
from collision import CollisionSystem
from grid import Grid
from explosion import ExplosionManager
from player import Player


class EnemyState:
    """敌人状态枚举"""

    IDLE = "idle"
    MOVING = "moving"
    CHASING = "chasing"
    CONFUSED = "confused"
    DEAD = "dead"


class Enemy:
    """敌人基类"""

    def __init__(
        self,
        enemy_type: str,
        grid_x: int,
        grid_y: int,
        speed: float = 100.0,
        collision_system: Optional[CollisionSystem] = None
    ):
        self.type = enemy_type
        self.state = EnemyState.IDLE

        # 网格位置
        self.grid_x = grid_x
        self.grid_y = grid_y

        # 像素位置
        self.position = pygame.math.Vector2(0, 0)

        # 移动速度
        self.speed = speed
        self.velocity = pygame.math.Vector2(0, 0)

        # 大小
        self.size = ENEMY_SIZE
        self.radius = ENEMY_SIZE // 2 - 6  # 进一步减小碰撞半径，避免粘墙

        # 碰撞系统
        self.collision = collision_system

        # 方向
        self.direction = Vector2(0, 0)
        self.next_direction = Vector2(0, 0)

        # 移动计时器
        self.move_timer = 0.0
        self.move_interval = 0.5  # 移动决策间隔

        # 存活状态
        self.alive = True

        # 动画
        self.animation_frame = 0
        self.animation_timer = 0

        # 初始化位置
        self._update_pixel_position()

        # 颜色
        self.color = self._get_color()

    def _get_color(self):
        """获取敌人颜色"""
        if self.type == EnemyType.CHASE:
            return ENEMY_CHASE_COLOR
        return ENEMY_BASIC_COLOR

    def set_collision_system(self, collision_system: CollisionSystem):
        """设置碰撞系统"""
        self.collision = collision_system

    def set_position(self, grid_x: int, grid_y: int):
        """设置敌人位置"""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self._update_pixel_position()

    def _update_pixel_position(self):
        """更新像素位置"""
        if self.collision:
            self.position = pygame.math.Vector2(
                self.collision.get_tile_center(self.grid_x, self.grid_y)
            )

    def get_speed(self) -> float:
        """获取当前速度"""
        return self.speed

    def update(
        self,
        dt: float,
        grid: Grid,
        player: Optional[Player],
        explosion_manager: ExplosionManager
    ):
        """更新敌人状态"""
        if not self.alive:
            return

        # 更新移动计时器
        self.move_timer += dt

        # 更新动画
        self.animation_timer += dt
        if self.animation_timer >= 0.15:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4

        # 获取移动方向
        self.direction = self._get_movement_direction(grid, player)

        # 执行移动
        if self.direction.length() > 0:
            self._move(dt, grid)
            self.state = EnemyState.MOVING if self.type == EnemyType.BASIC else EnemyState.CHASING
        else:
            self.state = EnemyState.IDLE

        # 检查与爆炸的碰撞
        self._check_explosion_collision(explosion_manager)

    def _get_movement_direction(
        self,
        grid: Grid,
        player: Optional[Player]
    ) -> Vector2:
        """获取移动方向（子类重写）"""
        return Vector2(0, 0)

    def _move(self, dt: float, grid: Grid):
        """执行移动"""
        if not self.collision:
            return

        # 持续尝试移动，直到成功或尝试完所有方向
        max_attempts = 4
        for attempt in range(max_attempts):
            actual_speed = self.speed * dt
            move_vector = self.direction * actual_speed

            if move_vector.length() == 0:
                break

            move_vector = move_vector.normalize() * actual_speed

            # 解决碰撞
            new_x, new_y, normal = self.collision.resolve_collision(
                (self.position.x, self.position.y),
                move_vector,
                self.radius
            )

            # 检查是否成功移动（目标位置和当前位置不同）
            moved_dist = ((new_x - self.position.x) ** 2 + (new_y - self.position.y) ** 2) ** 0.5

            if moved_dist > actual_speed * 0.5:
                # 成功移动
                self.position.x = new_x
                self.position.y = new_y
                # 更新网格位置
                new_grid_x, new_grid_y = self.collision.pixel_to_tile(self.position.x, self.position.y)
                if grid.is_valid_grid(new_grid_x, new_grid_y):
                    self.grid_x = new_grid_x
                    self.grid_y = new_grid_y
                break
            else:
                # 移动失败，尝试新方向
                new_dir = self._get_random_direction(grid)
                if new_dir.length() > 0:
                    self.direction = new_dir
                # 如果尝试完所有方向还是不行，就停下来
                if attempt == max_attempts - 1:
                    break

    def _check_explosion_collision(self, explosion_manager: ExplosionManager):
        """检查与爆炸的碰撞"""
        if self.collision:
            offset_x = self.collision.grid.offset_x
            offset_y = self.collision.grid.offset_y
        else:
            offset_x = 0
            offset_y = 0

        if explosion_manager.check_any_hit_position(
            self.position.x, self.position.y, self.radius * 0.8, offset_x, offset_y
        ):
            self.die()
            # 播放敌人死亡音效
            from assets import assets
            assets.play_sound("enemy_die")

    def check_player_collision(self, player: Player) -> bool:
        """检查与玩家的碰撞"""
        if not self.alive or not player.alive:
            return False

        return self.collision.check_entity_collision(
            (self.position.x, self.position.y),
            self.radius * 0.8,
            (player.position.x, player.position.y),
            player.radius * 0.8
        )

    def die(self):
        """敌人死亡"""
        if self.alive:
            self.alive = False
            self.state = EnemyState.DEAD

    def render(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """渲染敌人"""
        if not self.alive:
            return

        # 敌人位置已包含偏移量，无需再次添加
        draw_x = self.position.x
        draw_y = self.position.y

        # 绘制阴影
        shadow_radius = int(self.radius * 0.7)
        pygame.draw.circle(
            surface, (0, 0, 0, 60),
            (draw_x, draw_y + 3), shadow_radius
        )

        # 绘制身体
        pygame.draw.circle(surface, self.color, (draw_x, draw_y), self.radius)

        # 绘制边框
        pygame.draw.circle(surface, WHITE, (draw_x, draw_y), self.radius, 2)

        # 绘制眼睛
        eye_offset = 5
        eye_radius = 4

        # 左眼
        pygame.draw.circle(surface, WHITE, (draw_x - eye_offset, draw_y - 2), eye_radius)
        pygame.draw.circle(surface, BLACK, (draw_x - eye_offset + 1, draw_y - 2), 2)

        # 右眼
        pygame.draw.circle(surface, WHITE, (draw_x + eye_offset, draw_y - 2), eye_radius)
        pygame.draw.circle(surface, BLACK, (draw_x + eye_offset + 1, draw_y - 2), 2)

        # 绘制嘴巴（根据状态）
        mouth_y = draw_y + 6
        if self.state == EnemyState.CHASING:
            # 张嘴
            pygame.draw.circle(surface, BLACK, (draw_x, mouth_y + 2), 5)
        else:
            # 闭嘴
            pygame.draw.line(surface, BLACK, (draw_x - 4, mouth_y), (draw_x + 4, mouth_y), 2)

        # 绘制移动方向指示器
        if self.direction.length() > 0:
            indicator_length = self.radius + 6
            end_x = draw_x + self.direction.x * indicator_length
            end_y = draw_y + self.direction.y * indicator_length
            pygame.draw.line(
                surface, (255, 150, 150),
                (draw_x, draw_y), (end_x, end_y), 2
            )

    def get_rect(self) -> pygame.Rect:
        """获取碰撞矩形"""
        return pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )


class BasicEnemy(Enemy):
    """基础敌人（随机移动）"""

    def __init__(
        self,
        grid_x: int,
        grid_y: int,
        speed: float = 1.5,
        collision_system: Optional[CollisionSystem] = None
    ):
        super().__init__(
            EnemyType.BASIC,
            grid_x, grid_y,
            speed,
            collision_system
        )

    def _get_movement_direction(self, grid: Grid, player: Optional[Player]) -> Vector2:
        """获取随机移动方向"""
        # 定期改变方向
        self.move_timer += 0.016  # 约60fps
        if self.move_timer >= 0.5:
            self.move_timer = 0
            return self._get_random_direction(grid)

        return self.direction

    def _get_random_direction(self, grid: Grid) -> Vector2:
        """获取随机可用方向"""
        directions = [Vector2(0, -1), Vector2(0, 1), Vector2(-1, 0), Vector2(1, 0)]

        # 优先尝试当前方向（保持移动惯性）
        if self.direction.length() > 0:
            test_x = self.grid_x + int(self.direction.x)
            test_y = self.grid_y + int(self.direction.y)
            if grid.is_valid_grid(test_x, test_y) and grid.is_empty(test_x, test_y) and not grid.has_bomb(test_x, test_y):
                return self.direction

        # 随机打乱方向，增加随机性
        import random
        random.shuffle(directions)

        # 尝试找到可用的方向
        for direction in directions:
            test_x = self.grid_x + int(direction.x)
            test_y = self.grid_y + int(direction.y)

            if grid.is_valid_grid(test_x, test_y) and grid.is_empty(test_x, test_y) and not grid.has_bomb(test_x, test_y):
                return direction

        # 如果所有方向都不可用，保持原方向
        return self.direction if self.direction.length() > 0 else Vector2(0, 0)


class ChaseEnemy(Enemy):
    """追踪敌人（追踪玩家）"""

    def __init__(
        self,
        grid_x: int,
        grid_y: int,
        speed: float = 110.0,
        chase_range: int = 5,
        collision_system: Optional[CollisionSystem] = None
    ):
        super().__init__(
            EnemyType.CHASE,
            grid_x, grid_y,
            speed,
            collision_system
        )
        self.chase_range = chase_range
        self.last_player_pos = None
        self.path_timer = 0.0

    def _get_movement_direction(self, grid: Grid, player: Optional[Player]) -> Vector2:
        """获取追踪玩家的方向"""
        if not player:
            return Vector2(0, 0)

        # 检查玩家是否在追踪范围内
        if not self._is_player_in_range(player):
            return self._get_random_direction(grid)

        # 定期更新追踪目标
        self.path_timer += self.move_timer
        if self.path_timer >= 0.3 or not self.last_player_pos:
            self.path_timer = 0
            self.last_player_pos = (player.grid_x, player.grid_y)
            return self._calculate_path_direction(grid, player)

        return self.direction

    def _is_player_in_range(self, player: Player) -> bool:
        """检查玩家是否在追踪范围内"""
        dx = abs(self.grid_x - player.grid_x)
        dy = abs(self.grid_y - player.grid_y)
        return dx + dy <= self.chase_range

    def _calculate_path_direction(self, grid: Grid, player: Player) -> Vector2:
        """计算朝向玩家的方向"""
        # 基于像素位置检查方向是否通畅
        def is_direction_clear(dir: Vector2) -> bool:
            check_dist = self.radius + 10
            test_x = self.position.x + dir.x * check_dist
            test_y = self.position.y + dir.y * check_dist
            gx, gy = grid.pixel_to_grid(test_x, test_y)
            return (grid.is_valid_grid(gx, gy) and
                    grid.is_empty(gx, gy) and
                    not grid.has_bomb(gx, gy))

        # 简单的方向计算
        dx = player.grid_x - self.grid_x
        dy = player.grid_y - self.grid_y

        # 优先移动距离较大的方向
        directions = []
        if abs(dx) > abs(dy):
            # 优先水平移动
            if dx != 0:
                directions.append(Vector2(1 if dx > 0 else -1, 0))
            if dy != 0:
                directions.append(Vector2(0, 1 if dy > 0 else -1))
        else:
            # 优先垂直移动
            if dy != 0:
                directions.append(Vector2(0, 1 if dy > 0 else -1))
            if dx != 0:
                directions.append(Vector2(1 if dx > 0 else -1, 0))

        # 按优先级尝试方向
        for direction in directions:
            if is_direction_clear(direction):
                return direction

        # 如果首选方向被阻挡，尝试所有可用方向
        all_dirs = [Vector2(0, -1), Vector2(0, 1), Vector2(-1, 0), Vector2(1, 0)]
        for direction in all_dirs:
            if is_direction_clear(direction):
                return direction

        return Vector2(0, 0)

    def _get_random_direction(self, grid: Grid) -> Vector2:
        """获取随机可用方向"""
        directions = [Vector2(0, -1), Vector2(0, 1), Vector2(-1, 0), Vector2(1, 0)]

        # 随机打乱方向
        import random
        random.shuffle(directions)

        for direction in directions:
            # 检查前方格子是否为空（基于网格坐标）
            test_x = self.grid_x + int(direction.x)
            test_y = self.grid_y + int(direction.y)
            if (grid.is_valid_grid(test_x, test_y) and
                grid.is_empty(test_x, test_y) and
                not grid.has_bomb(test_x, test_y)):
                return direction

        # 如果所有方向都被阻挡，保持当前方向（让碰撞解决来处理）
        return self.direction if self.direction.length() > 0 else directions[0]
