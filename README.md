# Skills 技能集合

持续更新的实用技能和AI代理集合，涵盖游戏开发、数据分析等领域。

## 📁 项目结构

```
skills/
├── godot-Developer/          # Godot游戏开发技能与AI代理
│   ├── skills/              # 开发技能集
│   ├── agents/              # AI代理系统
│   └── references/          # 参考文档
├── lottery-prediction/       # 大乐透预测技能
│   ├── scripts/             # Python脚本
│   ├── references/          # API文档
│   └── assets/              # 配置资源
├── LICENSE                   # MIT许可证
└── README.md                 # 本文件
```

## 🎮 Godot Developer

基于 Godot Engine 4.6 官方文档生成的完整游戏开发技能和AI代理系统。

### 技能模块

| 分类 | 技能 | 说明 |
|------|------|------|
| **核心开发** | GDScript、Nodes & Scenes、Input System | 基础开发能力 |
| **图形渲染** | 2D/3D Development、Shaders、Animation | 视觉呈现 |
| **物理系统** | Physics、Navigation | 物理模拟与寻路 |
| **游戏系统** | UI System、Audio、State Machine | 游戏功能模块 |
| **部署** | Export & Deploy | 项目导出与发布 |

### AI代理

| 代理 | 专长 |
|------|------|
| godot-developer | 全栈Godot开发 |
| godot-2d-expert | 2D游戏开发 |
| godot-3d-expert | 3D游戏开发 |
| godot-ui-expert | UI/UX设计 |
| godot-ai-expert | 游戏AI与NPC行为 |
| godot-networking-expert | 多人游戏网络 |
| godot-optimization-expert | 性能优化 |

📖 **详细文档**: [godot-Developer/README.md](godot-Developer/README.md)

## 🎰 Lottery Prediction

基于历史数据的大乐透号码预测工具。

### 功能特性

- **数据获取** - 从多个在线数据源获取历史开奖数据
- **智能分析** - 频率、区间、奇偶比、和值、遗漏等多维度分析
- **多种策略** - 均衡、冷热、遗漏、区间、随机等预测策略
- **缓存机制** - 支持本地数据缓存，减少网络请求
- **灵活输出** - 支持文本和JSON格式输出

### 快速开始

```bash
cd lottery-prediction

# 安装依赖
pip install -r scripts/requirements.txt

# 运行预测（默认分析100期，生成5注）
python scripts/lottery_main.py

# 高级用法
python scripts/lottery_main.py -p 150 -n 8 --show-analysis
```

📖 **详细文档**: [lottery-prediction/README.md](lottery-prediction/README.md)

## 🚀 使用指南

### 作为Claude Code技能使用

这些技能设计为与 Claude Code 配合使用：

1. **Godot开发** - 在Godot项目中使用对应的技能和代理
2. **彩票预测** - 直接运行Python脚本获取预测结果

### 克隆仓库

```bash
git clone <repository-url>
cd skills
```

## 📚 文档来源

- **Godot技能** - 基于 Godot Engine 4.6 官方文档
- **彩票预测** - 基于公开的彩票历史数据API

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 添加新技能

1. 在对应目录创建新的技能文件
2. 更新目录中的 README.md
3. 提交 Pull Request

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

## ⚠️ 免责声明

- 彩票预测功能仅供娱乐参考，不保证中奖结果
- 请理性对待彩票，量力而行
- 本项目不构成任何投资建议

---

**持续更新中...**

*最后更新: 2026-06-17*