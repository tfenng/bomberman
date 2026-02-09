"""
资源加载管理模块
《经典炸弹人》复刻版
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

import pygame


class AssetManager:
    """资源管理器单例"""

    _instance: Optional['AssetManager'] = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not AssetManager._initialized:
            self._images: Dict[str, pygame.Surface] = {}
            self._sounds: Dict[str, pygame.mixer.Sound] = {}
            self._fonts: Dict[str, pygame.font.Font] = {}
            self._levels: Dict[str, Dict] = {}
            self._base_path = Path(__file__).parent / "assets"
            AssetManager._initialized = True

    @property
    def base_path(self) -> Path:
        """获取资源基础路径"""
        return self._base_path

    # ============ 图片资源 ============

    def load_image(self, name: str, path: str, scale: tuple = None) -> pygame.Surface:
        """加载图片资源"""
        key = f"{name}_{scale}" if scale else name
        if key in self._images:
            return self._images[key]

        filepath = self._base_path / path
        if not filepath.exists():
            # 如果文件不存在，创建一个简单的占位符
            surface = pygame.Surface((32, 32))
            surface.fill((128, 128, 128))
            self._images[key] = surface
            return surface

        image = pygame.image.load(str(filepath)).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        self._images[key] = image
        return image

    def get_image(self, name: str, scale: tuple = None) -> pygame.Surface:
        """获取图片资源（必须已加载）"""
        key = f"{name}_{scale}" if scale else name
        if key not in self._images:
            return self._create_default_surface(name, scale)
        return self._images[key]

    def _create_default_surface(self, name: str, scale: tuple = None) -> pygame.Surface:
        """创建默认占位符表面"""
        size = scale if scale else (32, 32)
        surface = pygame.Surface(size, pygame.SRCALPHA)

        # 根据名称创建不同颜色的占位符
        if "player" in name.lower():
            pygame.draw.circle(surface, (60, 140, 220), (size[0]//2, size[1]//2), size[0]//2)
        elif "enemy" in name.lower():
            pygame.draw.circle(surface, (220, 80, 80), (size[0]//2, size[1]//2), size[0]//2)
        elif "bomb" in name.lower():
            pygame.draw.circle(surface, (40, 40, 40), (size[0]//2, size[1]//2), size[0]//2)
        elif "wall" in name.lower() or "hard" in name.lower():
            surface.fill((80, 80, 90))
        elif "soft" in name.lower():
            surface.fill((160, 100, 60))
        else:
            surface.fill((100, 100, 100))

        return surface

    # ============ 声音资源 ============

    def load_sound(self, name: str, path: str) -> pygame.mixer.Sound:
        """加载声音资源"""
        if name in self._sounds:
            return self._sounds[name]

        filepath = self._base_path / path
        if not filepath.exists():
            # 创建静音替代品
            sound = pygame.mixer.Sound(buffer=bytearray(0))
            self._sounds[name] = sound
            return sound

        sound = pygame.mixer.Sound(str(filepath))
        self._sounds[name] = sound
        return sound

    def play_sound(self, name: str):
        """播放声音"""
        if name in self._sounds:
            self._sounds[name].play()

    # ============ 字体资源 ============

    def load_font(self, name: str, path: str, size: int) -> pygame.font.Font:
        """加载字体资源"""
        key = f"{name}_{size}"
        if key in self._fonts:
            return self._fonts[key]

        filepath = self._base_path / path
        if not filepath.exists():
            # 使用系统字体作为后备
            font = pygame.font.SysFont("arial", size)
        else:
            font = pygame.font.Font(str(filepath), size)
        self._fonts[key] = font
        return font

    def get_font(self, name: str, size: int) -> pygame.font.Font:
        """获取字体"""
        key = f"{name}_{size}"
        if key not in self._fonts:
            return pygame.font.SysFont("arial", size)
        return self._fonts[key]

    # ============ 关卡资源 ============

    def load_level(self, name: str = "level_01") -> Dict[str, Any]:
        """加载关卡数据"""
        if name in self._levels:
            return self._levels[name]

        filepath = self._base_path / "maps" / f"{name}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"关卡文件不存在: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            level_data = json.load(f)

        self._levels[name] = level_data
        return level_data

    def get_level(self, name: str = "level_01") -> Dict[str, Any]:
        """获取关卡数据"""
        return self._levels.get(name, self.load_level(name))

    # ============ 资源清理 ============

    def clear_cache(self):
        """清理资源缓存"""
        self._images.clear()
        self._sounds.clear()
        self._fonts.clear()
        self._levels.clear()

    def preload_all(self):
        """预加载所有资源"""
        # 预加载默认图片
        self.load_image("player", "images/player.png", (36, 36))
        self.load_image("enemy_basic", "images/enemy_basic.png", (32, 32))
        self.load_image("enemy_chase", "images/enemy_chase.png", (32, 32))
        self.load_image("bomb", "images/bomb.png", (32, 32))
        self.load_image("powerup_fire", "images/powerup_fire.png", (24, 24))
        self.load_image("powerup_bomb", "images/powerup_bomb.png", (24, 24))
        self.load_image("powerup_speed", "images/powerup_speed.png", (24, 24))
        self.load_image("wall_hard", "images/wall_hard.png", (48, 48))
        self.load_image("wall_soft", "images/wall_soft.png", (48, 48))
        self.load_image("exit", "images/exit.png", (48, 48))

        # 预加载关卡
        self.load_level()


# 全局资源管理器实例
assets = AssetManager()
