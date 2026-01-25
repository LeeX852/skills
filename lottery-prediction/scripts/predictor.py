#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大乐透预测模块
基于历史数据分析结果，生成预测号码
"""

import random
from typing import List, Dict, Tuple


class LotteryPredictor:
    """大乐透预测器"""

    def __init__(self, analysis_results: Dict):
        """
        初始化预测器

        Args:
            analysis_results: 数据分析结果
        """
        self.analysis = analysis_results

    def predict(self, count: int = 5) -> List[Dict]:
        """
        生成预测号码

        Args:
            count: 生成注数，默认5注

        Returns:
            预测号码列表，每注包含前区和后区号码
        """
        predictions = []

        # 多种策略生成预测
        strategies = [
            self._balanced_strategy,
            self._hot_cold_strategy,
            self._miss_strategy,
            self._interval_strategy,
            self._random_strategy
        ]

        for i in range(count):
            strategy = strategies[i % len(strategies)]
            prediction = strategy(i)
            predictions.append(prediction)

        return predictions

    def _balanced_strategy(self, seed: int) -> Dict:
        """
        均衡策略
        结合高频号和低频号，保持均衡

        Args:
            seed: 随机种子

        Returns:
            预测号码
        """
        random.seed(seed)

        # 前区：从高频号选2个，低频号选2个，随机选1个
        freq = self.analysis['frequency']
        high_front = [x[0] for x in freq['front']['high_frequency'][:15]]
        low_front = [x[0] for x in freq['front']['low_frequency'][:15]]

        front_high = random.sample(high_front, 2)
        front_low = random.sample(low_front, 2)
        front_random = random.sample([n for n in range(1, 36)
                                     if n not in front_high and n not in front_low], 1)

        front = sorted(front_high + front_low + front_random)

        # 后区：从高频号选1个，随机选1个
        high_back = [x[0] for x in freq['back']['high_frequency'][:8]]
        back_high = random.choice(high_back)
        back_random = random.choice([n for n in range(1, 13) if n != back_high])

        back = sorted([back_high, back_random])

        return {
            'front': front,
            'back': back,
            'strategy': '均衡策略'
        }

    def _hot_cold_strategy(self, seed: int) -> Dict:
        """
        冷热策略
        侧重于高频号码

        Args:
            seed: 随机种子

        Returns:
            预测号码
        """
        random.seed(seed)

        freq = self.analysis['frequency']
        high_front = [x[0] for x in freq['front']['high_frequency'][:20]]
        high_back = [x[0] for x in freq['back']['high_frequency'][:10]]

        # 前区主要从高频号中选
        front = sorted(random.sample(high_front, 5))

        # 后区从高频号中选
        back = sorted(random.sample(high_back, 2))

        return {
            'front': front,
            'back': back,
            'strategy': '冷热策略'
        }

    def _miss_strategy(self, seed: int) -> Dict:
        """
        遗漏策略
        考虑长期遗漏号码的回补

        Args:
            seed: 随机种子

        Returns:
            预测号码
        """
        random.seed(seed)

        miss = self.analysis['miss']
        freq = self.analysis['frequency']

        # 前区：从长期遗漏号中选2个，从高频号中选3个
        front_miss = miss['front']['long_miss']
        high_front = [x[0] for x in freq['front']['high_frequency'][:15]]

        if len(front_miss) >= 2:
            front_miss_selected = random.sample(front_miss, 2)
        else:
            front_miss_selected = front_miss + random.sample(
                [n for n in range(1, 36) if n not in front_miss and n not in high_front],
                2 - len(front_miss)
            )

        front_high = random.sample([n for n in high_front if n not in front_miss_selected], 3)

        front = sorted(front_miss_selected + front_high)

        # 后区：从遗漏号中选1个，从高频号中选1个
        back_miss = miss['back']['long_miss']
        high_back = [x[0] for x in freq['back']['high_frequency'][:8]]

        if back_miss:
            back_miss_selected = random.choice(back_miss)
            back_high = random.choice([n for n in high_back if n != back_miss_selected])
        else:
            back_miss_selected = random.choice(range(1, 13))
            back_high = random.choice([n for n in high_back if n != back_miss_selected])

        back = sorted([back_miss_selected, back_high])

        return {
            'front': front,
            'back': back,
            'strategy': '遗漏策略'
        }

    def _interval_strategy(self, seed: int) -> Dict:
        """
        区间策略
        确保号码分布在不同区间

        Args:
            seed: 随机种子

        Returns:
            预测号码
        """
        random.seed(seed)

        interval = self.analysis['interval']

        # 前区：从不同区间各选1个号码（前5个区间各选1个）
        front = []
        selected_intervals = random.sample(list(interval['front']['intervals'].keys()), 5)

        for interval_name in selected_intervals:
            interval_nums = interval['front']['intervals'][interval_name]
            front.append(random.choice(interval_nums))

        front = sorted(front)

        # 后区：从不同区间各选1个号码（前2个区间各选1个）
        back_intervals = random.sample(list(interval['back']['intervals'].keys()), 2)
        back = []
        for interval_name in back_intervals:
            interval_nums = interval['back']['intervals'][interval_name]
            back.append(random.choice(interval_nums))

        back = sorted(back)

        return {
            'front': front,
            'back': back,
            'strategy': '区间策略'
        }

    def _random_strategy(self, seed: int) -> Dict:
        """
        随机策略
        完全随机选择号码

        Args:
            seed: 随机种子

        Returns:
            预测号码
        """
        random.seed(seed)

        # 前区：随机选择5个不重复号码
        front = sorted(random.sample(range(1, 36), 5))

        # 后区：随机选择2个不重复号码
        back = sorted(random.sample(range(1, 13), 2))

        return {
            'front': front,
            'back': back,
            'strategy': '随机策略'
        }

    def validate_prediction(self, prediction: Dict) -> bool:
        """
        验证预测号码是否有效

        Args:
            prediction: 预测号码

        Returns:
            是否有效
        """
        # 检查前区
        if len(prediction['front']) != 5:
            return False
        if len(set(prediction['front'])) != 5:
            return False
        if not all(1 <= num <= 35 for num in prediction['front']):
            return False

        # 检查后区
        if len(prediction['back']) != 2:
            return False
        if len(set(prediction['back'])) != 2:
            return False
        if not all(1 <= num <= 12 for num in prediction['back']):
            return False

        return True

    def format_prediction(self, prediction: Dict, index: int) -> str:
        """
        格式化预测号码输出

        Args:
            prediction: 预测号码
            index: 注数编号

        Returns:
            格式化字符串
        """
        front_str = ' '.join(f'{num:02d}' for num in prediction['front'])
        back_str = ' '.join(f'{num:02d}' for num in prediction['back'])

        return f"第{index + 1}注：{front_str} + {back_str} [{prediction['strategy']}]"

    def generate_summary(self, predictions: List[Dict]) -> str:
        """
        生成预测摘要

        Args:
            predictions: 预测号码列表

        Returns:
            摘要字符串
        """
        freq = self.analysis['frequency']
        odd_even = self.analysis['odd_even']
        sum_val = self.analysis['sum_value']
        miss = self.analysis['miss']

        summary = "\n预测依据：\n"

        # 高频号和低频号
        summary += f"- 高频号前区: {[f'{x[0]:02d}' for x in freq['front']['high_frequency'][:5]]}\n"
        summary += f"- 高频号后区: {[f'{x[0]:02d}' for x in freq['back']['high_frequency'][:3]]}\n"
        summary += f"- 低频号前区: {[f'{x[0]:02d}' for x in freq['front']['low_frequency'][:5]]}\n"

        # 奇偶比
        summary += f"- 平均奇偶比前区: {odd_even['front']['avg_odd']:.0f}:{odd_even['front']['avg_even']:.0f}\n"
        summary += f"- 平均奇偶比后区: {odd_even['back']['avg_odd']:.0f}:{odd_even['back']['avg_even']:.0f}\n"

        # 和值
        summary += f"- 推荐和值范围: {sum_val['recommended_range'][0]}-{sum_val['recommended_range'][1]}\n"

        # 遗补号码
        if miss['front']['long_miss']:
            summary += f"- 长期遗漏前区: {[f'{x:02d}' for x in miss['front']['long_miss'][:5]]}\n"
        if miss['back']['long_miss']:
            summary += f"- 长期遗漏后区: {[f'{x:02d}' for x in miss['back']['long_miss'][:3]]}\n"

        return summary


if __name__ == '__main__':
    # 测试预测
    from data_fetcher import LotteryDataFetcher
    from analyzer import LotteryAnalyzer

    fetcher = LotteryDataFetcher()
    data = fetcher.fetch_history(100)

    if data:
        analyzer = LotteryAnalyzer(data)
        results = analyzer.analyze_all()

        predictor = LotteryPredictor(results)
        predictions = predictor.predict(5)

        print("\n推荐5注号码：")
        for i, pred in enumerate(predictions):
            print(predictor.format_prediction(pred, i))

        print(predictor.generate_summary(predictions))
