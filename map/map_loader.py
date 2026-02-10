"""
地图加载器
支持加载 .map 和 .json 格式的地图文件
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from constants import TileType, TileChar


class MapLoader:
    """地图加载器"""

    # 字符到TileType的映射
    CHAR_TO_TILE = {
        TileChar.HARD_WALL: TileType.HARD_WALL,
        TileChar.SOFT_WALL: TileType.SOFT_WALL,
        TileChar.EMPTY: TileType.EMPTY,
        TileChar.EXIT: TileType.EXIT,
        TileChar.PLAYER: TileType.EMPTY,  # 玩家出生点标记，实际设为空地
    }

    def __init__(self):
        """初始化地图加载器"""
        pass

    def load(self, map_path: str) -> Dict[str, Any]:
        """
        加载地图文件

        Args:
            map_path: 地图文件路径（.map 或 .json）

        Returns:
            关卡数据字典
        """
        path = Path(map_path)

        if path.suffix == '.map':
            return self._load_map_file(path)
        elif path.suffix == '.json':
            return self._load_json_file(path)
        else:
            raise ValueError(f"不支持的地图格式: {path.suffix}")

    def _load_map_file(self, filepath: Path) -> Dict[str, Any]:
        """
        加载 .map 格式文件

        Args:
            filepath: .map 文件路径

        Returns:
            关卡数据字典
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f]

        # 解析地图
        level_data = self.parse_map_string(lines)

        # 添加默认敌人配置（简单版本）
        level_data['enemies'] = [
            {'type': 'basic', 'col': 1, 'row': 3, 'speed': 85},
            {'type': 'basic', 'col': 11, 'row': 3, 'speed': 85},
            {'type': 'basic', 'col': 1, 'row': 5, 'speed': 80},
            {'type': 'chase', 'col': 11, 'row': 5, 'speed': 95, 'chase_range': 5},
        ]

        # 添加玩家起始位置
        level_data['player_start'] = {'col': 1, 'row': 1}

        # 添加出口位置（从地图中解析）
        level_data['exit'] = level_data.get('exit', {'col': 11, 'row': 9})

        return level_data

    def _load_json_file(self, filepath: Path) -> Dict[str, Any]:
        """
        加载 .json 格式文件（向后兼容）

        Args:
            filepath: .json 文件路径

        Returns:
            关卡数据字典
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def parse_map_string(self, lines: List[str]) -> Dict[str, Any]:
        """
        解析地图字符串为关卡数据

        Args:
            lines: 地图字符串列表

        Returns:
            关卡数据字典
        """
        height = len(lines)
        width = len(lines[0]) if lines else 0

        tiles = []
        player_start = {'col': 1, 'row': 1}
        exit_pos = None

        for row_idx, line in enumerate(lines):
            tile_row = ''
            for col_idx, char in enumerate(line):
                if col_idx >= width:
                    continue

                # 处理特殊字符
                if char == TileChar.PLAYER:
                    player_start = {'col': col_idx, 'row': row_idx}
                    tile_char = TileChar.EMPTY
                elif char == TileChar.EXIT:
                    exit_pos = {'col': col_idx, 'row': row_idx}
                    tile_char = char
                else:
                    tile_char = char

                # 转换为tile类型字符
                tile_type = self.CHAR_TO_TILE.get(tile_char, TileType.EMPTY)
                if tile_type == TileType.HARD_WALL:
                    tile_row += TileChar.HARD_WALL
                elif tile_type == TileType.SOFT_WALL:
                    tile_row += TileChar.SOFT_WALL
                elif tile_type == TileType.EXIT:
                    tile_row += TileChar.EXIT
                else:
                    tile_row += TileChar.EMPTY

            tiles.append(tile_row)

        result = {
            'width': width,
            'height': height,
            'tile_size': 48,
            'title': f"关卡",
            'tiles': tiles,
            'player_start': player_start,
        }

        if exit_pos:
            result['exit'] = exit_pos

        return result

    def get_all_map_files(self, map_dir: str = 'assets/maps') -> List[str]:
        """
        获取目录下所有地图文件

        Args:
            map_dir: 地图目录

        Returns:
            地图文件路径列表
        """
        path = Path(map_dir)
        if not path.exists():
            return []

        return sorted(path.glob('*.map'))


if __name__ == '__main__':
    # 测试加载
    loader = MapLoader()

    # 加载一个示例地图
    print("加载 maps 目录下的所有地图:")
    map_files = loader.get_all_map_files()
    for mf in map_files[:3]:  # 只显示前3个
        print(f"  {mf}")

    # 解析第一张地图
    if map_files:
        data = loader.load(str(map_files[0]))
        print(f"\n地图尺寸: {data['width']} x {data['height']}")
        print("地图预览:")
        for row in data['tiles'][:5]:
            print(f"  {row}")
