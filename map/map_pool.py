"""
地图池管理
管理多张地图的随机选用
"""

import random
from pathlib import Path
from typing import List, Optional, Set


class MapPool:
    """地图池管理器"""

    def __init__(self, map_dir: str = 'assets/maps'):
        """
        初始化地图池

        Args:
            map_dir: 地图文件目录
        """
        self.map_dir = Path(map_dir)
        self.available_maps: List[str] = []  # 可用地图列表
        self.used_maps: Set[str] = set()     # 已用地图
        self._load_all_maps()

    def _load_all_maps(self):
        """加载目录下所有 .map 文件"""
        if not self.map_dir.exists():
            return

        map_files = sorted(self.map_dir.glob('*.map'))
        self.available_maps = [str(f) for f in map_files]

    def get_random(self) -> Optional[str]:
        """
        随机获取一张未使用的地图

        Returns:
            地图文件路径，None表示全部用完
        """
        if not self.available_maps:
            return None
        return random.choice(self.available_maps)

    def get_random_name(self) -> Optional[str]:
        """
        获取随机地图名称（不含路径和扩展名）

        Returns:
            地图名称，None表示全部用完
        """
        path = self.get_random()
        if path:
            return Path(path).stem
        return None

    def mark_used(self, map_path: str):
        """
        标记地图为已使用

        Args:
            map_path: 地图文件路径
        """
        if map_path in self.available_maps:
            self.available_maps.remove(map_path)
            self.used_maps.add(map_path)

    def mark_used_by_name(self, map_name: str):
        """
        根据地图名称标记为已使用

        Args:
            map_name: 地图名称（如 "level_01"）
        """
        for path in self.available_maps:
            if Path(path).stem == map_name:
                self.mark_used(path)
                break

    def has_available(self) -> bool:
        """检查是否还有可用地图"""
        return len(self.available_maps) > 0

    def get_remaining_count(self) -> int:
        """获取剩余可用地图数量"""
        return len(self.available_maps)

    def get_used_count(self) -> int:
        """获取已用地图数量"""
        return len(self.used_maps)

    def reset(self):
        """重置地图池（供重新开始游戏时调用）"""
        self.available_maps = list(self.used_maps)
        self.used_maps.clear()

    def refresh(self):
        """刷新地图列表（重新扫描目录）"""
        self.available_maps = []
        self.used_maps.clear()
        self._load_all_maps()


if __name__ == '__main__':
    # 测试地图池
    pool = MapPool()
    print(f"可用地图: {pool.available_maps}")
    print(f"剩余数量: {pool.get_remaining_count()}")

    if pool.has_available():
        map_path = pool.get_random()
        print(f"随机选取: {map_path}")
        pool.mark_used(map_path)
        print(f"剩余数量: {pool.get_remaining_count()}")
