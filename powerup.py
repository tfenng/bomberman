"""
道具系统模块
《经典炸弹人》复刻版
"""

from typing import Optional, List, Callable
from enum import Enum
import pygame

from constants import (
    PowerupType, POWERUP_SIZE, POWERUP_FIRE_COLOR,
    POWERUP_BOMB_COLOR, POWERUP_SPEED_COLOR, WHITE, TILE_SIZE
)
from helpers import Timer, Cooldown


class Powerup:
    """道具类"""

    def __init__(self, powerup_type: str, grid_x: int, grid_y: int):
        self.type = powerup_type
        self.grid_x = grid_x
        self.grid_y = grid_y

        # 计算像素位置
        self.x = grid_x * TILE_SIZE + TILE_SIZE // 2
        self.y = grid_y * TILE_SIZE + TILE_SIZE // 2

        # 动画状态
        self.animation_offset = 0.0
        self.collected = False

        # 获取道具颜色
        self.color = self._get_color()

    def _get_color(self):
        """获取道具颜色"""
        color_map = {
            PowerupType.FIRE_INCREASE: POWERUP_FIRE_COLOR,
            PowerupType.BOMB_INCREASE: POWERUP_BOMB_COLOR,
            PowerupType.SPEED_INCREASE: POWERUP_SPEED_COLOR
        }
        return color_map.get(self.type, (128, 128, 128))

    def _get_symbol(self) -> str:
        """获取道具符号"""
        symbol_map = {
            PowerupType.FIRE_INCREASE: "F",
            PowerupType.BOMB_INCREASE: "B",
            PowerupType.SPEED_INCREASE: "S"
        }
        return symbol_map.get(self.type, "?")

    def update(self, dt: float):
        """更新道具状态"""
        self.animation_offset += dt * 5
        if self.animation_offset > 2 * 3.14159:
            self.animation_offset -= 2 * 3.14159

    def render(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """渲染道具"""
        if self.collected:
            return

        # 计算浮动效果
        float_offset = 3 * self.animation_offset / (2 * 3.14159)

        # 计算绘制位置
        center_x = self.x + offset_x
        center_y = self.y + offset_y - float_offset

        # 绘制阴影
        shadow_rect = pygame.Rect(
            center_x - POWERUP_SIZE // 2,
            center_y + POWERUP_SIZE // 2 + 2,
            POWERUP_SIZE,
            POWERUP_SIZE // 4
        )
        shadow_alpha = int(100 * (1 - float_offset / 3))
        shadow_color = (0, 0, 0)
        pygame.draw.rect(surface, shadow_color, shadow_rect)

        # 绘制道具主体
        rect = pygame.Rect(
            center_x - POWERUP_SIZE // 2,
            center_y - POWERUP_SIZE // 2,
            POWERUP_SIZE,
            POWERUP_SIZE
        )
        pygame.draw.rect(surface, self.color, rect)

        # 绘制边框
        pygame.draw.rect(surface, WHITE, rect, 2)

        # 绘制符号
        font = pygame.font.SysFont("arial", 16, bold=True)
        text = font.render(self._get_symbol(), True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)

        # 绘制发光效果
        glow_rect = rect.inflate(6, 6)
        glow_color = list(self.color) + [100]
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=4)
        surface.blit(glow_surface, glow_rect)

    def get_rect(self) -> pygame.Rect:
        """获取碰撞矩形"""
        return pygame.Rect(
            self.grid_x * TILE_SIZE,
            self.grid_y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

    def collect(self):
        """收集道具"""
        self.collected = True


class PowerupEffect:
    """道具效果类"""

    def __init__(self, effect_type: str, duration: float = 0):
        self.type = effect_type
        self.duration = duration
        self.timer = Timer(duration) if duration > 0 else None
        self.active = True

        # 效果参数
        self.fire_bonus = 0
        self.bomb_bonus = 0
        self.speed_multiplier = 1.0

        self._apply_effect()

    def _apply_effect(self):
        """应用效果"""
        if self.type == PowerupType.FIRE_INCREASE:
            self.fire_bonus = 1
        elif self.type == PowerupType.BOMB_INCREASE:
            self.bomb_bonus = 1
        elif self.type == PowerupType.SPEED_INCREASE:
            self.speed_multiplier = 1.2

    def update(self, dt: float) -> bool:
        """更新效果状态，返回是否仍然有效"""
        if self.timer:
            self.timer.update(dt)
            if self.timer.elapsed >= self.timer.duration:
                self.active = False
                self._remove_effect()
        return self.active

    def _remove_effect(self):
        """移除效果"""
        if self.type == PowerupType.FIRE_INCREASE:
            self.fire_bonus = 0
        elif self.type == PowerupType.BOMB_INCREASE:
            self.bomb_bonus = 0
        elif self.type == PowerupType.SPEED_INCREASE:
            self.speed_multiplier = 1.0


class PowerupManager:
    """道具管理器"""

    def __init__(self):
        self._powerups: List[Powerup] = []
        self._active_effects: List[PowerupEffect] = []

    def create_powerup(self, powerup_type: str, grid_x: int, grid_y: int) -> Powerup:
        """创建道具"""
        powerup = Powerup(powerup_type, grid_x, grid_y)
        self._powerups.append(powerup)
        return powerup

    def remove_powerup(self, powerup: Powerup):
        """移除道具"""
        if powerup in self._powerups:
            self._powerups.remove(powerup)

    def get_powerup_at(self, grid_x: int, grid_y: int) -> Optional[Powerup]:
        """获取指定位置的道具"""
        for powerup in self._powerups:
            if powerup.grid_x == grid_x and powerup.grid_y == grid_y and not powerup.collected:
                return powerup
        return None

    def add_effect(self, powerup: Powerup) -> Optional[PowerupEffect]:
        """添加道具效果"""
        if powerup.collected:
            return None

        powerup.collect()
        effect = PowerupEffect(powerup.type)
        self._active_effects.append(effect)
        return effect

    def update(self, dt: float):
        """更新所有道具和效果"""
        # 更新道具
        for powerup in self._powerups[:]:
            powerup.update(dt)
            if powerup.collected:
                self._powerups.remove(powerup)

        # 更新效果
        for effect in self._active_effects[:]:
            effect.update(dt)
            if not effect.active:
                self._active_effects.remove(effect)

    def render(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """渲染所有道具"""
        for powerup in self._powerups:
            powerup.render(surface, offset_x, offset_y)

    def get_total_bonus(self) -> dict:
        """获取所有效果的总加成"""
        total = {
            "fire_bonus": 0,
            "bomb_bonus": 0,
            "speed_multiplier": 1.0
        }

        for effect in self._active_effects:
            total["fire_bonus"] += effect.fire_bonus
            total["bomb_bonus"] += effect.bomb_bonus
            total["speed_multiplier"] *= effect.speed_multiplier

        return total

    def clear(self):
        """清空所有道具和效果"""
        self._powerups.clear()
        self._active_effects.clear()


def get_random_powerup_type() -> str:
    """获取随机道具类型"""
    import random
    return random.choice([
        PowerupType.FIRE_INCREASE,
        PowerupType.BOMB_INCREASE,
        PowerupType.SPEED_INCREASE
    ])
