"""
文本渲染模块
《经典炸弹人》复刻版
"""

import pygame
from typing import Tuple, Optional


class TextRenderer:
    """文本渲染器"""

    _instance: Optional['TextRenderer'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._fonts: dict = {}

    def get_font(self, name: str = "arial", size: int = 24, bold: bool = False) -> pygame.font.Font:
        """获取字体"""
        key = f"{name}_{size}_{bold}"
        if key not in self._fonts:
            self._fonts[key] = pygame.font.SysFont(name, size, bold=bold)
        return self._fonts[key]

    def render_text(
        self,
        text: str,
        size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255),
        bold: bool = False,
        antialias: bool = True
    ) -> pygame.Surface:
        """渲染文本"""
        font = self.get_font(size=size, bold=bold)
        return font.render(text, antialias, color)

    def render_outlined_text(
        self,
        text: str,
        size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255),
        outline_color: Tuple[int, int, int] = (0, 0, 0),
        outline_width: int = 2,
        bold: bool = False
    ) -> pygame.Surface:
        """渲染带描边的文本"""
        font = self.get_font(size=size, bold=bold)

        # 渲染主体
        main_text = font.render(text, True, color)

        # 创建带描边的表面
        width = main_text.get_width() + outline_width * 2
        height = main_text.get_height() + outline_width * 2
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # 绘制描边
        outline_font = self.get_font(size=size, bold=bold)
        for dx in (-outline_width, 0, outline_width):
            for dy in (-outline_width, 0, outline_width):
                if dx == 0 and dy == 0:
                    continue
                outline = outline_font.render(text, True, outline_color)
                surface.blit(outline, (outline_width + dx, outline_width + dy))

        # 绘制主体
        surface.blit(main_text, (outline_width, outline_width))

        return surface

    def render_shadowed_text(
        self,
        text: str,
        size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255),
        shadow_color: Tuple[int, int, int] = (0, 0, 0),
        shadow_offset: int = 2,
        bold: bool = False
    ) -> pygame.Surface:
        """渲染带阴影的文本"""
        font = self.get_font(size=size, bold=bold)

        # 渲染阴影
        shadow = font.render(text, True, shadow_color)

        # 渲染主体
        main = font.render(text, True, color)

        # 合并
        width = max(main.get_width(), shadow.get_width() + shadow_offset)
        height = max(main.get_height(), shadow.get_height() + shadow_offset)
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # 绘制阴影
        surface.blit(shadow, (shadow_offset, shadow_offset))

        # 绘制主体
        surface.blit(main, (0, 0))

        return surface

    def create_text_table(
        self,
        headers: list,
        rows: list,
        size: int = 20,
        header_color: Tuple[int, int, int] = (255, 200, 100),
        row_color: Tuple[int, int, int] = (200, 200, 200),
        padding: int = 10
    ) -> pygame.Surface:
        """创建文本表格"""
        # 计算尺寸
        col_widths = []
        for i, header in enumerate(headers):
            width = self.render_text(header, size).get_width()
            for row in rows:
                if i < len(row):
                    width = max(width, self.render_text(str(row[i]), size).get_width())
            col_widths.append(width + padding * 2)

        total_width = sum(col_widths)
        total_height = size * (len(rows) + 1) + padding * 2

        # 创建表面
        surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 100))

        # 绘制表头
        x = 0
        for i, header in enumerate(headers):
            text = self.render_text(header, size, header_color, bold=True)
            surface.blit(text, (x + col_widths[i] // 2 - text.get_width() // 2, padding))
            x += col_widths[i]

        # 绘制分隔线
        pygame.draw.line(surface, (100, 100, 100), (0, size + padding), (total_width, size + padding), 1)

        # 绘制行
        y = size + padding * 2
        for row in rows:
            x = 0
            for i, cell in enumerate(row):
                if i >= len(col_widths):
                    break
                text = self.render_text(str(cell), size, row_color)
                surface.blit(text, (x + padding, y))
                x += col_widths[i]
            y += size

        return surface


# 全局文本渲染器
text_renderer = TextRenderer()
