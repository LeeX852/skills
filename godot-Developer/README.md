# Godot Developer Skills & Agents

基于 Godot Engine 4.6 官方文档生成的完整游戏开发技能和AI代理系统。

## 📁 目录结构

```
.omc/
├── skills/
│   └── godot-dev/          # Godot开发技能集
│       ├── index.md        # 技能索引
│       ├── gdscript.md     # GDScript编程
│       ├── nodes-and-scenes.md  # 节点与场景
│       ├── physics.md      # 物理系统
│       ├── animation.md    # 动画系统
│       ├── shaders.md      # 着色器
│       ├── 2d-development.md   # 2D开发
│       ├── 3d-development.md   # 3D开发
│       ├── ui-system.md    # UI系统
│       ├── audio.md        # 音频系统
│       ├── input-system.md # 输入系统
│       ├── navigation.md   # 导航系统
│       ├── state-machine.md    # 状态机模式
│       └── export-deploy.md    # 导出部署
└── agents/
    └── index.md            # 代理索引
        ├── godot-developer.md      # 全栈开发代理
        ├── godot-2d-expert.md      # 2D专家
        ├── godot-3d-expert.md      # 3D专家
        ├── godot-ui-expert.md      # UI专家
        ├── godot-ai-expert.md      # AI专家
        ├── godot-networking-expert.md  # 网络专家
        └── godot-optimization-expert.md # 优化专家
```

## 🎮 Skills 技能列表

### 核心开发
| 技能 | 描述 | 文件 |
|------|------|------|
| GDScript | GDScript编程语言基础 | `gdscript.md` |
| Nodes & Scenes | 节点和场景系统 | `nodes-and-scenes.md` |
| Input System | 输入处理和映射 | `input-system.md` |

### 图形渲染
| 技能 | 描述 | 文件 |
|------|------|------|
| 2D Development | 2D游戏开发 | `2d-development.md` |
| 3D Development | 3D游戏开发 | `3d-development.md` |
| Shaders | 着色器编程 | `shaders.md` |
| Animation | 动画系统 | `animation.md` |

### 物理与移动
| 技能 | 描述 | 文件 |
|------|------|------|
| Physics | 物理系统 | `physics.md` |
| Navigation | 导航和寻路 | `navigation.md` |

### 游戏系统
| 技能 | 描述 | 文件 |
|------|------|------|
| UI System | UI开发 | `ui-system.md` |
| Audio | 音频系统 | `audio.md` |
| State Machine | 状态机模式 | `state-machine.md` |

### 部署
| 技能 | 描述 | 文件 |
|------|------|------|
| Export & Deploy | 导出和部署 | `export-deploy.md` |

## 🤖 Agents 代理列表

### 通用代理
- **godot-developer** - 全栈Godot开发代理，处理所有游戏系统

### 专业代理
- **godot-2d-expert** - 2D游戏开发专家
- **godot-3d-expert** - 3D游戏开发专家
- **godot-ui-expert** - UI/UX设计和实现专家
- **godot-ai-expert** - 游戏AI和NPC行为专家
- **godot-networking-expert** - 多人游戏和网络专家
- **godot-optimization-expert** - 性能优化专家

## 📚 文档来源

所有技能和代理基于 `references/` 目录中的 Godot Engine 4.6 官方文档：

- `references/getting_started/` - 入门教程
- `references/tutorials/` - 各类教程
- `references/classes/` - 类参考文档 (1066个类)
- `references/about/` - 关于Godot的信息

## 🚀 使用方法

### 使用技能
技能提供代码模式、最佳实践和常见任务的示例。

### 使用代理
根据任务类型选择合适的代理：
- 通用开发 → `godot-developer`
- 2D游戏 → `godot-2d-expert`
- 3D游戏 → `godot-3d-expert`
- UI设计 → `godot-ui-expert`
- AI系统 → `godot-ai-expert`
- 网络多人 → `godot-networking-expert`
- 性能优化 → `godot-optimization-expert`

## 📖 技能内容示例

每个技能文件包含：
1. **描述** - 技能概述
2. **触发条件** - 何时使用该技能
3. **代码示例** - 实用的GDScript代码
4. **最佳实践** - 推荐的开发方式
5. **常见模式** - 常用的实现方式

## 🔧 自定义和扩展

可以根据项目需求：
- 添加新的技能文件
- 创建新的专业代理
- 扩展现有技能内容
- 添加项目特定的模式

---

*基于 Godot Engine 4.6 官方文档自动生成*
*生成时间: 2026-06-17*
