#!/usr/bin/env python3
"""
《经典炸弹人》复刻版
主程序入口

操作说明:
  W/A/S/D 或 方向键: 移动
  空格: 放置炸弹
  R: 重新开始
  ESC: 返回菜单/退出
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from game import Game


def main():
    """游戏主函数"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
