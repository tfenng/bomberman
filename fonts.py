"""
字体管理模块
处理跨平台中文字体问题
《经典炸弹人》复刻版
"""

import pygame
import sys
import os
from typing import Optional, List, Tuple


class FontManager:
    """字体管理器 - 处理跨平台中文字体"""

    _instance: Optional['FontManager'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._fonts: dict = {}
        self._system = sys.platform
        self._bundled_font_path: Optional[str] = None

    def _get_font_candidates(self) -> List[str]:
        """根据系统获取字体候选列表"""
        if self._system == "win32":
            return [
                "microsoftyahei",
                "simhei",
                "simsun",
                "mingliub",
                "kaiti",
                "arialunicode",
                "tahoma",
            ]
        elif self._system == "darwin":
            return [
                "pingfangsc",
                "pingfangsemicondensed",
                "heiti",
                "songti",
                "yuanti",
                "arial",
                "helvetica",
            ]
        else:
            return [
                "notosanssc",
                "notosanscjk",
                "notosanscjkhk",
                "wqy-zenhe",
                "wqy-microhei",
                "droidsansfallback",
                "droidsansfallbackforcn",
                "arplumingun",
                "arplumingtwmbe",
                "uming",
                "simhei",
                "dejavusans",
            ]

    def _find_best_font(self) -> str:
        """查找最佳字体"""
        candidates = self._get_font_candidates()

        # 检查捆绑字体
        base_paths = [
            sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable),
            os.path.dirname(__file__),
            os.path.join(os.path.dirname(__file__), 'assets', 'fonts'),
        ]

        for base_path in base_paths:
            for root, dirs, files in os.walk(base_path):
                for f in files:
                    if f.endswith(('.ttf', '.ttc', '.otf')):
                        if 'cjk' in f.lower() or 'chinese' in f.lower() or 'wqy' in f.lower():
                            return os.path.join(root, f)

        # 查找系统字体
        try:
            available = pygame.font.get_fonts()
        except:
            available = []

        # 精确匹配
        for candidate in candidates:
            if candidate in available:
                return candidate

        # 部分匹配
        for candidate in candidates:
            for avail in available:
                if candidate.lower() in avail.lower():
                    return avail

        # 回退
        return "arial"

    def get_font(self, name: str = None, size: int = 24, bold: bool = False) -> pygame.font.Font:
        """获取字体"""
        key = f"{name}_{size}_{bold}" if name else f"default_{size}_{bold}"

        if key in self._fonts:
            return self._fonts[key]

        # 尝试捆绑字体
        bundled = self._find_best_font()
        font = None

        if os.path.exists(bundled):
            try:
                font = pygame.font.Font(bundled, size)
                self._fonts[key] = font
                return font
            except:
                pass

        # 使用系统字体
        try:
            font = pygame.font.SysFont(bundled, size, bold=bold)
        except:
            font = pygame.font.Font(None, size)

        self._fonts[key] = font
        return font

    def render_text(self, text: str, size: int = 24,
                    color: Tuple[int, int, int] = (255, 255, 255),
                    bold: bool = False, antialias: bool = True) -> pygame.Surface:
        """渲染文本"""
        font = self.get_font(size=size, bold=bold)
        return font.render(text, antialias, color)

    def render_chinese(self, text: str, size: int = 24,
                       color: Tuple[int, int, int] = (255, 255, 255),
                       bold: bool = False) -> pygame.Surface:
        """渲染中文"""
        font = self.get_font(size=size, bold=bold)
        return font.render(text, True, color)


# 全局字体管理器
font_manager = FontManager()
