"""
地图生成器
程序化生成炸弹人游戏地图
"""

import random
from pathlib import Path
from typing import List, Optional

from constants import TileChar


class MapGenerator:
    """地图生成器"""

    def __init__(self, width: int = 13, height: int = 11, seed: Optional[int] = None):
        """
        初始化地图生成器

        Args:
            width: 地图宽度（列数）
            height: 地图高度（行数）
            seed: 随机种子，用于生成可复现的地图
        """
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(seed)

    def generate(self) -> List[str]:
        """
        生成单张地图

        Returns:
            地图字符串列表，每行一个字符串
        """
        # 初始化空地图
        grid = [[TileChar.EMPTY for _ in range(self.width)] for _ in range(self.height)]

        # 1. 四周硬墙
        for x in range(self.width):
            grid[0][x] = TileChar.HARD_WALL
            grid[self.height - 1][x] = TileChar.HARD_WALL
        for y in range(self.height):
            grid[y][0] = TileChar.HARD_WALL
            grid[y][self.width - 1] = TileChar.HARD_WALL

        # 2. 内部十字硬墙骨架（2格间距）
        for y in range(2, self.height - 2, 2):
            for x in range(2, self.width - 2, 2):
                grid[y][x] = TileChar.HARD_WALL

        # 3. 随机软墙填充（50%-70%概率）
        soft_wall_positions = []
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                # 跳过骨架位置
                if y % 2 == 0 and x % 2 == 0:
                    continue
                # 随机填充软墙
                if random.random() < random.uniform(0.50, 0.70):
                    grid[y][x] = TileChar.SOFT_WALL
                    soft_wall_positions.append((x, y))

        # 4. 玩家出生点安全区（清空周围）
        safe_zone = [(1, 1), (2, 1), (1, 2), (2, 2)]
        for x, y in safe_zone:
            grid[y][x] = TileChar.EMPTY

        # 设置玩家出生点标记
        grid[1][1] = TileChar.PLAYER

        # 5. 随机放置出口（在远端软墙位置）
        if soft_wall_positions:
            # 选择远端的软墙位置（离出生点尽可能远）
            far_positions = [
                pos for pos in soft_wall_positions
                if pos[0] > self.width // 2 or pos[1] > self.height // 2
            ]
            if not far_positions:
                far_positions = soft_wall_positions

            exit_x, exit_y = random.choice(far_positions)
            grid[exit_y][exit_x] = TileChar.EXIT

        # 转换为字符串列表
        return [''.join(row) for row in grid]

    def generate_to_file(self, filename: str) -> str:
        """
        生成单张地图并保存到文件

        Args:
            filename: 文件路径

        Returns:
            保存的文件路径
        """
        map_data = self.generate()
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            for line in map_data:
                f.write(line + '\n')

        return str(filepath)

    def generate_multiple(self, count: int, save_dir: str) -> List[str]:
        """
        生成多张地图并保存

        Args:
            count: 生成地图数量
            save_dir: 保存目录

        Returns:
            保存的文件路径列表
        """
        saved_files = []
        save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)

        for i in range(1, count + 1):
            # 为每张地图使用不同的种子
            self.generate()  # 使用全局随机状态
            filename = save_path / f"level_{i:02d}.map"
            self.generate_to_file(str(filename))
            saved_files.append(str(filename))

        return saved_files


def generate_maps_demo():
    """演示：生成3张地图"""
    print("正在生成3张测试地图...")
    generator = MapGenerator()
    files = generator.generate_multiple(3, 'assets/maps')
    print(f"已生成地图文件:")
    for f in files:
        print(f"  - {f}")
    print("\n地图预览 (level_01.map):")
    with open('assets/maps/level_01.map', 'r') as f:
        print(f.read())


if __name__ == '__main__':
    generate_maps_demo()
