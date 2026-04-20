# Bomberman 角色图片生成提示词

本文件把角色图片生成从“单条灵感提示词”升级为“可复用的角色提示词系统”。
目标是先稳定生成主角，再用同一套规则扩展敌人、NPC、皮肤和不同动作帧。

---

## 🎯 角色风格总纲

### 1. 视觉定位

- 类型：经典街机俯视角动作迷宫游戏角色
- 风格：可爱、清晰、易读的像素风机器人吉祥物
- 用途：游戏内精灵，不是海报，不是插画，不是场景概念图
- 重点：小尺寸下依然能一眼认出轮廓、颜色和表情

### 2. 主角身份锚点

以下特征在所有主角图中都应尽量保持稳定：

- 主体是蓝色圆润机器人，不是人类，不是写实机甲
- 轮廓短小、结实、可爱，头身比例偏 Q 版
- 面部区域简单清楚，优先使用单一面罩或大面积脸部显示区
- 顶部保留一个“天线 / 引信感”的标志性结构
- 气质友好、机警、带一点街机英雄感

### 3. 像素表现约束

- 单角色、居中构图、透明背景
- 正面或接近正面的游戏精灵视角，避免强透视
- 形体尽量由大色块组成，不要依赖细碎纹理表达
- 控制在 3 到 5 个主要色块族群内
- 阴影简洁，边缘清晰，适合后续缩放到 `64x64`
- 可以先生成更高分辨率版本，再人工缩放到最终精灵尺寸

### 4. 明确避免

以下内容会明显降低可用性，应直接写进提示词：

- 不要场景背景，不要地面，不要 UI，不要文字
- 不要多角色同屏，不要道具堆满画面
- 不要写实金属、复杂反光、电影级灯光
- 不要厚重笔触、插画感、概念设定图感
- 不要侧身奔跑透视，不要夸张动态镜头
- 不要过密零件、过多电缆、过强表面噪声

---

## 🤖 OpenAI 角色生成工作流

### 推荐用法

1. 先使用“角色风格总纲 + 具体角色提示词”生成基础版本
2. 选出轮廓最清楚、颜色最稳定的一版作为角色基准
3. 后续生成敌人或变体时，固定相同的风格总纲，只替换角色描述字段
4. 最终导出时保留透明背景，并缩放到目标精灵尺寸

### 推荐补充语句

可在提示词末尾附加以下控制语句：

```text
single character sprite, centered composition, transparent background, front-facing game sprite, readable silhouette, minimal detail noise, crisp pixel-art shapes
```

### OpenAI 使用要点

- 优先把需求写成“游戏精灵约束”，不要写成“概念图气氛”
- 先强调“单角色精灵可读性”，再补充材质和性格
- 如果生成结果太像插画，就加强“flat sprite readability / no background / minimal detail”
- 如果生成结果太写实，就加强“cute arcade pixel-art robot mascot / simplified shapes / restrained shading”

---

## 🧩 可复用角色提示词模板

把下面模板作为未来所有角色的基础骨架：

```text
Cute arcade pixel-art [角色类型] character sprite for a top-down action maze game, [轮廓描述], [主色] body with [辅色] accents, [标志性配件], [面部描述], [气质描述], front-facing or near front-facing game sprite, single character only, centered composition, transparent background, readable silhouette, large simple shapes, restrained shading, minimal texture noise, no environment, no text, no UI, no extra props, designed to read clearly as a 64x64 sprite
```

### 模板字段说明

- `[角色类型]`：player robot / scout enemy / brute enemy / support bot
- `[轮廓描述]`：round compact body / tall narrow silhouette / squat heavy silhouette
- `[主色]`：blue / red-orange / toxic green / black-yellow
- `[辅色]`：white / silver / orange / cyan
- `[标志性配件]`：small antenna / fuse-like topper / visor horns / single eye lens
- `[面部描述]`：friendly visor face / angry square eyes / single glowing eye
- `[气质描述]`：brave and alert / sneaky and fast / heavy and dangerous

---

## ⭐ 主角基准提示词

这是当前项目的主角默认版本，优先用于生成玩家角色基准图。

```text
Cute arcade pixel-art robot bomber hero character sprite for a top-down action maze game, compact round blue robot body with white and dark navy accents, one small fuse-like antenna on top, simple friendly visor face, brave and alert expression, charming mascot energy, front-facing game sprite, single character only, centered composition, transparent background, highly readable silhouette, large simple shapes, restrained shading, minimal texture noise, no environment, no text, no UI, no extra props, not a concept art illustration, designed to read clearly as a 64x64 sprite
```

### 中文意图说明

- 蓝色是主识别色，不能漂成紫色或青灰色
- 身体应偏圆润，不要变成人形战甲或高达风
- 表情应友好但可靠，不要呆滞，也不要邪恶
- 天线是识别点之一，尽量保留
- 重心是“街机主角精灵”，不是“高细节机器人立绘”

### 如果结果偏掉，可追加修正

#### 太像插画

```text
game sprite only, no illustration background, simplified sprite design, flat readable shape language
```

#### 太像写实机甲

```text
cute mascot robot, simplified toy-like proportions, minimal mechanical detail, no realistic metal rendering
```

#### 太花太碎

```text
reduce surface detail, fewer texture lines, broader color blocks, cleaner silhouette
```

#### 角度太斜

```text
front-facing sprite, symmetric game character presentation, avoid dramatic perspective
```

---

## 🧪 后续角色扩展建议

后续新增敌人时，不要重写整套风格，只替换这几个维度：

- 轮廓：轻型、重型、狡猾型、爆发型
- 主色：避免与主角蓝色过近
- 面部情绪：敌意、阴险、呆萌、狂暴
- 标志配件：角、单眼、履带脚、尖刺帽、警报灯

建议保持不变的部分：

- 透明背景
- 单角色居中
- 适合 `64x64` 精灵阅读
- 简洁阴影和大色块
- 街机像素风而非写实插画

---

## 📁 其余资源快速提示词

以下保留为环境和道具的快速参考词，方便与角色风格配套使用。

### 1. 地板 (Floor)

```text
Classic arcade game floor tile, dark metallic gray steel plate with subtle grid pattern, industrial sci-fi dungeon aesthetic, pixel art style, 64x64 pixels, clean sharp edges, seamless tileable, centered composition
```

### 2. 硬墙 (Hard Wall)

```text
Solid reinforced concrete block wall, dark charcoal gray stone bricks, industrial bunker military style, subtle 3D depth with highlights on top edges and shadows on bottom, pixel art style, 64x64 pixels, classic arcade bomberman game aesthetic, transparent background, centered
```

### 3. 软墙 (Soft Wall / Destructible Crate)

```text
Destructible wooden crate box, light tan beige wooden planks texture, aged worn rustic look, treasure chest style breakable block, pixel art style, 64x64 pixels, classic arcade bomberman game aesthetic, transparent background, centered
```

### 4. 出口 (Exit / Portal)

```text
Glowing green neon portal exit door, bright lime green energy swirl, inviting victory escape route, subtle pulsing glow effect, pixel art style, 64x64 pixels, classic arcade game aesthetic, transparent background, centered
```

### 5. 炸弹 (Bomb)

```text
Classic black spherical bomb with lit fuse, orange glowing spark on top, dark red accent color, round 3D shading, pixel art style, 64x64 pixels, classic arcade bomberman game item, transparent background, centered
```

### 6. 火焰 (Explosion Flame)

```text
Dynamic explosion fire burst, bright orange yellow flames, cartoon fire effect, power-up fire style, animated sprite feel, pixel art style, 64x64 pixels, classic arcade bomberman game explosion, transparent background, centered
```

### 7. 敌人 - Drifter

```text
Cute but dangerous pixel art enemy slime robot, rounded red-orange body, single bright eye, simple patrol monster silhouette, low-tier arcade bomberman enemy, easy to read shape, transparent background, 64x64 pixels, centered composition
```

### 8. 敌人 - Seeker-Y

```text
Classic arcade pixel art enemy drone, tall narrow yellow body with vertical stripe markings, scanning eye facing forward, design emphasizes vertical pursuit behavior, readable silhouette, transparent background, 64x64 pixels, centered composition
```

### 9. 敌人 - Seeker-X

```text
Classic arcade pixel art enemy drone, wide flat orange body with horizontal stripe markings, sharp side-facing eyes, design emphasizes horizontal pursuit behavior, readable silhouette, transparent background, 64x64 pixels, centered composition
```

### 10. 敌人 - Hunter

```text
Aggressive pixel art hunter robot enemy, angular crimson armor, glowing red visor, fast deadly chaser, compact but threatening arcade bomberman monster, strong silhouette clarity, transparent background, 64x64 pixels, centered composition
```

### 11. 敌人 - Phantom

```text
Ghost-like pixel art phantom enemy, pale cyan translucent body, floating mask face, eerie soft glow, can phase through destructible walls, rare high-threat arcade bomberman monster, transparent background, 64x64 pixels, centered composition
```

### 12. 敌人 - Punisher

```text
Elite pixel art punisher enemy, dark black-purple armored demon robot, piercing neon magenta eyes, relentless endgame pursuer, intimidating high-pressure arcade bomberman monster, bold silhouette, transparent background, 64x64 pixels, centered composition
```

---

## 单张生成版提示词

### 通用附加约束

每条提示词建议在网页端生成时追加下面这段，提升“程序友好”的稳定性：

```text
pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

如果网页端透明背景效果不稳定，可改为纯色抠图底：

```text
perfectly flat solid #00ff00 background only, no gradient, no shadow, no texture
```

### 1. Floor
```text
Bomberman-style floor tile, dark metallic gray steel plate with subtle grid pattern, industrial arcade dungeon aesthetic, top-down readable tile, seamless-looking single tile, pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 2. Hard Wall
```text
Bomberman-style hard wall tile, solid reinforced concrete block, dark charcoal gray stone bricks, sturdy bunker look, slight top highlight and bottom shadow for depth, top-down readable tile, pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 3. Soft Wall
```text
Bomberman-style destructible soft wall tile, wooden crate block made of light tan worn planks, breakable arcade obstacle, compact readable shape, top-down readable tile, pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 4. Exit
```text
Bomberman-style exit tile, glowing green portal door with bright lime energy swirl, clear victory destination, arcade readable silhouette, top-down readable tile, pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 5. Player
```text
Cute robot bomberman player character, round blue metallic body, friendly face, small antenna on top, simple heroic arcade protagonist silhouette, top-down readable pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 6. Drifter
```text
Cute but dangerous enemy slime robot, rounded red-orange body, single bright eye, simple low-tier patrol monster silhouette, easy to read arcade enemy, top-down readable pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 7. Seeker-Y
```text
Arcade enemy drone, tall narrow yellow body with vertical stripe markings, scanning eye facing forward, design emphasizes vertical pursuit, clear readable silhouette, top-down readable pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 8. Seeker-X
```text
Arcade enemy drone, wide flat orange body with horizontal stripe markings, sharp side-facing eyes, design emphasizes horizontal pursuit, clear readable silhouette, top-down readable pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 9. Hunter
```text
Aggressive hunter robot enemy, angular crimson armor, glowing red visor, fast deadly chaser, compact but threatening arcade monster silhouette, top-down readable pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 10. Phantom
```text
Ghost-like phantom enemy, pale cyan translucent body, floating mask face, eerie soft glow, rare high-threat wall-phasing monster, clear readable silhouette, top-down readable pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 11. Punisher
```text
Elite punisher enemy, dark black armored demon robot with neon magenta eyes, relentless endgame pursuer, intimidating high-pressure arcade monster, bold readable silhouette, top-down readable pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 12. Bomb
```text
Classic round black bomb with short lit fuse, small orange spark, dark red accent shading, iconic arcade explosive item, compact readable silhouette, top-down readable pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 13. Flame
```text
Cross-shaped bomberman explosion flame, bright orange and yellow fire burst, energetic arcade blast effect, compact readable shape for a single tile, top-down readable pixel art game sprite, transparent background, one centered subject only, square composition, clean readable silhouette, no text, no border, no decorative frame, no scene background, no floor plane, no cast shadow, no extra objects
```

### 14. Empty Transparent Tile

不建议用 AI 生成，直接制作一张 `64x64` 的全透明 PNG 最稳。

如需临时占位提示词，可用：

```text
completely empty transparent game sprite tile, no subject, no object, no text, no border, no shadow, no frame, pure transparent background only
```

---

## 💡 工具使用说明

| 工具 | 使用方式 |
|------|----------|
| **OpenAI Images** | 以“角色风格总纲 + 具体角色提示词”为主，优先生成单角色透明背景版本 |
| **Midjourney** | 使用同一角色骨架，但需额外强化 `sprite`, `front-facing`, `no background` 约束 |
| **Stable Diffusion** | 使用主提示词，并加入 Negative prompt：`photorealistic, concept art, detailed background, multiple characters, text, UI, dramatic perspective, blurry` |

**推荐生成策略**：先出高分辨率候选图，再筛选并缩放到 `64x64` 或 `128x128` 精灵尺寸。

**保存格式**：`PNG with transparency`（地板可按平铺素材单独处理）。
