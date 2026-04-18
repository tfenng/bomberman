# Blast Maze

A Bomberman-style game built with Bevy.

## Setup

1. Install Rust (latest stable)
2. Clone and run:

```sh
cargo run
```

For faster builds (iterative development):

```sh
cp .cargo/config_fast_builds.toml .cargo/config.toml
cargo run
```

## 运行与调试

### 本地运行

```sh
cargo run
```

### Debug 模式运行

```sh
cargo run --debug
```

### 发布构建

```sh
cargo build --release
```

构建产物位于 `target/release/blast_maze.exe`

### 运行测试

```sh
cargo test
```

### 代码检查

```sh
cargo check          # 快速检查编译错误
cargo clippy        # 代码风格检查
cargo fmt --check    # 格式检查
```

### IDE 调试

使用 VS Code + rust-analyzer：

1. 安装 rust-analyzer 扩展
2. 打开项目目录
3. `F5` 开始调试

或使用 CLion + Rust 插件。

## 游戏操作

| 按键 | 功能 |
|------|------|
| 方向键 / WASD | 移动 |
| 空格 | 放置炸弹 |
| Enter | 开始游戏 / 确认 |
| Esc | 暂停 / 取消 |

## 项目结构

```
src/
├── main.rs              # 应用入口
└── plugins/
    ├── app.rs          # 应用插件、状态定义
    ├── core.rs         # 相机、输入处理
    ├── map.rs          # 地图系统
    ├── player.rs       # 玩家系统
    ├── bomb.rs         # 炸弹系统
    ├── enemy.rs        # 敌人系统（阶段C）
    ├── config.rs       # 配置读取
    ├── game_state.rs   # 游戏状态（关卡/生命/分数）
    └── mod.rs          # 模块导出

assets/
├── config/
│   └── gameplay.json   # 游戏平衡参数
└── levels/             # 关卡文件

bevy-release-0.17.3/   # Bevy 引擎源码（参考用）

memory-bank/            # 设计文档
```

## 当前进度

| 阶段 | 状态 |
|------|------|
| 阶段 A | ✅ 完成 |
| 阶段 B | ✅ 完成 |
| 阶段 C | 🔜 下一个 |
| 阶段 D | ❌ 未开始 |
| 阶段 E | ❌ 未开始 |
| 阶段 F | ❌ 未开始 |

详见 [memory-bank/progress.md](memory-bank/progress.md)
