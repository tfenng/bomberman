"""
实体生成器模块
《经典炸弹人》复刻版
"""

from typing import Dict, List, Optional
import random
import pygame

from constants import EnemyType, PowerupType, TileType
from grid import Grid
from player import Player
from enemy import Enemy, BasicEnemy, ChaseEnemy
from collision import CollisionSystem
from powerup import PowerupManager
from bomb import BombManager
from explosion import ExplosionManager
from assets import assets


class Spawner:
    """实体生成器"""

    def __init__(self, grid: Grid):
        self.grid = grid
        self.collision_system = CollisionSystem(grid)
        self.powerup_manager = PowerupManager()
        self.bomb_manager = BombManager()
        self.explosion_manager = ExplosionManager()

    def spawn_player(
        self,
        grid_x: int,
        grid_y: int,
        player_id: int = 0
    ) -> Player:
        """生成玩家"""
        player = Player(
            grid_x=grid_x,
            grid_y=grid_y,
            player_id=player_id,
            collision_system=self.collision_system
        )
        return player

    def spawn_enemy(
        self,
        enemy_type: str,
        grid_x: int,
        grid_y: int,
        speed: float = 1.5,
        chase_range: int = 5
    ) -> Enemy:
        """生成敌人"""
        if enemy_type == EnemyType.CHASE:
            enemy = ChaseEnemy(
                grid_x=grid_x,
                grid_y=grid_y,
                speed=speed,
                chase_range=chase_range,
                collision_system=self.collision_system
            )
        else:
            enemy = BasicEnemy(
                grid_x=grid_x,
                grid_y=grid_y,
                speed=speed,
                collision_system=self.collision_system
            )
        return enemy

    def spawn_enemies_from_level(self, level_data: Dict) -> List[Enemy]:
        """从关卡数据生成所有敌人"""
        enemies = []
        enemies_data = level_data.get("enemies", [])

        for enemy_data in enemies_data:
            enemy_type = enemy_data.get("type", EnemyType.BASIC)
            col = enemy_data.get("col", 1)
            row = enemy_data.get("row", 1)
            speed = enemy_data.get("speed", 1.5)

            enemy = self.spawn_enemy(
                enemy_type=enemy_type,
                grid_x=col,
                grid_y=row,
                speed=speed
            )
            enemies.append(enemy)

        return enemies

    def spawn_powerup(
        self,
        grid_x: int,
        grid_y: int,
        powerup_type: Optional[str] = None
    ):
        """生成道具"""
        if powerup_type is None:
            powerup_type = get_random_powerup_type()

        return self.powerup_manager.create_powerup(powerup_type, grid_x, grid_y)

    def spawn_powerups_from_soft_walls(
        self,
        level_data: Dict,
        destroyed_walls: List[tuple]
    ) -> List:
        """从被破坏的软墙生成道具"""
        powerups = []

        # 使用 powerup_probabilities 配置，各道具独立概率
        powerup_probs = level_data.get("powerup_probabilities", {
            "bomb_increase": 0.15,
            "speed_increase": 0.15,
            "fire_increase": 0.05,
            "none": 0.65
        })

        for wall_pos in destroyed_walls:
            # 根据概率分布选择结果
            choices = list(powerup_probs.keys())
            weights = list(powerup_probs.values())
            result = random.choices(choices, weights=weights, k=1)[0]

            if result != "none":
                powerup = self.spawn_powerup(wall_pos[0], wall_pos[1], result)
                powerups.append(powerup)

        return powerups

    def create_explosion(
        self,
        grid_x: int,
        grid_y: int,
        power: int
    ):
        """创建爆炸"""
        return self.explosion_manager.create_explosion(
            grid=self.grid,
            center_x=grid_x,
            center_y=grid_y,
            power=power
        )

    def load_level(self, level_name: str = "level_01") -> Dict:
        """加载关卡"""
        level_data = assets.load_level(level_name)

        # 设置网格偏移
        self.collision_system.grid.offset_x = (pygame.display.get_surface().get_width() -
                                               level_data["width"] * level_data["tile_size"]) // 2
        self.collision_system.grid.offset_y = (pygame.display.get_surface().get_height() -
                                               level_data["height"] * level_data["tile_size"]) // 2

        # 更新网格大小
        self.grid.width = level_data["width"]
        self.grid.height = level_data["height"]

        # 加载地图数据
        self.grid.load_from_data(level_data)

        # 设置出口（如果藏在软墙下，需要确保出口位置是软墙）
        exit_data = level_data.get("exit", {})
        exit_x = exit_data.get("col", 11)
        exit_y = exit_data.get("row", 5)
        hidden = exit_data.get("hidden_under_soft_wall", True)

        if hidden:
            # 出口藏在软墙下 - 确保该位置是软墙
            if not self.grid.is_soft_wall(exit_x, exit_y):
                self.grid.add_soft_wall(exit_x, exit_y)
        else:
            # 出口直接显示
            self.grid.set_tile(exit_x, exit_y, TileType.EXIT)

        return level_data


def get_random_powerup_type() -> str:
    """获取随机道具类型"""
    return random.choice([
        PowerupType.FIRE_INCREASE,
        PowerupType.BOMB_INCREASE,
        PowerupType.SPEED_INCREASE
    ])
