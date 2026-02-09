"""
游戏界面模块
《经典炸弹人》复刻版
"""

from typing import Optional
import pygame

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, UI_BG_COLOR,
    UI_TEXT_COLOR, UI_HIGHLIGHT_COLOR,
    POWERUP_FIRE_COLOR, POWERUP_BOMB_COLOR, POWERUP_SPEED_COLOR,
    PLAYER_COLOR, ENEMY_BASIC_COLOR
)
from fonts import font_manager


class HUD:
    """游戏界面类"""

    def __init__(self):
        self.font = font_manager.get_font(size=20, bold=True)
        self.title_font = font_manager.get_font(size=24, bold=True)

    def draw(
        self,
        surface: pygame.Surface,
        player_alive: bool = True,
        enemies_remaining: int = 0,
        total_enemies: int = 0,
        time_elapsed: float = 0.0,
        bomb_count: int = 0,
        bomb_max: int = 1,
        bomb_power: int = 1,
        powerups_collected: int = 0
    ):
        """绘制游戏HUD"""
        # 顶部栏
        self._draw_top_bar(
            surface,
            player_alive,
            enemies_remaining,
            total_enemies,
            time_elapsed
        )

        # 底部状态栏
        self._draw_status_bar(
            surface,
            bomb_count,
            bomb_max,
            bomb_power,
            powerups_collected
        )

    def _draw_top_bar(
        self,
        surface: pygame.Surface,
        player_alive: bool,
        enemies_remaining: int,
        total_enemies: int,
        time_elapsed: float
    ):
        """绘制顶部栏"""
        # 背景
        pygame.draw.rect(surface, UI_BG_COLOR, (0, 0, SCREEN_WIDTH, 50))

        # 分割线
        pygame.draw.line(surface, (80, 80, 90), (0, 50), (SCREEN_WIDTH, 50), 2)

        # 玩家状态
        if player_alive:
            status_text = "存活"
            status_color = (100, 255, 100)
        else:
            status_text = "死亡"
            status_color = (255, 100, 100)

        status = self.font.render(f"状态: {status_text}", True, status_color)
        surface.blit(status, (20, 12))

        # 敌人数量
        enemy_text = self.font.render(
            f"敌人: {enemies_remaining}/{total_enemies}",
            True, ENEMY_BASIC_COLOR
        )
        surface.blit(enemy_text, (150, 12))

        # 关卡标题
        level_text = self.title_font.render("第一关 - 迷宫初探", True, UI_TEXT_COLOR)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 25))
        surface.blit(level_text, level_rect)

        # 时间
        time_text = self.font.render(f"时间: {time_elapsed:.1f}s", True, WHITE)
        surface.blit(time_text, (SCREEN_WIDTH - 120, 12))

    def _draw_status_bar(
        self,
        surface: pygame.Surface,
        bomb_count: int,
        bomb_max: int,
        bomb_power: int,
        powerups_collected: int
    ):
        """绘制底部状态栏"""
        # 背景
        bar_height = 60
        pygame.draw.rect(
            surface, UI_BG_COLOR,
            (0, SCREEN_HEIGHT - bar_height, SCREEN_WIDTH, bar_height)
        )

        # 分割线
        pygame.draw.line(
            surface, (80, 80, 90),
            (0, SCREEN_HEIGHT - bar_height),
            (SCREEN_WIDTH, SCREEN_HEIGHT - bar_height), 2
        )

        # 炸弹信息
        bomb_text = self.font.render("炸弹", True, UI_TEXT_COLOR)
        surface.blit(bomb_text, (20, SCREEN_HEIGHT - bar_height + 10))

        # 炸弹图标和数量
        bomb_icon_color = POWERUP_BOMB_COLOR
        pygame.draw.circle(surface, bomb_icon_color, (60, SCREEN_HEIGHT - bar_height + 40), 12)
        pygame.draw.circle(surface, BLACK, (60, SCREEN_HEIGHT - bar_height + 40), 12, 1)

        bomb_count_text = self.font.render(f"{bomb_count}/{bomb_max}", True, WHITE)
        surface.blit(bomb_count_text, (80, SCREEN_HEIGHT - bar_height + 25))

        # 火力信息
        fire_text = self.font.render("火力", True, UI_TEXT_COLOR)
        surface.blit(fire_text, (160, SCREEN_HEIGHT - bar_height + 10))

        # 火力图标
        fire_icon_color = POWERUP_FIRE_COLOR
        fire_rect = pygame.Rect(200, SCREEN_HEIGHT - bar_height + 28, 24, 24)
        pygame.draw.rect(surface, fire_icon_color, fire_rect)
        pygame.draw.rect(surface, WHITE, fire_rect, 2)

        # 绘制火焰符号
        for i in range(bomb_power):
            x = 205 + i * 18
            y = SCREEN_HEIGHT - bar_height + 32
            pygame.draw.polygon(surface, WHITE, [
                (x + 6, y),
                (x + 12, y + 16),
                (x, y + 16)
            ])

        # 道具收集数
        if powerups_collected > 0:
            powerup_text = self.font.render(f"道具 +{powerups_collected}", True, POWERUP_SPEED_COLOR)
            surface.blit(powerup_text, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - bar_height + 25))

        # 操作提示
        controls = [
            ("WASD/方向键", "移动"),
            ("空格", "放炸弹"),
            ("R", "重新开始"),
            ("ESC", "菜单")
        ]

        x_offset = 280
        for key, action in controls:
            key_text = self.font.render(key, True, UI_HIGHLIGHT_COLOR)
            action_text = self.font.render(action, True, (150, 150, 150))

            surface.blit(key_text, (x_offset, SCREEN_HEIGHT - bar_height + 10))
            surface.blit(action_text, (x_offset + key_text.get_width() + 5, SCREEN_HEIGHT - bar_height + 10))
            x_offset += key_text.get_width() + action_text.get_width() + 30


class PauseMenu:
    """暂停菜单"""

    def __init__(self):
        self.font = font_manager.get_font(size=32, bold=True)
        self.options = ["继续游戏", "重新开始", "返回菜单"]
        self.selected = 0

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理暂停菜单事件，返回选中的操作"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected == 0:
                    return "continue"
                elif self.selected == 1:
                    return "restart"
                elif self.selected == 2:
                    return "menu"
            elif event.key == pygame.K_ESCAPE:
                return "continue"
        return None

    def render(self, surface: pygame.Surface):
        """渲染暂停菜单"""
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))

        # 暂停标题
        title = self.font.render("游戏暂停", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        surface.blit(title, title_rect)

        # 菜单选项
        start_y = SCREEN_HEIGHT // 2
        for i, option in enumerate(self.options):
            y = start_y + i * 50

            if i == self.selected:
                text = self.font.render(f"> {option} <", True, UI_HIGHLIGHT_COLOR)
            else:
                text = self.font.render(option, True, UI_TEXT_COLOR)

            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            surface.blit(text, text_rect)


class GameOverScreen:
    """游戏结束画面"""

    def __init__(self):
        self.font = font_manager.get_font(size=48, bold=True)
        self.hint_font = font_manager.get_font(size=20)

    def render(self, surface: pygame.Surface, victory: bool = False):
        """渲染游戏结束画面"""
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # 标题
        if victory:
            title = self.font.render("胜利!", True, (255, 200, 0))
            subtitle = self.hint_font.render("恭喜你通过了关卡!", True, WHITE)
        else:
            title = self.font.render("游戏结束", True, (220, 60, 60))
            subtitle = self.hint_font.render("继续努力吧!", True, WHITE)

        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        surface.blit(title, title_rect)

        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        surface.blit(subtitle, subtitle_rect)

        # 提示
        hint = self.hint_font.render("按 R 重新开始 | 按 ESC 返回菜单", True, (180, 180, 180))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        surface.blit(hint, hint_rect)
