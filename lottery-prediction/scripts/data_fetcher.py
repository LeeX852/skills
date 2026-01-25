#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大乐透数据获取模块
使用体彩官方API获取大乐透历史开奖数据
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional


class LotteryDataFetcher:
    """大乐透数据获取器"""

    # 体彩官方API基础URL
    API_BASE_URL = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry'
    # 大乐透游戏编号
    GAME_NO = '85'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Referer': 'https://www.lottery.gov.cn/',
            'Accept': 'application/json, text/plain, */*'
        })

    def fetch_history(self, count: int = 100) -> List[Dict]:
        """
        获取大乐透历史数据

        Args:
            count: 获取期数，默认100期

        Returns:
            历史开奖数据列表
        """
        print(f"正在获取最近 {count} 期大乐透开奖数据...")

        try:
            # 构建API URL
            # 使用 termLimits 参数一次性获取指定期数的数据
            params = {
                'gameNo': self.GAME_NO,      # 大乐透游戏编号
                'provinceId': 0,               # 全国
                'pageSize': count,              # 每页数据条数
                'isVerify': 1,                # 已验证的数据
                'pageNo': 1,                  # 第1页
                'termLimits': count             # 获取指定期数
            }

            response = self.session.get(
                self.API_BASE_URL,
                params=params,
                timeout=15
            )

            if response.status_code == 200:
                data = json.loads(response.text)

                # 检查API响应是否成功
                if not data.get('success', False):
                    error_msg = data.get('errorMessage', '未知错误')
                    print(f"API返回错误: {error_msg}")
                    # 如果API失败，返回模拟数据
                    return self._generate_mock_data(count)

                # 解析开奖数据
                value = data.get('value', {})
                lottery_list = value.get('list', [])

                if not lottery_list:
                    print("API未返回数据，使用模拟数据")
                    return self._generate_mock_data(count)

                # 转换数据格式
                result = []
                for item in lottery_list[:count]:
                    # 解析开奖结果
                    draw_result = item.get('lotteryDrawResult', '')
                    numbers = [int(x) for x in draw_result.split() if x.isdigit()]

                    # 前5个是前区号码，后2个是后区号码
                    front = numbers[:5]
                    back = numbers[5:7] if len(numbers) >= 7 else []

                    result.append({
                        'period': item.get('lotteryDrawNum', ''),
                        'date': item.get('lotteryDrawTime', ''),
                        'front': front,
                        'back': back
                    })

                print(f"成功从体彩官方API获取 {len(result)} 条数据")
                return result

        except requests.exceptions.Timeout:
            print("请求超时，使用模拟数据")
        except requests.exceptions.RequestException as e:
            print(f"网络请求失败: {e}，使用模拟数据")
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}，使用模拟数据")
        except Exception as e:
            print(f"获取数据失败: {e}，使用模拟数据")

        # 如果所有尝试都失败，返回模拟数据用于演示
        return self._generate_mock_data(count)

    def _generate_mock_data(self, count: int) -> List[Dict]:
        """
        生成模拟数据用于演示

        Args:
            count: 生成期数

        Returns:
            模拟开奖数据列表
        """
        import random

        data = []
        current_date = datetime.now()

        for i in range(count):
            # 生成模拟期号
            year = current_date.year
            period_num = 26000 - i  # 模拟期号
            period = f"{period_num}"

            date = current_date.strftime('%Y-%m-%d')

            # 生成前区号码（5个，1-35，不重复）
            front = sorted(random.sample(range(1, 36), 5))

            # 生成后区号码（2个，1-12，不重复）
            back = sorted(random.sample(range(1, 13), 2))

            data.append({
                'period': period,
                'date': date,
                'front': front,
                'back': back
            })

            current_date = datetime.fromtimestamp(
                current_date.timestamp() - 3 * 24 * 60 * 60
            )

        return data

    def save_to_file(self, data: List[Dict], filename: str = 'lottery_history.json'):
        """
        保存数据到文件

        Args:
            data: 开奖数据列表
            filename: 保存文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {filename}")
        except Exception as e:
            print(f"保存数据失败: {e}")

    def load_from_file(self, filename: str = 'lottery_history.json') -> Optional[List[Dict]]:
        """
        从文件加载数据

        Args:
            filename: 文件名

        Returns:
            开奖数据列表
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"从 {filename} 加载了 {len(data)} 条数据")
            return data
        except FileNotFoundError:
            print(f"文件 {filename} 不存在")
            return None
        except Exception as e:
            print(f"加载数据失败: {e}")
            return None


if __name__ == '__main__':
    # 测试数据获取
    fetcher = LotteryDataFetcher()
    data = fetcher.fetch_history(100)

    if data:
        print("\n最近5期数据:")
        for item in data[:5]:
            print(f"{item['period']} - {item['date']}: {item['front']} + {item['back']}")

        # 保存到文件
        fetcher.save_to_file(data)
