# 开发进度记录（Progress Log）

## Step 1 - 初始化 Rust/Bevy 工程骨架
- 在仓库根目录新增 `Cargo.toml`，初始化 `blast_maze` 项目。
- 选定核心依赖：`bevy`、`bevy_ecs_tilemap`、`bevy_ecs_ldtk`、`serde`、`serde_json`、`anyhow`。
- 建立基础目录结构：`src/`、`assets/config/`、`assets/levels/`、`.github/workflows/`。

## Step 2 - 基础 App、窗口、状态机与日志入口
- 新增 `src/main.rs`，统一从 `AppPlugin` 启动。
- 新增 `src/plugins/app.rs`，配置窗口标题、分辨率、状态机 `AppState`。
- 新增 `src/plugins/core.rs`，建立基础相机、全局键位输入（Enter 开始、Esc 暂停切换）。

## Step 3 - 地图加载与数据配置骨架
- 新增 `src/plugins/map.rs`，接入地图插件入口。
- 新增 `src/plugins/config.rs`，读取 `assets/config/gameplay.json` 到 `GameBalanceConfig` 资源。
- 新增 `assets/config/gameplay.json` 默认参数文件。
- 新增 `assets/levels/README.md` 说明关卡资源放置规范。

## Step 4 - Windows CI 构建链
- 新增 `.github/workflows/windows-build.yml`，配置 `windows-latest` 的构建流水线。
- 流水线执行 Rust toolchain 安装、依赖缓存、`cargo build --release`、artifact 上传。

## Step 5 - 核心玩法第一批实现（可先写代码，暂不阻塞于 cargo check）
- 新增 `src/plugins/player.rs`，实现玩家实体生成、按格移动与基础参数（炸弹容量/火焰长度/生命）。
- 新增 `src/plugins/bomb.rs`，实现放弹、2.25 秒引信、十字火焰扩散、软墙摧毁、连锁引爆与火焰生命周期。
- 改造 `src/plugins/map.rs`，实现 15x13 地图资源、硬墙/软墙/出口与阻挡判定工具函数。
- 更新 `src/plugins/app.rs` 与 `src/plugins/mod.rs`，注册 `PlayerPlugin` 与 `BombPlugin`。

## Step 6 - 文档同步
- 更新 `memory-bank/progress.md`，补充 Step 5 的实现记录。
- 更新 `memory-bank/architecture.md`，新增 player/bomb/map 三层职责说明，便于后续开发者接续阶段 B。

## Step 7 - 编译检查策略
- 按用户指示，当前轮次先优先推进代码编写；`cargo check` 继续保留为后续网络可用时再执行。
