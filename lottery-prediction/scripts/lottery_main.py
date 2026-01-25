#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大乐透预测主程序
整合数据获取、分析和预测功能
"""

import argparse
import sys
import json
from pathlib import Path
import io

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

# 设置标准输出编码为UTF-8（兼容Windows终端）
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# 重定向标准输出到支持UTF-8的包装器
class UTF8Stdout:
    def __init__(self, stream):
        self.stream = stream
        self.encoding = 'utf-8'

    def write(self, text):
        if isinstance(text, str):
            try:
                self.stream.buffer.write(text.encode(self.encoding))
            except:
                # 兜底方案
                self.stream.write(text)
        else:
            self.stream.write(text)

    def flush(self):
        self.stream.flush()

# 替换标准输出
sys.stdout = UTF8Stdout(sys.stdout)

from data_fetcher import LotteryDataFetcher
from analyzer import LotteryAnalyzer
from predictor import LotteryPredictor


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='大乐透号码预测工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python lottery_main.py                    # 使用默认设置预测
  python lottery_main.py -p 150            # 分析最近150期
  python lottery_main.py -n 8              # 生成8注预测
  python lottery_main.py -f json           # 输出JSON格式
  python lottery_main.py --show-analysis   # 显示详细分析
  python lottery_main.py --use-cache       # 使用缓存数据
  python lottery_main.py --save-cache      # 保存数据到缓存
        '''
    )

    parser.add_argument(
        '-p', '--periods',
        type=int,
        default=100,
        help='分析的期数（默认：100）'
    )

    parser.add_argument(
        '-n', '--numbers',
        type=int,
        default=5,
        help='生成的预测注数（默认：5）'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json'],
        default='text',
        help='输出格式：text或json（默认：text）'
    )

    parser.add_argument(
        '--show-analysis',
        action='store_true',
        help='显示详细数据分析报告'
    )

    parser.add_argument(
        '--use-cache',
        action='store_true',
        help='使用缓存的历史数据'
    )

    parser.add_argument(
        '--save-cache',
        action='store_true',
        help='保存获取的数据到缓存'
    )

    parser.add_argument(
        '--cache-file',
        default='lottery_history.json',
        help='缓存文件路径（默认：lottery_history.json）'
    )

    args = parser.parse_args()

    # 步骤1：获取数据
    fetcher = LotteryDataFetcher()

    if args.use_cache:
        print(f"正在从缓存加载数据: {args.cache_file}")
        data = fetcher.load_from_file(args.cache_file)
        if not data:
            print("缓存数据不存在或加载失败，重新获取在线数据")
            data = fetcher.fetch_history(args.periods)
    else:
        data = fetcher.fetch_history(args.periods)

    if not data:
        print("错误：无法获取历史数据")
        return 1

    # 保存缓存
    if args.save_cache:
        fetcher.save_to_file(data, args.cache_file)

    # 步骤2：数据分析
    print(f"\n正在分析最近 {len(data)} 期数据...")
    analyzer = LotteryAnalyzer(data)
    results = analyzer.analyze_all()

    # 步骤3：生成预测
    print("正在生成预测号码...")
    predictor = LotteryPredictor(results)
    predictions = predictor.predict(args.numbers)

    # 步骤4：输出结果
    if args.format == 'json':
        output_json(predictions, results, data)
    else:
        output_text(predictions, results, data, args.show_analysis)

    return 0


def output_text(predictions, results, data, show_analysis):
    """输出文本格式结果"""
    print("\n" + "=" * 60)
    print("【大乐透预测号码】")
    print("=" * 60)

    # 计算下一期期号
    if data:
        latest_period = data[0]['period']
        try:
            # 期号格式：26XXXX (26010, 26009, etc.)
            # 提取期号后4位数字
            if len(latest_period) >= 6:
                prefix = latest_period[:-4]  # 前2位 (26)
                suffix = latest_period[-4:]  # 后4位 (0010, 0009, etc.)
                next_suffix = str(int(suffix) + 1).zfill(4)  # 加1，前面补0到4位
                next_period_str = prefix + next_suffix
            else:
                # 简单加1
                next_period_str = str(int(latest_period) + 1)
            print(f"期次：{next_period_str}（下一期预测）")
        except:
            # 如果计算失败，显示下一期
            try:
                next_period_str = str(int(latest_period) + 1)
            except:
                next_period_str = "26???"
            print(f"期次：{next_period_str}（下一期预测）")
    else:
        print("期次：26???（下一期预测）")

    print(f"分析期数：{len(data)} 期\n")

    # 推荐号码
    print("推荐5注号码：")
    for i, pred in enumerate(predictions):
        front_str = ' '.join(f'{num:02d}' for num in pred['front'])
        back_str = ' '.join(f'{num:02d}' for num in pred['back'])
        print(f"第{i + 1}注：{front_str} + {back_str}")

    # 预测依据
    predictor_temp = LotteryPredictor(results)
    print(predictor_temp.generate_summary(predictions))

    # 详细分析报告
    if show_analysis:
        analyzer_temp = LotteryAnalyzer(data)
        print("\n" + analyzer_temp.generate_report())

    print("\n注：仅供娱乐参考，理性投注")
    print("=" * 60)


def output_json(predictions, results, data):
    """输出JSON格式结果"""
    # 计算下一期期号
    next_period = None
    if data:
        latest_period = data[0]['period']
        try:
            # 期号格式：26XXXX (26010, 26009, etc.)
            # 提取期号后4位数字
            if len(latest_period) >= 6:
                prefix = latest_period[:-4]  # 前2位 (26)
                suffix = latest_period[-4:]  # 后4位 (0010, 0009, etc.)
                next_suffix = str(int(suffix) + 1).zfill(4)  # 加1，前面补0到4位
                next_period = prefix + next_suffix
            else:
                # 简单加1
                next_period = str(int(latest_period) + 1)
        except:
            # 如果计算失败，显示下一期
            try:
                next_period = str(int(latest_period) + 1)
            except:
                next_period = "26???"
    else:
        next_period = "26???"

    output = {
        'period': next_period,
        'analysis_periods': len(data),
        'predictions': [],
        'analysis': {
            'high_frequency_front': [f'{x[0]:02d}' for x in results['frequency']['front']['high_frequency'][:10]],
            'high_frequency_back': [f'{x[0]:02d}' for x in results['frequency']['back']['high_frequency'][:5]],
            'low_frequency_front': [f'{x[0]:02d}' for x in results['frequency']['front']['low_frequency'][:10]],
            'low_frequency_back': [f'{x[0]:02d}' for x in results['frequency']['back']['low_frequency'][:5]],
            'odd_even_ratio_front': f"{results['odd_even']['front']['avg_odd']:.0f}:{results['odd_even']['front']['avg_even']:.0f}",
            'odd_even_ratio_back': f"{results['odd_even']['back']['avg_odd']:.0f}:{results['odd_even']['back']['avg_even']:.0f}",
            'sum_value_range': results['sum_value']['recommended_range'],
            'long_miss_front': [f'{x:02d}' for x in results['miss']['front']['long_miss']],
            'long_miss_back': [f'{x:02d}' for x in results['miss']['back']['long_miss']]
        },
        'disclaimer': '仅供娱乐参考，理性投注'
    }

    for pred in predictions:
        output['predictions'].append({
            'front': [f'{x:02d}' for x in pred['front']],
            'back': [f'{x:02d}' for x in pred['back']],
            'strategy': pred['strategy']
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    sys.exit(main())
