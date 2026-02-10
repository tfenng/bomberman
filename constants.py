"""
游戏常量定义
《经典炸弹人》复刻版
"""

from pygame.math import Vector2

# ============ 屏幕设置 ============
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "经典炸弹人 - Boomer"
FPS = 60

# ============ 颜色定义 ============
# 基础颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GREEN = (60, 200, 60)
BLUE = (60, 100, 220)
YELLOW = (240, 200, 60)
ORANGE = (255, 140, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# 游戏实体颜色
PLAYER_COLOR = (60, 140, 220)  # 蓝色玩家
ENEMY_BASIC_COLOR = (220, 80, 80)  # 红色敌人
ENEMY_CHASE_COLOR = (180, 60, 180)  # 紫色追踪敌人
BOMB_COLOR = (40, 40, 40)  # 深色炸弹
BOMB_CORE_COLOR = (255, 80, 0)  # 炸弹核心
EXPLOSION_COLOR = (255, 120, 0)  # 橙红色爆炸

# 地形颜色
HARD_WALL_COLOR = (80, 80, 90)  # 深灰色硬墙
SOFT_WALL_COLOR = (160, 100, 60)  # 棕色软墙
GROUND_COLOR = (100, 180, 100)  # 浅绿色地面
EXIT_COLOR = (100, 200, 255)  # 出口发光色

# 道具颜色
POWERUP_FIRE_COLOR = (255, 80, 0)  # 火焰道具 - 红色
POWERUP_BOMB_COLOR = (60, 60, 60)  # 炸弹道具 - 黑色
POWERUP_SPEED_COLOR = (255, 220, 0)  # 速度道具 - 黄色

# UI颜色
UI_BG_COLOR = (40, 40, 50)
UI_TEXT_COLOR = (220, 220, 220)
UI_HIGHLIGHT_COLOR = (255, 180, 60)

# ============ 地图设置 ============
GRID_WIDTH = 13
GRID_HEIGHT = 11
TILE_SIZE = 48
MAP_OFFSET_X = (SCREEN_WIDTH - GRID_WIDTH * TILE_SIZE) // 2
MAP_OFFSET_Y = (SCREEN_HEIGHT - GRID_HEIGHT * TILE_SIZE) // 2

# ============ 玩家设置 ============
PLAYER_SIZE = 36
PLAYER_SPEED_DEFAULT = 150.0
PLAYER_SPEED_MIN = 100.0
PLAYER_SPEED_MAX = 250.0

# ============ 敌人设置 ============
ENEMY_SIZE = 32
ENEMY_BASIC_SPEED = 1.5
ENEMY_CHASE_SPEED = 1.2
ENEMY_CHASE_RANGE = 5

# ============ 炸弹设置 ============
BOMB_SIZE = 32
BOMB_FUSE_TIME = 2.0  # 爆炸倒计时（秒）
BOMB_ANIMATION_SPEED = 0.1  # 动画帧间隔
EXPLOSION_DURATION = 0.3  # 爆炸持续时间（秒）
INITIAL_BOMB_POWER = 1
INITIAL_BOMB_COUNT = 1
MAX_BOMB_POWER = 4
MAX_BOMB_COUNT = 3

# ============ 道具设置 ============
POWERUP_SIZE = 24
POWERUP_DROP_RATE = 0.5  # 软墙破坏后掉落概率
POWERUP_DURATION = 8.0  # 持续型道具持续时间

# ============ 游戏状态 ============
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"

# ============ 方向定义 ============
class Direction:
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    NONE = Vector2(0, 0)

    @staticmethod
    def all_directions():
        return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

# ============ 瓦片类型 ============
class TileType:
    EMPTY = 0
    HARD_WALL = 1
    SOFT_WALL = 2
    EXIT = 3


# ============ 地图字符常量 ============
class TileChar:
    """地图文件字符映射"""
    HARD_WALL = '#'  # 硬墙 (不可破坏)
    SOFT_WALL = '.'  # 软墙 (可破坏)
    EMPTY = ' '      # 空地
    PLAYER = '@'     # 玩家出生点
    EXIT = 'X'       # 出口

# ============ 道具类型 ============
class PowerupType:
    FIRE_INCREASE = "fire_increase"  # +1 爆炸范围
    BOMB_INCREASE = "bomb_increase"  # +1 可放置炸弹数
    SPEED_INCREASE = "speed_increase"  # +20% 移动速度

# ============ 敌人类型 ============
class EnemyType:
    BASIC = "basic"  # 随机移动
    CHASE = "chase"  # 追踪玩家

# ============ 碰撞类型 ============
class CollisionType:
    NONE = 0
    WALL = 1
    BOMB = 2
    ENEMY = 3
    EXPLOSION = 4
    POWERUP = 5
    EXIT = 6
