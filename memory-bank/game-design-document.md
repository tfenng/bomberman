# 爆弹迷宫 新设计文档 / Blast Maze Clean-Slate Design Document

## 1. 产品定位与经典参照 / Product Positioning and Classic Reference

### 中文

本项目是一款从零开始设计的单人动作迷宫游戏。它以 [bomber.md](/Users/tony/src/bomberman/docs/bomber.md) 中整理的 FC/NES《炸弹人》特征为重要参照，但不是复刻，也不继承任何已废弃原型的技术假设或内容结构。

这版产品要保留的经典骨架：

- 迷宫地图中的高风险炸弹决策
- 软墙破坏、隐藏出口、清怪后过关
- 出生区安全保护
- 敌人类型分层与节奏递进
- 奖励关带来的节奏变化
- 道具与秘密目标带来的重复游玩价值

这版产品明确不照搬的部分：

- 不采用 FC 原版 `30 x 13` 横向滚屏结构
- 不做 `50` 关超长马拉松
- 不把极端隐晦的彩蛋积分条件作为主流程理解门槛
- 不沿用旧原型里的实现参数、文件结构或引擎约束

产品目标是做出“经典规则骨架 + 清晰现代反馈”的单人桌面动作游戏：玩家能在 10 秒内理解目标，在第一局就体验到放炸弹、炸墙、误伤自己和诱敌进爆炸范围的乐趣，并在后续关卡中形成更成熟的路线规划与节奏控制。

### English

This project is a clean-slate single-player action-maze game. It takes key FC/NES Bomberman traits summarized in [bomber.md](/Users/tony/src/bomberman/docs/bomber.md) as reference, but it is not a direct remake and does not inherit any assumptions from the abandoned prototype.

Classic foundations this product intentionally keeps:

- high-risk bomb decision making inside a maze
- destructible soft walls, hidden exits, and enemy-clear stage completion
- guaranteed spawn safety
- layered enemy archetypes and pacing escalation
- bonus stages that change the rhythm
- power-ups and secret objectives that support replayability

Things this product deliberately does not copy:

- no FC-style `30 x 13` horizontally scrolling stage format
- no `50`-stage marathon campaign
- no reliance on extremely obscure secret-score conditions for core progression
- no reuse of old prototype parameters, file layout, or engine constraints

The goal is a single-player desktop action game with a "classic rules backbone + clear modern feedback" approach: players should understand the objective within 10 seconds, experience bombing walls, self-trapping, and baiting enemies in the first session, and then grow into route planning and pacing mastery across later stages.

## 2. 核心循环、战役结构与胜负规则 / Core Loop, Campaign Structure, and Win-Lose Rules

### 中文

#### 2.1 单局核心循环

1. 阅读出生区和可走路线
2. 放置炸弹打开地图
3. 在爆炸前撤离并维持安全路径
4. 利用爆炸范围诱杀或封锁敌人
5. 拾取成长道具或战术道具
6. 清空敌人后找到并进入出口

#### 2.2 战役结构

- 主战役包含 `12` 个主线关卡
- 每 `4` 个主线关卡后插入 `1` 个奖励关
- 总流程为 `12` 主线关 + `3` 奖励关
- 每个主题区的第 `4` 关通关后，先奖励 `1` 条生命，再进入对应奖励关
- 奖励关采用 `30 秒` 限时挑战
- 奖励关中玩家无敌，目标是在限定时间内尽可能多地消灭敌人赚取分数

#### 2.3 生命与重开

- 开局生命数：`3`
- 每通过一个主题区末关后奖励 `1` 条生命
- 生命上限：`5`
- 玩家死亡时，若仍有剩余生命，则立即重开当前关卡
- 生命归零后结束本次战役并返回标题界面
- MVP 不包含密码系统或存档续关系统

#### 2.4 玩家规则

- 地图逻辑以 tile 为核心，视觉表现可平滑移动
- 玩家与敌人的逻辑移动都以格中心为锚点，只在到达格中心时选择新方向
- 默认操作：
  - `W/A/S/D` 或方向键：移动
  - `Space`：放置炸弹
  - `Enter`：菜单确认
  - `R`：失败后快速重开
  - `Esc`：暂停或返回
- 玩家无血量条，任何爆炸伤害或敌人接触都直接致死

#### 2.5 炸弹规则

- 初始炸弹容量：`1`
- 初始火焰长度：`1`
- 初始引信：`2.25 秒`
- 火焰有效时间：`0.45 秒`
- 炸弹最大容量：`5`
- 火焰最大长度：`5`
- 爆炸为经典十字扩散
- 火焰遇硬墙立即停止
- 火焰摧毁软墙并在该格停止
- 火焰触碰炸弹会立即引发连锁爆炸
- 玩家放下炸弹后，可在离开当前格之前短暂穿出该炸弹；离开后炸弹变为实体阻挡

#### 2.6 胜利与失败

- 失败条件：
  - 玩家接触任意爆炸火焰
  - 玩家与敌人发生接触
- 关卡胜利条件：
  - 地图内所有敌人被消灭
  - 隐藏出口显现
  - 玩家进入出口

#### 2.7 关卡计时与拖延惩罚

- 所有主线关卡统一采用 `300 秒` 倒计时
- HUD 持续显示剩余时间
- 倒计时归零后，地图上新增 `2` 个 `Punisher`
- `Punisher` 从可通行候选格中随机生成，但必须与玩家当前位置保持最小安全间隔
- `Punisher` 只可穿过软墙，不可穿过硬墙或炸弹

#### 2.8 轻量现代化 QoL

- 炸弹临爆前要有清晰的闪烁节奏
- HUD 持续显示剩余敌人数、生命数、炸弹容量、火焰等级、速度等级
- 前两关使用极简文本提示帮助理解“先清敌人，再进出口”
- 不加入自动逃生、炸弹落点修正、时间倒流等削弱风险的机制

### English

#### 2.1 Per-Stage Core Loop

1. read the spawn area and available paths
2. place bombs to open the map
3. evacuate before detonation and preserve a safe route
4. use blast lines to bait or trap enemies
5. collect progression or tactical pickups
6. reveal and enter the exit after clearing enemies

#### 2.2 Campaign Structure

- The main campaign contains `12` core stages
- A bonus stage appears after every `4` core stages
- Total flow: `12` core stages + `3` bonus stages
- Clearing stage `4` of each themed zone grants `1` extra life before entering its bonus stage
- Bonus stages are `30-second` timed challenges
- During bonus stages the player is invulnerable and tries to destroy as many enemies as possible for score

#### 2.3 Lives and Restart

- Starting lives: `3`
- Clearing the final stage of each themed zone grants `1` extra life
- Life cap: `5`
- On death, if lives remain, the current stage restarts immediately
- On zero lives, the campaign ends and returns to the title screen
- MVP does not include a password or save-based continue system

#### 2.4 Player Rules

- Gameplay logic is tile-centric, while movement presentation may be smooth
- Player and enemy logic both anchor to tile centers and only choose new directions on center arrival
- Default controls:
  - `W/A/S/D` or arrow keys: move
  - `Space`: place bomb
  - `Enter`: confirm in menus
  - `R`: fast restart after failure
  - `Esc`: pause or back
- The player has no health bar; any explosion damage or enemy contact is instantly lethal

#### 2.5 Bomb Rules

- Starting bomb capacity: `1`
- Starting flame length: `1`
- Starting fuse: `2.25 seconds`
- Flame active duration: `0.45 seconds`
- Maximum bomb capacity: `5`
- Maximum flame length: `5`
- Explosions use the classic cross pattern
- Flames stop immediately on hard walls
- Flames destroy soft walls and stop on that tile
- Flames touching bombs trigger immediate chain detonation
- After placing a bomb, the player may briefly step out through it before it becomes solid

#### 2.6 Win and Loss

- Lose conditions:
  - the player touches any explosion flame
  - the player contacts an enemy
- Stage clear conditions:
  - all enemies in the map are defeated
  - the hidden exit is revealed
  - the player enters the exit

#### 2.7 Stage Timer and Anti-Stall Pressure

- All mainline stages use a shared `300-second` countdown
- The HUD continuously shows remaining time
- When the countdown reaches zero, `2` `Punisher` enemies are added to the map
- `Punishers` spawn from valid passable cells chosen at random, but each spawn must keep a minimum safety gap from the player's current location
- `Punishers` may pass through soft walls only; they do not pass through hard walls or bombs

#### 2.8 Light Modern QoL

- Bombs must communicate imminent detonation with a clear flashing rhythm
- The HUD continuously shows remaining enemies, lives, bomb capacity, flame level, and speed tier
- The first two stages use minimal onboarding text to teach "clear enemies first, then use the exit"
- Do not add systems such as auto-escape, bomb auto-correction, or time rewind

## 3. 地图设计、生成原则与奖励关 / Map Design, Generation Principles, and Bonus Stages

### 中文

#### 3.1 主线标准地图

- 标准关卡尺寸：`15 x 13`
- 单屏固定视野
- 不采用横向滚屏
- 这是对 FC 版 `30 x 13` 横向长图的主动取舍：保留经典迷宫密度与柱阵感，但改为更适合现代单局阅读的单屏布局

#### 3.2 基础布局法则

- 最外圈全部为硬墙
- 内部使用规则柱阵，形成稳定十字路口与死角
- 玩家出生区固定在左上象限
- 出生区至少保证 `2 x 2` 安全空间
- 出生后第一颗炸弹必须存在明确逃生路线
- 出口默认藏在距离出生点最远象限的一块软墙下
- 任何地图都必须确保出生区不被砖块封死，这一点直接继承经典 Bomberman 的安全思路

#### 3.3 软墙生成策略

- 关卡采用“作者控制模板 + 伪随机软墙填充”
- 伪随机仅作用于允许放置软墙的候选格
- 第 1 关软墙目标数量：`42`
- 随关卡推进逐步提高，最终主线关约 `72`
- 软墙增加时优先提高远离出生区和出口区的密度

#### 3.4 ASCII 参考图

```text
###############
#@   . . .    #
# # # # # # # #
# . .   .   . #
# # # # # # # #
#   . . . .   #
# # # # # # # #
# .   .   . . #
# # # # # # # #
#   . . .   . #
# # # # # # # #
#      . .  X #
###############
```

图例：

- `#`：硬墙
- `.`：软墙
- `@`：玩家出生点
- `X`：出口逻辑位置，初始应隐藏在软墙下
- `空格`：通路

#### 3.5 奖励关设计

- 奖励关地图采用更开阔的布局
- 不设置隐藏出口
- 不掉落常规成长道具
- 玩家无敌
- 目标是 `30 秒` 内高效消灭敌人并赚取额外分数
- 奖励关用于打断主线压力，形成情绪释放与分数追求

### English

#### 3.1 Standard Mainline Map

- Standard stage size: `15 x 13`
- Single-screen fixed camera
- No horizontal scrolling
- This is a deliberate adaptation of the FC game's `30 x 13` scrolling format: keep the classic maze density and pillar language, but reshape it into a single-screen layout that is easier to read in modern play

#### 3.2 Core Layout Rules

- The outer border is fully hard wall
- The interior uses a regular pillar pattern to produce stable intersections and dead ends
- The player spawn is fixed in the upper-left quadrant
- The spawn area must guarantee at least a `2 x 2` safe zone
- The first bomb always needs a valid escape route
- The exit is hidden under a soft wall in the quadrant farthest from spawn
- No map may seal the player inside the spawn zone; this safety rule is directly inherited from classic Bomberman design

#### 3.3 Soft-Wall Generation Strategy

- Stages use "authored template + pseudo-random soft-wall fill"
- Randomization only affects eligible soft-wall cells
- Stage 1 target soft-wall count: `42`
- The count rises gradually across the campaign to roughly `72` in late mainline stages
- Density should increase primarily away from the spawn area and exit region

#### 3.4 ASCII Reference Map

```text
###############
#@   . . .    #
# # # # # # # #
# . .   .   . #
# # # # # # # #
#   . . . .   #
# # # # # # # #
# .   .   . . #
# # # # # # # #
#   . . .   . #
# # # # # # # #
#      . .  X #
###############
```

Legend:

- `#`: hard wall
- `.`: soft wall
- `@`: player spawn
- `X`: logical exit position, initially hidden under a soft wall
- `space`: passable floor

#### 3.5 Bonus Stage Design

- Bonus stages use a more open layout
- No hidden exit
- No standard growth pickups
- The player is invulnerable
- The goal is to destroy enemies efficiently within `30 seconds` for bonus score
- Bonus stages break mainline tension and create a release-and-score rhythm

## 4. 敌人梯度、道具分层与分数系统 / Enemy Ladder, Power-Up Layers, and Scoring

### 中文

#### 4.1 玩家默认值

| 项目 | 默认值 | 上限 |
| --- | --- | --- |
| 生命 | 3 | 5 |
| 炸弹容量 | 1 | 5 |
| 火焰等级 | 1 | 5 |
| 速度等级 | 100% | 145% |

#### 4.2 敌人梯度

[bomber.md](/Users/tony/src/bomberman/docs/bomber.md) 中最有价值的启发之一，是敌人不是简单地“血量更高”，而是以追踪方式、速度和穿墙能力构成行为梯度。这版产品采用 5 个敌人家族：

| 敌人 | 分数 | 速度 | 行为摘要 | 设计职责 |
| --- | --- | --- | --- | --- |
| Drifter | 100 | 2.0 tiles/sec | 随机巡游，仅在到达格中心时重新选方向，遇阻改向 | 基础教学敌人 |
| Seeker-Y | 200 | 3.0 tiles/sec | 仅在与玩家同列时追踪，否则按默认巡游逻辑行动；仅在格中心重新决策 | 强化纵向压迫 |
| Seeker-X | 400 | 3.0 tiles/sec | 仅在与玩家同行时追踪，否则按默认巡游逻辑行动；仅在格中心重新决策 | 强化横向压迫 |
| Hunter | 800 | 4.0 tiles/sec | 在格中心优先选择能缩短与玩家曼哈顿距离的方向；若同轴则直接追击 | 中高压主力敌人 |
| Phantom | 2000 | 2.0 tiles/sec | 沿 `Hunter` 的追击逻辑行动，但只可穿过软墙，不可穿过硬墙或炸弹 | 高威胁稀有敌人 |

额外规则：

- 主线关卡中的敌人编排与核心成长道具分配由设计阶段预生成并固定到关卡数据中；同一关卡重开时结果保持一致
- 当主线关卡超时或进入极端拖延状态时，地图上新增 `2` 个 `Punisher`
- `Punisher` 为高压清场单位，移动速度为 `4.0 tiles/sec`，在格中心优先选择能缩短与玩家曼哈顿距离的方向，且只可穿过软墙

#### 4.3 道具分层

参考经典作品的“基础属性可长期保留、特殊功能更脆弱”思路，本作将道具分为两层：

核心成长道具，持续到本次战役结束：

| 道具 | 效果 | 上限 |
| --- | --- | --- |
| Bomb Up | 炸弹容量 +1 | 5 |
| Fire Up | 火焰长度 +1 | 5 |
| Skate | 移动速度 +15% | 145% |

战术功能道具，死亡后丢失：

| 道具 | 效果 | 备注 |
| --- | --- | --- |
| Remote Trigger | 手动引爆已放置炸弹 | 增加高阶操作空间 |
| Soft Pass | 穿过软墙 | 仅改变路径，不免疫爆炸 |
| Bomb Pass | 穿过炸弹 | 降低自困概率，但仍需判断爆炸时机 |
| Flame Guard | 免疫一次爆炸伤害 | 不免疫敌人接触 |

#### 4.4 道具投放规则

- 每个主线关卡固定隐藏 `1` 个出口
- 每个主线关卡固定隐藏 `1` 个核心成长道具或成长替代奖励
- MVP 的前 `4` 个主线关与首个奖励关不启用战术功能道具
- 从第 `5` 关开始，部分关卡额外隐藏 `1` 个战术功能道具
- 若某项核心成长已达上限，则该位置改为统一的 `10000` 分高分奖励，并在过关结算时发放

#### 4.5 分数与秘密目标

- 分数是副目标，不影响通关
- 敌人击杀按敌人类型提供固定积分
- 奖励关重点提供高分空间
- 主线关可配置“秘密目标”，用于致敬经典隐藏奖励，但规则必须比 FC 原版更易理解
- 首个 MVP 交付版本不启用秘密目标

后续版本可启用的秘密目标类型：

- 无伤通关
- 限时通关
- 少炸弹通关
- 全清软墙后通关

### English

#### 4.1 Player Defaults

| Item | Default | Cap |
| --- | --- | --- |
| lives | 3 | 5 |
| bomb capacity | 1 | 5 |
| flame level | 1 | 5 |
| speed tier | 100% | 145% |

#### 4.2 Enemy Ladder

One of the strongest ideas in [bomber.md](/Users/tony/src/bomberman/docs/bomber.md) is that enemy escalation comes from movement logic, tracking behavior, speed, and wall interaction rather than simple health inflation. This design uses 5 enemy families:

| Enemy | Score | Speed | Behavior Summary | Design Role |
| --- | --- | --- | --- | --- |
| Drifter | 100 | 2.0 tiles/sec | random roaming; only re-evaluates direction on tile-center arrival and turns when blocked | baseline teaching enemy |
| Seeker-Y | 200 | 3.0 tiles/sec | only chases when the player is in the same column; otherwise follows default roaming and only re-decides on tile centers | adds column pressure |
| Seeker-X | 400 | 3.0 tiles/sec | only chases when the player is in the same row; otherwise follows default roaming and only re-decides on tile centers | adds lane pressure |
| Hunter | 800 | 4.0 tiles/sec | at tile centers, prefers directions that reduce Manhattan distance to the player; direct chase when axis-aligned | mid/high-pressure main threat |
| Phantom | 2000 | 2.0 tiles/sec | follows the same chase preference as `Hunter`, but may pass through soft walls only, not hard walls or bombs | rare high-threat enemy |

Additional rule:

- Mainline enemy compositions and core-growth placements are pre-generated during design and then fixed into stage data; restarting the same stage keeps the same result
- if a mainline stage times out or enters excessive stalling, `2` `Punisher` enemies are added to the map
- `Punishers` are high-pressure cleanup units that move at `4.0 tiles/sec`, prefer directions that reduce Manhattan distance on tile-center arrival, and may pass through soft walls only

#### 4.3 Power-Up Layers

Inspired by the classic distinction between long-term stat growth and more fragile special abilities, power-ups are split into two layers:

Core growth items, retained for the rest of the current campaign:

| Power-Up | Effect | Cap |
| --- | --- | --- |
| Bomb Up | +1 bomb capacity | 5 |
| Fire Up | +1 flame length | 5 |
| Skate | +15% move speed | 145% |

Tactical items, lost on death:

| Power-Up | Effect | Notes |
| --- | --- | --- |
| Remote Trigger | manually detonate placed bombs | creates high-skill routing and trapping |
| Soft Pass | move through soft walls | changes route access but does not grant blast immunity |
| Bomb Pass | move through bombs | reduces self-trap risk while preserving timing skill |
| Flame Guard | absorb one explosion hit | does not prevent enemy-contact death |

#### 4.4 Pickup Placement Rules

- every mainline stage hides exactly `1` exit
- every mainline stage hides exactly `1` core growth item or a growth-replacement reward
- the first MVP slice of `4` mainline stages plus the first bonus stage does not enable tactical items
- from stage `5` onward, selected stages may additionally hide `1` tactical item
- if a core-growth category is already capped, that placement becomes a unified `10000-point` score reward paid out during clear results

#### 4.5 Score and Secret Goals

- score is a secondary objective and never blocks completion
- enemy kills grant fixed points by enemy type
- bonus stages are the primary score spikes
- mainline stages may include "secret goals" as a cleaner homage to classic hidden rewards
- the first MVP delivery does not enable secret goals

Allowed post-MVP secret-goal categories:

- no-damage clear
- time-limit clear
- low-bomb clear
- clear after destroying all soft walls

## 5. 内容规划、范围边界与主题区 / Content Plan, Scope Boundaries, and Themed Zones

### 中文

#### 5.1 主题区结构

- `12` 个主线关卡分为 `3` 个主题区
- 每区 `4` 关主线 + `1` 个奖励关

主题区建议：

1. Foundation Maze
   - 教学重点：炸弹逃生、隐藏出口、基础敌人
2. Pressure Maze
   - 教学重点：轴向追踪敌人、路线取舍、奖励关分数驱动
3. Hazard Maze
   - 教学重点：穿墙敌人、复杂资源分配、高压残局

#### 5.2 明确在范围内

- 单人闯关
- 奖励关
- 分数系统
- 隐藏出口
- 分层道具系统
- 5 个敌人家族
- 主菜单、暂停、失败、结算流程
- 桌面端离线体验

#### 5.3 明确不在范围内

- 本地多人对战
- 在线联机
- 角色外观商店
- rogue-lite 元进度
- 技能树
- Boss 战
- 用户地图编辑器
- 排行榜服务端

### English

#### 5.1 Zone Structure

- `12` mainline stages are split into `3` themed zones
- each zone contains `4` main stages + `1` bonus stage

Recommended zone framing:

1. Foundation Maze
   - teaches bomb escape, hidden exits, and basic enemies
2. Pressure Maze
   - teaches axis-based chasers, route tradeoffs, and score-driven bonus-stage pacing
3. Hazard Maze
   - teaches wall-phasing threats, deeper resource allocation, and high-pressure end states

#### 5.2 Explicitly In Scope

- single-player stage progression
- bonus stages
- score system
- hidden exits
- layered power-up system
- 5 enemy families
- main menu, pause, fail, and result flow
- offline desktop experience

#### 5.3 Explicitly Out of Scope

- local multiplayer battle mode
- online multiplayer
- cosmetic shops
- rogue-lite metaprogression
- skill trees
- boss fights
- user-facing map editor
- server-backed leaderboards

## 6. 视觉、音频与交互目标 / Visual, Audio, and Interaction Goals

### 中文

#### 6.1 视觉目标

- 单帧截图即可清楚区分墙体、炸弹、爆炸、敌人、道具和出口
- 不同敌人必须通过颜色、轮廓和移动动画形成明确角色分工
- 炸弹的闪烁节奏必须能被玩家读作“还剩多少时间”
- 战术道具拾取后要有明显的状态提示

#### 6.2 音频目标

- 放弹音：短、准、略带机械感
- 爆炸音：冲击强，但不遮盖后续拾取或敌人音效
- 拾取音：清脆明亮
- 失败音：明确告诉玩家“这一局结束”
- 奖励关音频：整体更轻快，鼓励连杀节奏

#### 6.3 交互目标

- 菜单总层级不超过 3 层
- 死亡后 2 秒内可以重新开始当前关卡
- 暂停界面可直接查看控制说明与道具说明
- 首次教学必须在 60 秒内结束，不阻断玩家自主探索

### English

#### 6.1 Visual Goals

- A single screenshot should clearly distinguish walls, bombs, explosions, enemies, pickups, and exit states
- Different enemy types must be readable through color, silhouette, and motion rhythm
- Bomb blinking should communicate remaining fuse time clearly enough for player timing
- Tactical pickups need an obvious on-screen state indicator once collected

#### 6.2 Audio Goals

- Bomb placement sound: short, precise, slightly mechanical
- Explosion sound: impactful without masking pickup or enemy feedback
- Pickup sound: crisp and bright
- Failure sound: clearly marks the end of the attempt
- Bonus-stage audio: lighter and more energetic to encourage chain kills

#### 6.3 Interaction Goals

- menu depth should not exceed 3 layers
- the player should be able to restart the current stage within 2 seconds of death
- the pause screen should expose controls and pickup explanations directly
- the initial onboarding should end within 60 seconds and not block self-driven exploration

## 7. 面向未来实现的约束 / Constraints for Future Implementation

### 中文

这份文档刻意保持与具体引擎解耦，但未来实现必须遵守以下边界：

- 规则优先于实现便利，不能删除炸弹穿出、连锁爆炸、隐藏出口、奖励关等关键体验
- 任意技术选型都必须支持稳定 tile 逻辑与确定性爆炸传播
- 地图和关卡内容必须数据驱动，便于作者控制与后续扩展
- 视觉表现可以升级，但不能让判定与画面不一致
- 如果未来加入多人模式，应另起设计分支，不得反向污染单人主战役规则

### English

This document intentionally stays engine-agnostic, but future implementation must obey the following boundaries:

- gameplay rules outrank implementation convenience; core experiences such as bomb step-out, chain detonation, hidden exits, and bonus stages must not be removed
- any technology choice must support stable tile logic and deterministic blast propagation
- maps and stage content must be data-driven for authored control and future expansion
- presentation may improve, but visual feedback must stay aligned with actual gameplay rules
- if multiplayer is added later, it should be designed as a separate branch and must not back-drive the single-player campaign rules
