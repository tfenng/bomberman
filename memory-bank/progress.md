# 开发进度记录（Progress Log）

## 进度概览

| 阶段 | 内容 | 状态 | 里程碑 |
|------|------|------|--------|
| 阶段 A | 项目初始化 + Windows CI | ? 完成 | M1 |
| 阶段 B | 核心玩法闭环 | ?? 进行中（HUD/倒计时/Punisher/重开已补；LDtk/测试待补） | M2 |
| 阶段 C | 敌人系统 | ?? 骨架就位（EnemyCount 已接入出口判定；敌人行为未实现） | M3 |
| 阶段 D | 道具与战役进程 | ? 未开始 | M3 |
| 阶段 E | 内容扩展 | ? 未开始 | M4 |
| 阶段 F | Windows 发布 | ? 未开始 | M5 |

---

## 当前阶段 TODO（阶段 B - 核心玩法闭环）

### 已完成项
- [x] **B-1**: 隐藏出口逻辑（清怪后显现）- `EnemyCount` 资源已建立，[src/plugins/bomb.rs](../src/plugins/bomb.rs) `check_exit` 通过它门控过关
- [x] **B-2**: 关卡切换流程（过关 → 下一关）- [src/plugins/game_state.rs](../src/plugins/game_state.rs) `GameState` 跟踪 `current_level` 并递增
- [x] **B-3**: 游戏失败流程（死亡 → 重开）- `GameOver` 状态已接入，按 Enter 回 `MainMenu`
- [x] **B-4**: 游戏胜利流程（通关 → 结束画面）- 全部关卡完成后进入 `Victory` 状态
- [x] **B-5**: HUD 插件 —— 生命 / 敌人数 / 炸弹容量 / 火焰范围 / 倒计时显示（已新增 [src/plugins/ui.rs](../src/plugins/ui.rs)）
- [x] **B-6**: 主线关 300 秒倒计时运行时 —— [src/plugins/game_state.rs](../src/plugins/game_state.rs) 已建立 `LevelTimer`，并在 Update 中递减
- [x] **B-7**: 超时惩罚 —— 倒计时归零后生成 `punisher_spawn_count` 个 Punisher（已接入随机安全区生成）
- [x] **B-9**: 玩家死亡复位 —— [src/plugins/game_state.rs](../src/plugins/game_state.rs) 已在保命重开时重建关卡并把玩家拉回 `StageMap.player_spawn`
- [x] **B-10**: 过关衔接打磨 —— [src/plugins/bomb.rs](../src/plugins/bomb.rs) 已从 `MainMenu` 回绕改为直接触发关卡重置流程

### 缺口项（未完成，阻塞阶段 B 收尾）
- [ ] **B-8**: LDtk 关卡落地 —— 当前地图为 [src/plugins/map.rs](../src/plugins/map.rs) 硬编码程序化生成，`bevy_ecs_ldtk` 依赖已引但未使用；[assets/levels/README.md](../assets/levels/README.md) 预留了 `stage_1.ldtk` 约定
- [ ] **B-11**: 自动化测试 —— 已新增 [tests/core_rules.rs](../tests/core_rules.rs) 的基础规则测试（出生区、阻挡、Timer reset），但 §6.1 的完整覆盖仍未补齐

### 验证项
- [ ] **B-V1**: 玩家可完整通关单关 —— 需人工走查并回填截图/录屏
- [ ] **B-V2**: 爆炸传播和判定稳定一致 —— 需人工走查并回填截图/录屏
- [ ] **B-V3**: 自炸、自困、卡位等经典风险都能正确发生 —— 需人工走查并回填截图/录屏

---

## 阶段 C TODO（敌人系统）

### 已就位骨架
- [x] **C-0**: `EnemyCount` 资源与 `OnEnter(InGame)` 重置（[src/plugins/enemy.rs](../src/plugins/enemy.rs)），并被 [src/plugins/bomb.rs](../src/plugins/bomb.rs) `check_exit` 读取作为出口门控

### 敌人实现
- [ ] **C-1**: Drifter（随机移动，2.0 tiles/sec）
- [ ] **C-2**: Seeker-Y（Y轴追踪，3.0 tiles/sec）
- [ ] **C-3**: Seeker-X（X轴追踪，3.0 tiles/sec）
- [ ] **C-4**: Hunter（双轴追踪，4.0 tiles/sec）
- [ ] **C-5**: Phantom（穿软墙，2.0 tiles/sec）
- [ ] **C-6**: Punisher（超时惩罚，穿软墙，4.0 tiles/sec）

### 敌人行为
- [ ] **C-7**: 敌人转向决策锁定在格中心
- [ ] **C-8**: Seeker-Y/X 仅在同列/同行时追踪
- [ ] **C-9**: Phantom/Punisher 仅可穿过软墙

---

## 阶段 D TODO（道具与战役进程）

> 铺垫现状：[src/plugins/player.rs](../src/plugins/player.rs) `Player` 组件已有 `bomb_capacity / flame_length / lives` 字段，[src/plugins/game_state.rs](../src/plugins/game_state.rs) `GameState` 已有 `score` 字段，但尚无拾取实体、得分规则与奖励关入口。

### 核心成长道具
- [ ] **D-1**: Bomb Up（炸弹上限 +1）
- [ ] **D-2**: Fire Up（火焰范围 +1）
- [ ] **D-3**: Skate（移动速度提升）

### 战役系统
- [ ] **D-4**: 生命系统（初始生命、死亡消耗）
- [ ] **D-5**: 分数系统
- [ ] **D-6**: 奖励关插入逻辑
- [ ] **D-7**: 成长道具封顶后 10000 分替代奖励

---

## 历史记录

### ? Step 1-7（阶段 A + 阶段 B 部分）
完成时间：2026-03-31

- [x] 初始化 Rust/Bevy 工程骨架
- [x] 基础 App、窗口、状态机与日志入口
- [x] 地图加载与数据配置骨架
- [x] Windows CI 构建链
- [x] 核心玩法第一批实现（玩家移动、炸弹爆炸）

### ? 2026-04-18 - 阶段 B 修复与完善

**完成：**
- [x] AppState添加GameOver和Victory状态
- [x] 炸弹/火焰计时器接入GameBalanceConfig配置
- [x] 修复连锁爆炸bug：使用processed_bombs追踪已处理炸弹
- [x] 实现玩家死亡逻辑：生命归零进入GameOver，否则复活
- [x] 实现出口检测：玩家到达出口进入Victory状态
- [x] 添加GameState资源跟踪关卡进度
- [x] 添加EnemyCount资源为敌人系统做准备
- [x] 实现GameOver/Victory按Enter重启流程
- [x] 实现多关卡切换（当前4关）

**待验证：**
- [ ] 炸弹自炸检测
- [ ] 连锁爆炸正确性
- [ ] 复活位置正确

### ?? 2026-04-24 - 进度核验快照

对照 [implementation-plan.md](implementation-plan.md) 逐项核验 `src/` 实际代码后更新状态。

**已验证完成（阶段 A + B 核心）：**
- Cargo 依赖：`bevy 0.17.3` / `bevy_ecs_tilemap 0.17` / `bevy_ecs_ldtk 0.13` / `serde` / `serde_json` / `anyhow`
- 目录骨架采用 `src/plugins/*.rs` 扁平化组织，与实施计划 §3.2 推荐的 `src/<模块>/` 略有出入（当前扁平化够用，未来扩大规模时可再分层）
- Windows CI：[.github/workflows/windows-build.yml](../.github/workflows/windows-build.yml) 走 `x86_64-pc-windows-msvc` 的 release 构建与 artifact 上传
- 状态机：`AppState { MainMenu, InGame, Paused, GameOver, Victory }` 已完整接入
- 地图程序化生成：[src/plugins/map.rs](../src/plugins/map.rs) 21×13、硬墙边框+偶数格硬柱、出生区 2×2 安全、稀疏软墙、`is_blocked` 统一阻挡判定
- 玩家按格移动：[src/plugins/player.rs](../src/plugins/player.rs) 方向键/WASD + 硬/软墙/炸弹阻挡
- 炸弹核心：[src/plugins/bomb.rs](../src/plugins/bomb.rs) 容量限制、同格去重、引信、十字火焰传播、硬墙止步、软墙摧毁、连锁爆炸（`processed_bombs` 去重 + `chain_queue`）、火焰命中扣生命
- 战役外壳：[src/plugins/game_state.rs](../src/plugins/game_state.rs) `GameState{current_level, total_levels=4, lives=3, score}`、`LevelTimer`、`LevelResetRequest`、关卡重置与清理逻辑
- 配置数据化：[src/plugins/config.rs](../src/plugins/config.rs) 从 [assets/config/gameplay.json](../assets/config/gameplay.json) 加载 `main_stage_timer_seconds / bomb_fuse_seconds / flame_duration_seconds / punisher_spawn_count`
- HUD / 倒计时 / Punisher / 重开：已接入 [src/plugins/ui.rs](../src/plugins/ui.rs)、[src/plugins/game_state.rs](../src/plugins/game_state.rs)、[src/plugins/bomb.rs](../src/plugins/bomb.rs)
- 基础回归测试：[tests/core_rules.rs](../tests/core_rules.rs) 覆盖出生区、阻挡和 `LevelTimer::reset`

**核验发现的缺口（需补进阶段 B 才能真正收尾）：**
- 未使用 LDtk（依赖已引，地图仍硬编码）
- 自动化测试覆盖还偏少，§6.1 的爆炸/连锁/出口/Punisher 断言仍需继续补齐

**升级的状态判断：**
- 阶段 B：`? 完成` → `?? 进行中`（规则可玩但完成标准未闭合）
- 阶段 C：`? 未开始` → `?? 骨架就位`（仅 `EnemyCount`，敌人实体与六类行为待实现）
- 阶段 A / D / E / F 状态判断不变

**下一步建议：**
1. 先补 LDtk 关卡落地，把阶段 B 的地图数据驱动收尾
2. 扩充 `tests/` 与 §6.1 核心断言（火焰止步、连锁、出口显现、上限、重开一致性）
3. 再开阶段 C 的敌人实体骨架与六类行为（Drifter → Seeker-Y/X → Hunter → Phantom → Punisher）
4. 将 HUD、倒计时和 Punisher 逻辑与更完整的敌人 AI 继续打通

### 2026-04-24 - 阶段 B 收尾实现

**完成：**
- [x] 新增 HUD 插件，显示生命 / 敌人数 / 炸弹容量 / 火焰范围 / 倒计时
- [x] 新增 `LevelTimer` 运行时和超时 Punisher 生成
- [x] 新增关卡重置流程，死亡保命和过关换图都回到 `StageMap.player_spawn`
- [x] 新增基础规则测试 `tests/core_rules.rs`

**下一步：**
- [ ] 接入 LDtk 关卡数据
- [ ] 补齐 §6.1 其余自动化测试

---

## 更新日志格式

```
### YYYY-MM-DD - [阶段名称]

**完成：**
- [任务描述]

**进行中：**
- [任务描述]

**下一步：**
- [任务描述]
```
