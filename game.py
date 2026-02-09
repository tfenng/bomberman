"""
游戏主循环模块
《经典炸弹人》复刻版
"""

from typing import Dict, Optional
import pygame
import sys

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS, GameState
)
from base_scene import BaseScene
from menu_scene import MenuScene
from game_scene import GameScene
from result_scene import ResultScene


class Game:
    """游戏主类"""

    def __init__(self):
        # 初始化 Pygame
        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)

        # 创建窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # 游戏状态
        self.running = True
        self.current_state: Optional[BaseScene] = None
        self.scenes: Dict[str, BaseScene] = {}

        # 初始化场景
        self._init_scenes()

        # 设置初始场景
        self.change_state(GameState.MENU)

    def _init_scenes(self):
        """初始化所有场景"""
        self.scenes = {
            GameState.MENU: MenuScene(self),
            GameState.PLAYING: GameScene(self),
            GameState.GAME_OVER: ResultScene(self, "game_over"),
            GameState.VICTORY: ResultScene(self, "victory")
        }

    def change_state(self, state: str):
        """切换游戏状态"""
        # 退出当前场景
        if self.current_state:
            self.current_state.exit()

        # 切换到新场景
        self.current_state = self.scenes.get(state)
        if self.current_state:
            self.current_state.enter()

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # 处理当前场景的事件
            if self.current_state:
                self.current_state.handle_event(event)

            # 检查状态切换
            if self.current_state and self.current_state.next_state:
                next_state = self.current_state.next_state
                self.current_state.next_state = None
                self.change_state(next_state)

    def update(self):
        """更新游戏状态"""
        dt = self.clock.get_time() / 1000.0  # 转换为秒

        # 获取按键状态并传递给游戏场景
        if self.current_state and hasattr(self.current_state, 'handle_key_state'):
            keys = pygame.key.get_pressed()
            self.current_state.handle_key_state(keys)

        # 更新当前场景
        if self.current_state:
            self.current_state.update(dt)

        # 检查状态切换
        if self.current_state and self.current_state.next_state:
            next_state = self.current_state.next_state
            self.current_state.next_state = None
            self.change_state(next_state)

    def render(self):
        """渲染游戏"""
        # 清除屏幕
        self.screen.fill((0, 0, 0))

        # 渲染当前场景
        if self.current_state:
            self.current_state.render(self.screen)

        # 刷新显示
        pygame.display.flip()

    def run(self):
        """运行游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()

            # 控制帧率
            self.clock.tick(FPS)

        self._cleanup()

    def _cleanup(self):
        """清理资源"""
        pygame.quit()
        sys.exit()
