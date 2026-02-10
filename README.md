---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304602210090eb59b550977dfbe41d17340bf3f6d1f8b5fa164929c492350355ea694ad0c0022100d69e3ff16047d25d992a4ab6d0e7e490ab0c9e0e1cddb02f1c4222199021ed7e
    ReservedCode2: 304402205195e9f60ed9955e444fb0da18532eb78249834b59de0db09f0717bf0b5e3e1d0220353f434d7844ea78a0293edb1ba8e181dfec8aac302d609cd8e47fef9977ea64
---

# 《经典炸弹人》复刻版 - 简化Demo

> 基于 Pygame 的经典炸弹人游戏复刻版，专注于核心玩法验证。

## 📖 项目简介

这是一个经典炸弹人游戏的简化版本，聚焦于实现单一可玩关卡、单人模式和键盘控制，以最快速度构建一个可运行、可体验的核心玩法原型。

### 核心特性

- 🎮 **单人闯关模式**: 在精心设计的迷宫中消灭敌人，找到隐藏出口
- 💣 **炸弹系统**: 放置炸弹，炸毁软墙，消灭敌人
- 🎁 **道具系统**: 三种核心道具（火焰增强、炸弹数量、速度提升）
- 🤖 **敌人AI**: 两种敌人类型（基础型、追踪型）
- 🖥️ **跨平台支持**: Windows / macOS / Linux

## 🎯 操作说明

| 操作 | 键位 |
| :--- | :--- |
| 移动 | `W` `A` `S` `D` |
| 放置炸弹 | `空格键` |
| 重新开始 | `R` 键 |
| 退出游戏 | `Esc` 键 |

## 🚀 快速开始

### 环境要求

- Python 3.10 或更高版本
- 操作系统: Windows 10+, macOS 10.15+, Ubuntu 20.04+

### 安装依赖

```bash
# 克隆或下载项目后，进入项目目录
pip install -r requirements.txt
```

### 运行游戏（开发模式）

```bash
python main.py
```

### 打包为独立应用

```bash
# 自动检测当前平台并打包
python build_config.py

# 手动使用 PyInstaller（高级）
pyinstaller --clean --windowed --onefile \
  --add-data "assets:assets" \
  --name Bomberman \
  main.py
```

打包后的可执行文件位于 `dist/` 目录。

## 📁 项目结构

```
bomberman/
├── main.py                 # 程序入口
├── requirements.txt        # Python依赖清单
├── build_config.py         # 打包配置脚本
├── README.md               # 项目说明
│
├── docs/
│   └── prd.md              # 完整产品需求文档
│
├── src/                    # 源代码
│   ├── game.py             # 游戏主循环
│   ├── config.py           # 全局配置
│   ├── entities/           # 游戏实体（玩家、敌人、炸弹等）
│   ├── systems/            # 游戏系统（网格、碰撞、AI）
│   ├── scenes/             # 场景管理
│   ├── ui/                 # 用户界面
│   └── utils/              # 工具模块
│
└── assets/                 # 游戏资源
    ├── images/             # 图像资源
    ├── sounds/             # 音效资源
    ├── fonts/              # 字体文件
    └── maps/               # 地图数据
        └── level_01.json   # 第一关地图
```

## 🎮 游戏玩法

### 胜利条件
1. 消灭地图上所有敌人
2. 隐藏的出口会显现（发出光芒）
3. 移动到出口位置即可通关

### 失败条件
- 被炸弹火焰击中
- 触碰到敌人

### 道具效果

| 道具 | 外观 | 效果 |
| :--- | :--- | :--- |
| **火焰增强** | 🔴 红色方块 | 炸弹火焰范围 +1 格 |
| **炸弹数量** | 🔵 蓝色方块 | 可同时放置炸弹数量 +1 |
| **速度提升** | 🟢 绿色方块 | 移动速度提升 20% |

## 🛠️ 技术栈

- **核心框架**: Pygame 2.5.0+
- **编程语言**: Python 3.10+
- **打包工具**: PyInstaller 6.0.0+

## 📋 开发路线图

详细的开发计划请参考 [`docs/prd.md`](docs/prd.md) 第8章节。

### 关键里程碑

- **第7天**: MVP原型（玩家移动、放炸弹、炸墙）
- **第14天**: 完整Demo（所有功能实现，可通关）
- **第16天**: 发布版本（三平台打包完成）

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建新分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 🙏 致谢

- 经典炸弹人游戏的原创团队
- Pygame 社区的支持与贡献
- 所有参与测试和反馈的玩家

## TODO 待修复，重要且紧急
在之前的和AI漫长的 chat流中， 发现下面两类问题最突出
- 地图的构造，最好单独设计子系统，由自定义的字符矩阵保存，交由主游戏应用
- NPC移动过程中接墙角后粘连

## TODO 新特性，重要不紧急
- 更好看的player/npc/墙体图片
- 音效效果优化
- 支持手柄游玩
- 难度可配置

---

**作者**: MiniMax Agent
**版本**: v1.0.0
**最后更新**: 2026-02-09
