#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大乐透数据分析模块
实现多种分析算法：频率分析、区间分析、奇偶比分析、和值分析、遗漏分析
"""

from typing import List, Dict, Tuple
from collections import Counter, defaultdict
import statistics


class LotteryAnalyzer:
    """大乐透数据分析器"""

    def __init__(self, data: List[Dict]):
        """
        初始化分析器

        Args:
            data: 历史开奖数据列表
        """
        self.data = data
        self.front_range = range(1, 36)  # 前区1-35
        self.back_range = range(1, 13)   # 后区1-12

    def analyze_all(self) -> Dict:
        """
        执行所有分析算法

        Returns:
            包含所有分析结果的字典
        """
        results = {
            'frequency': self.frequency_analysis(),
            'interval': self.interval_analysis(),
            'odd_even': self.odd_even_analysis(),
            'sum_value': self.sum_value_analysis(),
            'miss': self.miss_analysis()
        }
        return results

    def frequency_analysis(self) -> Dict:
        """
        频率分析
        统计每个号码出现的次数和频率

        Returns:
            频率分析结果
        """
        # 前区频率统计
        front_counter = Counter()
        for item in self.data:
            front_counter.update(item['front'])

        # 后区频率统计
        back_counter = Counter()
        for item in self.data:
            back_counter.update(item['back'])

        # 计算频率
        total_periods = len(self.data)
        front_freq = {num: front_counter.get(num, 0) / total_periods for num in self.front_range}
        back_freq = {num: back_counter.get(num, 0) / total_periods for num in self.back_range}

        # 获取高频号（出现次数最多的）
        front_high_freq = sorted(front_counter.items(), key=lambda x: x[1], reverse=True)[:10]
        back_high_freq = sorted(back_counter.items(), key=lambda x: x[1], reverse=True)[:5]

        # 获取低频号（出现次数最少的）
        front_low_freq = sorted(front_counter.items(), key=lambda x: x[1])[:10]
        back_low_freq = sorted(back_counter.items(), key=lambda x: x[1])[:5]

        return {
            'front': {
                'total': dict(front_counter),
                'frequency': front_freq,
                'high_frequency': front_high_freq,
                'low_frequency': front_low_freq
            },
            'back': {
                'total': dict(back_counter),
                'frequency': back_freq,
                'high_frequency': back_high_freq,
                'low_frequency': back_low_freq
            }
        }

    def interval_analysis(self) -> Dict:
        """
        区间分析
        将号码分区，分析各区间的分布规律

        前区：1-35分为7个区间，每区间5个号码
        后区：1-12分为3个区间，每区间4个号码

        Returns:
            区间分析结果
        """
        # 前区分区
        front_intervals = {}
        for i in range(7):
            start = i * 5 + 1
            end = (i + 1) * 5
            front_intervals[f'{start}-{end}'] = list(range(start, end + 1))

        # 后区分区
        back_intervals = {}
        for i in range(3):
            start = i * 4 + 1
            end = (i + 1) * 4
            back_intervals[f'{start}-{end}'] = list(range(start, end + 1))

        # 统计前区区间分布
        front_interval_dist = defaultdict(int)
        for item in self.data:
            for num in item['front']:
                for interval_name, interval_nums in front_intervals.items():
                    if num in interval_nums:
                        front_interval_dist[interval_name] += 1
                        break

        # 统计后区区间分布
        back_interval_dist = defaultdict(int)
        for item in self.data:
            for num in item['back']:
                for interval_name, interval_nums in back_intervals.items():
                    if num in interval_nums:
                        back_interval_dist[interval_name] += 1
                        break

        return {
            'front': {
                'intervals': front_intervals,
                'distribution': dict(front_interval_dist)
            },
            'back': {
                'intervals': back_intervals,
                'distribution': dict(back_interval_dist)
            }
        }

    def odd_even_analysis(self) -> Dict:
        """
        奇偶比分析
        统计奇数和偶数的比例

        Returns:
            奇偶比分析结果
        """
        # 前区奇偶统计
        front_odd_counts = []
        front_even_counts = []
        for item in self.data:
            odd_count = sum(1 for num in item['front'] if num % 2 == 1)
            even_count = 5 - odd_count
            front_odd_counts.append(odd_count)
            front_even_counts.append(even_count)

        # 后区奇偶统计
        back_odd_counts = []
        back_even_counts = []
        for item in self.data:
            odd_count = sum(1 for num in item['back'] if num % 2 == 1)
            even_count = 2 - odd_count
            back_odd_counts.append(odd_count)
            back_even_counts.append(even_count)

        # 统计常见组合
        front_patterns = Counter()
        for odd, even in zip(front_odd_counts, front_even_counts):
            front_patterns[f'{odd}:{even}'] += 1

        back_patterns = Counter()
        for odd, even in zip(back_odd_counts, back_even_counts):
            back_patterns[f'{odd}:{even}'] += 1

        return {
            'front': {
                'avg_odd': statistics.mean(front_odd_counts),
                'avg_even': statistics.mean(front_even_counts),
                'common_patterns': front_patterns.most_common(5)
            },
            'back': {
                'avg_odd': statistics.mean(back_odd_counts),
                'avg_even': statistics.mean(back_even_counts),
                'common_patterns': back_patterns.most_common(3)
            }
        }

    def sum_value_analysis(self) -> Dict:
        """
        和值分析
        计算前区号码的总和及其分布

        Returns:
            和值分析结果
        """
        sum_values = []
        for item in self.data:
            sum_val = sum(item['front'])
            sum_values.append(sum_val)

        # 计算统计信息
        sum_stats = {
            'min': min(sum_values),
            'max': max(sum_values),
            'avg': statistics.mean(sum_values),
            'median': statistics.median(sum_values),
            'std': statistics.stdev(sum_values) if len(sum_values) > 1 else 0
        }

        # 统计常见和值区间
        sum_counter = Counter(sum_values)
        common_sums = sum_counter.most_common(10)

        # 分析和值趋势（最近10期）
        recent_trends = sum_values[-10:]

        return {
            'values': sum_values,
            'statistics': sum_stats,
            'common_sums': common_sums,
            'recent_trends': recent_trends,
            'recommended_range': [
                int(sum_stats['avg'] - sum_stats['std']),
                int(sum_stats['avg'] + sum_stats['std'])
            ]
        }

    def miss_analysis(self) -> Dict:
        """
        遗漏分析
        计算每个号码连续未出现的期数

        Returns:
            遗漏分析结果
        """
        # 前区遗漏统计
        front_miss = {num: 0 for num in self.front_range}
        back_miss = {num: 0 for num in self.back_range}

        # 倒序遍历数据，计算遗漏
        for item in reversed(self.data):
            # 更新前区遗漏
            for num in list(front_miss.keys()):
                if num not in item['front']:
                    front_miss[num] += 1
                else:
                    if front_miss[num] == 0:
                        # 已经出现过，标记为-1表示本期出现
                        front_miss[num] = -1
                    # 如果已经标记过，保持不变

            # 更新后区遗漏
            for num in list(back_miss.keys()):
                if num not in item['back']:
                    back_miss[num] += 1
                else:
                    if back_miss[num] == 0:
                        back_miss[num] = -1

        # 提取长期遗漏的号码（遗漏超过20期）
        front_long_miss = [num for num, miss in front_miss.items() if miss > 20]
        back_long_miss = [num for num, miss in back_miss.items() if miss > 15]

        # 按遗漏次数排序
        front_miss_sorted = sorted(front_miss.items(), key=lambda x: x[1], reverse=True)
        back_miss_sorted = sorted(back_miss.items(), key=lambda x: x[1], reverse=True)

        return {
            'front': {
                'all_miss': front_miss,
                'long_miss': front_long_miss,
                'top_miss': front_miss_sorted[:15]
            },
            'back': {
                'all_miss': back_miss,
                'long_miss': back_long_miss,
                'top_miss': back_miss_sorted[:8]
            }
        }

    def generate_report(self) -> str:
        """
        生成分析报告

        Returns:
            格式化的分析报告
        """
        results = self.analyze_all()

        report = "=" * 60 + "\n"
        report += "大乐透数据分析报告\n"
        report += "=" * 60 + "\n\n"

        # 频率分析
        freq = results['frequency']
        report += "【频率分析】\n"
        report += f"前区高频号: {[f'{x[0]}({x[1]}次)' for x in freq['front']['high_frequency'][:5]]}\n"
        report += f"前区低频号: {[f'{x[0]}({x[1]}次)' for x in freq['front']['low_frequency'][:5]]}\n"
        report += f"后区高频号: {[f'{x[0]}({x[1]}次)' for x in freq['back']['high_frequency'][:3]]}\n"
        report += f"后区低频号: {[f'{x[0]}({x[1]}次)' for x in freq['back']['low_frequency'][:3]]}\n\n"

        # 区间分析
        interval = results['interval']
        report += "【区间分析】\n"
        report += f"前区最热区间: {sorted(interval['front']['distribution'].items(), key=lambda x: x[1], reverse=True)[0]}\n"
        report += f"后区最热区间: {sorted(interval['back']['distribution'].items(), key=lambda x: x[1], reverse=True)[0]}\n\n"

        # 奇偶比分析
        odd_even = results['odd_even']
        report += "【奇偶比分析】\n"
        report += f"前区平均奇偶比: {odd_even['front']['avg_odd']:.1f}:{odd_even['front']['avg_even']:.1f}\n"
        report += f"前区常见组合: {odd_even['front']['common_patterns'][:3]}\n"
        report += f"后区平均奇偶比: {odd_even['back']['avg_odd']:.1f}:{odd_even['back']['avg_even']:.1f}\n\n"

        # 和值分析
        sum_val = results['sum_value']
        report += "【和值分析】\n"
        report += f"和值范围: {sum_val['statistics']['min']} - {sum_val['statistics']['max']}\n"
        report += f"平均和值: {sum_val['statistics']['avg']:.1f}\n"
        report += f"推荐和值范围: {sum_val['recommended_range'][0]} - {sum_val['recommended_range'][1]}\n"
        report += f"常见和值: {[f'{x[0]}({x[1]}次)' for x in sum_val['common_sums'][:5]]}\n\n"

        # 遗漏分析
        miss = results['miss']
        report += "【遗漏分析】\n"
        report += f"前区长期遗漏: {miss['front']['long_miss']}\n"
        report += f"后区长期遗漏: {miss['back']['long_miss']}\n"
        report += "前区最大遗漏:\n"
        for num, m in miss['front']['top_miss'][:10]:
            if m > 0:
                report += f"  {num:02d}号({m}期未出) "

        report += "\n"

        return report


if __name__ == '__main__':
    # 测试数据分析
    from data_fetcher import LotteryDataFetcher

    fetcher = LotteryDataFetcher()
    data = fetcher.fetch_history(100)

    if data:
        analyzer = LotteryAnalyzer(data)
        results = analyzer.analyze_all()
        print(analyzer.generate_report())
