"""
辅助函数模块
《经典炸弹人》复刻版
"""

import math
import random
from typing import Tuple, Optional, List

import pygame
from pygame.math import Vector2


def clamp(value: float, min_value: float, max_value: float) -> float:
    """将值限制在指定范围内"""
    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, t: float) -> float:
    """线性插值"""
    return start + (end - start) * t


def normalize_vector(vector: Vector2) -> Vector2:
    """标准化向量"""
    length = vector.length()
    if length == 0:
        return Vector2(0, 0)
    return vector / length


def distance_squared(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """计算两点之间的平方距离"""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return dx * dx + dy * dy


def distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """计算两点之间的欧几里得距离"""
    return math.sqrt(distance_squared(pos1, pos2))


def rect_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """检测两个矩形是否碰撞"""
    return rect1.colliderect(rect2)


def circle_rect_collision(
    circle_pos: Tuple[float, float],
    circle_radius: float,
    rect: pygame.Rect
) -> bool:
    """检测圆形与矩形的碰撞"""
    # 找到矩形上距离圆心最近的点
    closest_x = clamp(circle_pos[0], rect.left, rect.right)
    closest_y = clamp(circle_pos[1], rect.top, rect.bottom)

    # 计算圆心到最近点的距离
    distance_x = circle_pos[0] - closest_x
    distance_y = circle_pos[1] - closest_y

    # 如果距离小于半径，则发生碰撞
    return (distance_x * distance_x + distance_y * distance_y) < (circle_radius * circle_radius)


def circle_collision(
    pos1: Tuple[float, float],
    radius1: float,
    pos2: Tuple[float, float],
    radius2: float
) -> bool:
    """检测两个圆形是否碰撞"""
    return distance_squared(pos1, pos2) < (radius1 + radius2) ** 2


def random_choice_excluding(choices: List, exclude: any) -> any:
    """从列表中随机选择一个元素，排除指定元素"""
    filtered = [c for c in choices if c != exclude]
    if not filtered:
        return choices[0] if choices else None
    return random.choice(filtered)


def get_random_direction() -> Vector2:
    """获取随机方向"""
    directions = [Vector2(0, -1), Vector2(0, 1), Vector2(-1, 0), Vector2(1, 0)]
    return random.choice(directions)


def format_time(seconds: float) -> str:
    """格式化时间为 MM:SS 格式"""
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes:02d}:{secs:02d}"


def load_json(filepath: str) -> dict:
    """加载JSON文件"""
    import json
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def scale_color(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """缩放颜色亮度"""
    return tuple(int(clamp(c * factor, 0, 255)) for c in color)


def create_pulse_alpha(
    surface: pygame.Surface,
    base_alpha: int = 128,
    pulse_range: int = 127,
    speed: float = 3.0
) -> pygame.Surface:
    """创建带脉冲效果的半透明表面"""
    # 创建带有 alpha 通道的副本
    new_surface = surface.copy()
    new_surface.set_alpha(base_alpha)

    # 简单脉冲效果（实际应用中可以在 update 中动态调整）
    return new_surface


class Timer:
    """简单计时器类"""

    def __init__(self, duration: float):
        self.duration = duration
        self.elapsed = 0.0
        self.paused = False

    def update(self, dt: float) -> bool:
        """更新计时器，返回是否超时"""
        if not self.paused:
            self.elapsed += dt
        return self.elapsed >= self.duration

    def reset(self):
        """重置计时器"""
        self.elapsed = 0.0

    def pause(self):
        """暂停计时器"""
        self.paused = True

    def resume(self):
        """恢复计时器"""
        self.paused = False

    def get_progress(self) -> float:
        """获取进度 (0.0 - 1.0)"""
        if self.duration <= 0:
            return 1.0
        return min(self.elapsed / self.duration, 1.0)

    def time_remaining(self) -> float:
        """获取剩余时间"""
        return max(0.0, self.duration - self.elapsed)


class Cooldown:
    """冷却时间类"""

    def __init__(self, cooldown_time: float):
        self.cooldown_time = cooldown_time
        self.current_cooldown = 0.0

    def update(self, dt: float) -> bool:
        """更新冷却，返回是否可以使用"""
        if self.current_cooldown > 0:
            self.current_cooldown -= dt
            return False
        return True

    def use(self):
        """使用后开始冷却"""
        self.current_cooldown = self.cooldown_time

    def reset(self):
        """重置冷却"""
        self.current_cooldown = 0.0

    def get_remaining(self) -> float:
        """获取剩余冷却时间"""
        return max(0.0, self.current_cooldown)

    def is_ready(self) -> bool:
        """检查是否可以使用"""
        return self.current_cooldown <= 0
