# 大乐透预测技能

根据往期体彩大乐透数据，预测本期大乐透5注号码

## 项目结构

```
lottery-prediction/
├── SKILL.md              # 必需：核心指令文件
├── README.md             # 项目说明文档
├── LICENSE               # 许可证文件
├── scripts/              # 可执行脚本目录
│   ├── data_fetcher.py   # 数据获取模块
│   ├── analyzer.py       # 数据分析模块
│   ├── predictor.py      # 预测生成模块
│   ├── lottery_main.py   # 主程序入口
│   └── requirements.txt  # Python依赖包
├── references/           # 参考文档目录
│   └── api-docs.md      # 数据源API文档
└── assets/              # 静态资源目录
    └── template.json    # 配置模板
```

## 功能介绍

### 1. 数据获取 (data_fetcher.py)
- 从多个在线数据源获取大乐透历史开奖数据
- 支持缓存机制，减少重复请求
- 数据源包括：500彩票网、网易彩票、新浪彩票
- 自动处理网络异常，提供备用数据源

### 2. 数据分析 (analyzer.py)
实现多种分析算法：
- **频率分析**: 统计高频号和低频号
- **区间分析**: 分析各区间号码分布
- **奇偶比分析**: 统计奇数偶数比例
- **和值分析**: 计算号码总和及趋势
- **遗漏分析**: 计算号码遗漏期数

### 3. 预测生成 (predictor.py)
基于分析结果生成预测号码：
- **均衡策略**: 结合高频号和低频号
- **冷热策略**: 侧重高频号码
- **遗漏策略**: 考虑长期遗漏回补
- **区间策略**: 确保区间分布均衡
- **随机策略**: 完全随机生成

## 安装依赖

```bash
pip install -r scripts/requirements.txt
```

## 使用方法

### 基本用法

```bash
# 使用默认设置（分析100期，生成5注预测）
python scripts/lottery_main.py
```

### 高级选项

```bash
# 分析最近150期数据
python scripts/lottery_main.py -p 150

# 生成8注预测
python scripts/lottery_main.py -n 8

# 输出JSON格式
python scripts/lottery_main.py -f json

# 显示详细分析报告
python scripts/lottery_main.py --show-analysis

# 使用缓存数据
python scripts/lottery_main.py --use-cache

# 保存数据到缓存
python scripts/lottery_main.py --save-cache

# 自定义缓存文件
python scripts/lottery_main.py --cache-file my_data.json
```

### 组合使用

```bash
# 分析200期，生成10注，显示详细报告，保存缓存
python scripts/lottery_main.py -p 200 -n 10 --show-analysis --save-cache
```

## 输出示例

### 文本格式输出

```
============================================================
【大乐透预测号码】
============================================================
期次：2026001（最新期次）
分析期数：100 期

推荐5注号码：
第1注：01 08 15 22 29 + 03 09
第2注：05 12 18 25 33 + 04 11
第3注：02 09 16 23 30 + 05 07
第4注：07 14 21 28 35 + 02 08
第5注：04 11 17 24 31 + 06 12

预测依据：
- 高频号前区: ['01', '05', '08', '12', '15']
- 高频号后区: ['03', '07', '09']
- 低频号前区: ['02', '04', '06', '10', '11']
- 平均奇偶比前区: 3:2
- 平均奇偶比后区: 1:1
- 推荐和值范围: 75-125
- 长期遗漏前区: ['13', '19', '26', '32', '34']
- 长期遗漏后区: ['05', '10']

注：仅供娱乐参考，理性投注
============================================================
```

### JSON格式输出

```json
{
  "period": "2026001",
  "analysis_periods": 100,
  "predictions": [
    {
      "front": ["01", "08", "15", "22", "29"],
      "back": ["03", "09"],
      "strategy": "均衡策略"
    }
  ],
  "analysis": {
    "high_frequency_front": ["01", "05", "08", "12", "15"],
    "high_frequency_back": ["03", "07", "09"],
    "low_frequency_front": ["02", "04", "06", "10", "11"],
    "odd_even_ratio_front": "3:2",
    "odd_even_ratio_back": "1:1",
    "sum_value_range": [75, 125]
  },
  "disclaimer": "仅供娱乐参考，理性投注"
}
```

## 命令行参数

| 参数 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| --periods | -p | int | 100 | 分析的期数 |
| --numbers | -n | int | 5 | 生成的预测注数 |
| --format | -f | string | text | 输出格式：text或json |
| --show-analysis | - | flag | false | 显示详细分析报告 |
| --use-cache | - | flag | false | 使用缓存数据 |
| --save-cache | - | flag | false | 保存数据到缓存 |
| --cache-file | - | string | lottery_history.json | 缓存文件路径 |

## 注意事项

1. **免责声明**: 本预测仅供娱乐参考，不保证中奖结果
2. **理性投注**: 请理性对待彩票，量力而行
3. **数据来源**: 历史数据来自公开的彩票网站
4. **网络连接**: 首次运行需要网络连接获取数据
5. **数据更新**: 建议定期更新历史数据

## 开发说明

### 添加新的数据源

在 `data_fetcher.py` 中添加新的数据源方法：

```python
def _fetch_from_new_source(self, source: Dict, count: int) -> Optional[List[Dict]]:
    """从新数据源获取数据"""
    # 实现数据获取逻辑
    pass
```

### 添加新的分析算法

在 `analyzer.py` 中添加新的分析方法：

```python
def custom_analysis(self) -> Dict:
    """自定义分析算法"""
    # 实现分析逻辑
    pass
```

### 添加新的预测策略

在 `predictor.py` 中添加新的预测策略：

```python
def custom_strategy(self, seed: int) -> Dict:
    """自定义预测策略"""
    # 实现预测逻辑
    pass
```

## 常见问题

### Q: 如何更新历史数据？
A: 重新运行程序即可，程序会自动获取最新数据。或者使用 `--save-cache` 参数保存数据。

### Q: 离线模式如何使用？
A: 使用 `--use-cache` 参数，程序会使用之前保存的缓存数据。

### Q: 数据获取失败怎么办？
A: 程序会自动尝试备用数据源，如果都失败会使用模拟数据。也可以手动从网站下载历史数据，使用本地缓存。

### Q: 预测准确率如何？
A: 彩票开奖是随机事件，本工具仅供娱乐参考，不保证任何预测准确率。

## 许可证

MIT License

## 更新日志

### v1.0 (2026-01-25)
- 初始版本
- 实现基础数据获取功能
- 实现5种分析算法
- 实现5种预测策略
- 支持多种输出格式
- 支持缓存机制
