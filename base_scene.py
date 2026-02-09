"""
场景基类模块
《经典炸弹人》复刻版
"""

from typing import Optional
import pygame

from constants import GameState


class BaseScene:
    """场景基类"""

    def __init__(self, game):
        self.game = game
        self.next_state: Optional[str] = None

    def enter(self):
        """进入场景时调用"""
        pass

    def exit(self):
        """退出场景时调用"""
        pass

    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        pass

    def update(self, dt: float):
        """更新场景状态"""
        pass

    def render(self, surface: pygame.Surface):
        """渲染场景"""
        pass

    def set_next_state(self, state: str):
        """设置下一个状态"""
        self.next_state = state
