"""
结果场景模块
《经典炸弹人》复刻版
"""

import pygame

from constants import (
    GameState, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK,
    UI_BG_COLOR, UI_TEXT_COLOR, UI_HIGHLIGHT_COLOR
)
from base_scene import BaseScene
from fonts import font_manager


class ResultScene(BaseScene):
    """结果场景（用于显示游戏结果）"""

    def __init__(self, game, result_type: str = "victory"):
        super().__init__(game)
        self.result_type = result_type

        # 字体
        self.title_font = font_manager.get_font(size=64, bold=True)
        self.stats_font = font_manager.get_font(size=28)
        self.hint_font = font_manager.get_font(size=20)

        # 统计数据
        self.stats = {
            "enemies_killed": 0,
            "total_enemies": 0,
            "time_elapsed": 0.0,
            "powerups_collected": 0
        }

    def set_stats(self, **kwargs):
        """设置统计数据"""
        self.stats.update(kwargs)

    def enter(self):
        """进入结果场景"""
        pass

    def handle_event(self, event: pygame.event.Event):
        """处理结果场景事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.set_next_state(GameState.MENU)
            elif event.key == pygame.K_r:
                self.set_next_state(GameState.PLAYING)

    def update(self, dt: float):
        """更新结果场景"""
        pass

    def render(self, surface: pygame.Surface):
        """渲染结果场景"""
        # 背景
        if self.result_type == "victory":
            bg_color = (40, 80, 40)
        else:
            bg_color = (80, 40, 40)
        surface.fill(bg_color)

        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        surface.blit(overlay, (0, 0))

        # 标题
        if self.result_type == "victory":
            title = self.title_font.render("胜利!", True, UI_HIGHLIGHT_COLOR)
            subtitle = self.stats_font.render("恭喜你通过了关卡!", True, WHITE)
        else:
            title = self.title_font.render("游戏结束", True, (220, 60, 60))
            subtitle = self.stats_font.render("再接再厉!", True, WHITE)

        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 40))
        surface.blit(title, title_rect)

        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 20))
        surface.blit(subtitle, subtitle_rect)

        # 统计信息
        self._draw_stats(surface)

        # 操作提示
        self._draw_hints(surface)

    def _draw_stats(self, surface: pygame.Surface):
        """绘制统计信息"""
        stats_items = [
            ("消灭敌人", f"{self.stats['enemies_killed']}/{self.stats['total_enemies']}"),
            ("通关时间", f"{self.stats['time_elapsed']:.1f} 秒"),
            ("收集道具", f"{self.stats['powerups_collected']}")
        ]

        start_y = SCREEN_HEIGHT // 2 + 60
        for i, (label, value) in enumerate(stats_items):
            y = start_y + i * 45

            label_text = self.stats_font.render(label + ":", True, WHITE)
            value_text = self.stats_font.render(value, True, UI_HIGHLIGHT_COLOR)

            surface.blit(label_text, (SCREEN_WIDTH // 2 - 150, y))
            surface.blit(value_text, (SCREEN_WIDTH // 2 + 50, y))

    def _draw_hints(self, surface: pygame.Surface):
        """绘制操作提示"""
        hints = [
            "按 回车键 或 空格键 返回菜单",
            "按 R 重新开始"
        ]

        start_y = SCREEN_HEIGHT - 80
        for i, hint in enumerate(hints):
            text = self.hint_font.render(hint, True, (180, 180, 180))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 25))
            surface.blit(text, text_rect)
