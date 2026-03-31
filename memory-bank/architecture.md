# 架构洞察（Architecture Insights）

## 根目录
- `Cargo.toml`：Rust 项目入口配置，定义包名、版本、编译版本及核心依赖。

## 运行入口层
- `src/main.rs`：应用启动入口，仅负责创建 Bevy `App` 并注册组合插件。
- `src/plugins/mod.rs`：插件模块导出中心，控制子模块显式可见性。

## 应用编排层
- `src/plugins/app.rs`：顶层应用插件；负责窗口参数、默认插件、全局状态机注册，以及子插件组合装配。
- `src/plugins/core.rs`：核心运行时插件；负责基础渲染相机和全局输入逻辑，承载跨系统通用行为。

## 地图与空间规则层
- `src/plugins/map.rs`：地图资源和空间判定中心。
  - 维护 `StageMap`（尺寸、硬墙、软墙、出口、出生点）。
  - 提供 `GridPosition` 格坐标组件与 `TileKind` 标记。
  - 提供 `tile_to_transform`、`is_blocked` 供角色和炸弹系统复用。

## 玩家层
- `src/plugins/player.rs`：玩家生命周期与输入移动。
  - 启动时在 `StageMap.player_spawn` 生成玩家。
  - 在 `InGame` 状态处理按格移动。
  - 根据地图阻挡和炸弹占位决定可移动性。

## 炸弹与爆炸层
- `src/plugins/bomb.rs`：炸弹闭环核心。
  - `Space` 放弹（受容量限制、同格去重）。
  - 引信计时后爆炸，按十字方向传播火焰。
  - 遇硬墙停止；遇软墙摧毁并停止；命中炸弹触发连锁引爆。
  - 火焰短时存在后销毁，并处理玩家被火焰命中后的死亡状态切换。

## 数据与规则配置层
- `src/plugins/config.rs`：配置读取插件；将 `assets/config/gameplay.json` 解析为强类型资源，提供规则参数注入点。
- `assets/config/gameplay.json`：游戏规则参数数据文件（计时、引信、火焰持续、Punisher 数量）。

## 资源约定层
- `assets/levels/README.md`：关卡资源目录约定说明，为后续 LDtk 文件接入提供最小规范。

## 工程自动化层
- `.github/workflows/windows-build.yml`：Windows CI 构建流程定义，确保每次提交都可进行 release 构建与产物上传。

## Memory Bank 文档层
- `memory-bank/progress.md`：实施计划执行日志，按步骤记录“做了什么、为什么这样做”。
- `memory-bank/architecture.md`：本文件；面向后续开发者解释当前工程每个关键文件的职责边界。
