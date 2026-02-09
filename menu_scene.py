"""
菜单场景模块
《经典炸弹人》复刻版
"""

import pygame
import math

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLUE,
    UI_BG_COLOR, UI_TEXT_COLOR, UI_HIGHLIGHT_COLOR,
    GameState
)
from base_scene import BaseScene
from assets import assets
from fonts import font_manager


class MenuScene(BaseScene):
    """菜单场景"""

    def __init__(self, game):
        super().__init__(game)

        # 使用支持中文的字体
        self.title_font = font_manager.get_font(size=64, bold=True)
        self.menu_font = font_manager.get_font(size=32)
        self.footer_font = font_manager.get_font(size=20)

        # 选项
        self.options = ["开始游戏", "退出游戏"]
        self.selected_index = 0

        # 动画
        self.title_pulse = 0.0
        self.bomb_animations = []

    def enter(self):
        """进入菜单场景"""
        self.bomb_animations = []
        for i in range(5):
            self.bomb_animations.append({
                "x": 100 + i * 150,
                "y": 400,
                "radius": 20,
                "phase": i * 0.5
            })

    def handle_event(self, event: pygame.event.Event):
        """处理菜单事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_option()
            elif event.key == pygame.K_ESCAPE:
                self.game.running = False

    def _select_option(self):
        """选择菜单选项"""
        if self.selected_index == 0:
            # 开始游戏
            self.set_next_state(GameState.PLAYING)
        elif self.selected_index == 1:
            # 退出游戏
            self.game.running = False

    def update(self, dt: float):
        """更新菜单状态"""
        self.title_pulse += dt * 3

        # 更新炸弹动画
        for anim in self.bomb_animations:
            anim["phase"] += dt * 5

    def render(self, surface: pygame.Surface):
        """渲染菜单"""
        surface.fill(BLUE)

        # 绘制背景网格效果
        self._draw_background_grid(surface)

        # 绘制标题
        self._draw_title(surface)

        # 绘制菜单选项
        self._draw_menu(surface)

        # 绘制底部提示
        self._draw_footer(surface)

    def _draw_background_grid(self, surface: pygame.Surface):
        """绘制背景网格"""
        grid_size = 40
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(surface, (40, 60, 100), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(surface, (40, 60, 100), (0, y), (SCREEN_WIDTH, y), 1)

    def _draw_title(self, surface: pygame.Surface):
        """绘制标题"""
        # 标题抖动效果
        offset_x = int(pygame.math.Vector2(self.title_pulse, 0).x) % 10 - 5
        offset_y = int(pygame.math.Vector2(0, self.title_pulse).y) % 10 - 5

        # 标题阴影
        title_shadow = self.title_font.render("经典炸弹人", True, (0, 0, 0))
        surface.blit(title_shadow, (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + 4 + offset_x,
                                      80 + 4 + offset_y))

        # 标题文字
        pulse_value = int(20 * math.sin(self.title_pulse))
        pulse_color = (
            min(255, UI_HIGHLIGHT_COLOR[0] + pulse_value),
            min(255, UI_HIGHLIGHT_COLOR[1] + pulse_value),
            min(255, UI_HIGHLIGHT_COLOR[2] + pulse_value)
        )

        title = self.title_font.render("经典炸弹人", True, UI_HIGHLIGHT_COLOR)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2 + offset_x,
                             80 + offset_y))

        # 绘制装饰炸弹
        self._draw_decorative_bombs(surface)

    def _draw_decorative_bombs(self, surface: pygame.Surface):
        """绘制装饰炸弹"""
        for anim in self.bomb_animations:
            phase = anim["phase"]
            radius = anim["radius"] + int(math.sin(phase) * 3)

            # 炸弹阴影
            pygame.draw.circle(surface, (0, 0, 0, 80),
                             (anim["x"] + 3, anim["y"] + radius + 3), radius)

            # 炸弹主体
            pygame.draw.circle(surface, (40, 40, 40), (anim["x"], anim["y"]), radius)

            # 炸弹高光
            pygame.draw.circle(surface, (100, 100, 100),
                             (anim["x"] - radius // 3, anim["y"] - radius // 3), radius // 4)

            # 炸弹引信
            fuse_x = anim["x"] + radius // 2
            fuse_y = anim["y"] - radius // 2
            pygame.draw.line(surface, (80, 60, 40),
                           (anim["x"], anim["y"] - radius // 2),
                           (fuse_x, fuse_y - 8), 3)

            # 火花
            spark_offset = (anim["phase"] * 30) % 10
            pygame.draw.circle(surface, (255, 200, 0),
                             (fuse_x + spark_offset, fuse_y - 8), 4)

    def _draw_menu(self, surface: pygame.Surface):
        """绘制菜单选项"""
        start_y = 300

        for i, option in enumerate(self.options):
            y = start_y + i * 60

            if i == self.selected_index:
                # 选中项
                # 高亮背景
                bg_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, y - 10, 240, 50)
                pygame.draw.rect(surface, UI_HIGHLIGHT_COLOR, bg_rect, border_radius=10)

                text = self.menu_font.render(f"> {option} <", True, BLACK)
            else:
                # 未选中项
                text = self.menu_font.render(option, True, UI_TEXT_COLOR)

            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y + 20))
            surface.blit(text, text_rect)

    def _draw_footer(self, surface: pygame.Surface):
        """绘制底部提示"""
        footer = self.footer_font.render("使用 方向键/WASD 移动，空格键确定，ESC 退出", True, WHITE)
        surface.blit(footer, (SCREEN_WIDTH // 2 - footer.get_width() // 2, SCREEN_HEIGHT - 40))
