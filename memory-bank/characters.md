# Bomberman 游戏 AI 图片生成提示词

## 📁 地图元素

### 1. 地板 (Floor）
```
Classic arcade game floor tile, dark metallic gray steel plate with subtle grid pattern, industrial sci-fi dungeon aesthetic, pixel art style, 64x64 pixels, clean sharp edges, seamless tileable, centered composition
```

### 2. 硬墙 (Hard Wall)
```
Solid reinforced concrete block wall, dark charcoal gray stone bricks, industrial bunker military style, subtle 3D depth with highlights on top edges and shadows on bottom, pixel art style, 64x64 pixels, classic arcade bomberman game aesthetic, transparent background, centered
```

### 3. 软墙 (Soft Wall / Destructible Crate)
```
Destructible wooden crate box, light tan beige wooden planks texture, aged worn rustic look, treasure chest style breakable block, pixel art style, 64x64 pixels, classic arcade bomberman game aesthetic, transparent background, centered
```

### 4. 出口 (Exit / Portal)
```
Glowing green neon portal exit door, bright lime green energy swirl, inviting victory escape route, subtle pulsing glow effect, pixel art style, 64x64 pixels, classic arcade game aesthetic, transparent background, centered
```

---

## 🎮 角色与道具

### 5. 玩家 (Player)
```
Cute pixel art robot bomberman character, round blue metallic body, friendly face with antenna on top, simple 8-bit style, classic arcade game protagonist, transparent background, 64x64 pixels, centered composition
```

### 6. 敌人 - Drifter
```
Cute but dangerous pixel art enemy slime robot, rounded red-orange body, single bright eye, simple patrol monster silhouette, low-tier arcade bomberman enemy, easy to read shape, transparent background, 64x64 pixels, centered composition
```

### 7. 敌人 - Seeker-Y
```
Classic arcade pixel art enemy drone, tall narrow yellow body with vertical stripe markings, scanning eye facing forward, design emphasizes vertical pursuit behavior, readable silhouette, transparent background, 64x64 pixels, centered composition
```

### 8. 敌人 - Seeker-X
```
Classic arcade pixel art enemy drone, wide flat orange body with horizontal stripe markings, sharp side-facing eyes, design emphasizes horizontal pursuit behavior, readable silhouette, transparent background, 64x64 pixels, centered composition
```

### 9. 敌人 - Hunter
```
Aggressive pixel art hunter robot enemy, angular crimson armor, glowing red visor, fast deadly chaser, compact but threatening arcade bomberman monster, strong silhouette clarity, transparent background, 64x64 pixels, centered composition
```

### 10. 敌人 - Phantom
```
Ghost-like pixel art phantom enemy, pale cyan translucent body, floating mask face, eerie soft glow, can phase through destructible walls, rare high-threat arcade bomberman monster, transparent background, 64x64 pixels, centered composition
```

### 11. 敌人 - Punisher
```
Elite pixel art punisher enemy, dark black-purple armored demon robot, piercing neon magenta eyes, relentless endgame pursuer, intimidating high-pressure arcade bomberman monster, bold silhouette, transparent background, 64x64 pixels, centered composition
```

### 12. 炸弹 (Bomb)
```
Classic black spherical bomb with lit fuse, orange glowing spark on top, dark red accent color, round 3D shading, pixel art style, 64x64 pixels, classic arcade bomberman game item, transparent background, centered
```

### 13. 火焰 (Explosion Flame)
```
Dynamic explosion fire burst, bright orange yellow flames, cartoon fire effect, power-up fire style, animated sprite feel, pixel art style, 64x64 pixels, classic arcade bomberman game explosion, transparent background, centered
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

## 💡 使用说明

| 工具 | 使用方式 |
|------|----------|
| **DALL-E** | 直接粘贴提示词，可加 ", pixel art" 更强调像素风格 |
| **Midjourney** | 提示词 + `--pixelart --style` 参数 |
| **Stable Diffusion** | 提示词，Negative prompt: "photorealistic, 3d render, blurry" |

**推荐分辨率**: 64x64 或 128x128 像素（2x 放大）

**保存格式**: PNG with transparency (除地板外)
