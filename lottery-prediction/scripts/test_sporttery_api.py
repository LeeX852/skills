#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试体彩官方API"""

import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Referer': 'https://www.lottery.gov.cn/'
}

# 体彩官方API
url = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=100&isVerify=1&pageNo=1'

print("请求体彩官方API...")
response = requests.get(url, headers=headers, timeout=10)
print(f"状态码: {response.status_code}")
print(f"内容长度: {len(response.text)} 字节\n")

# 尝试解析JSON
try:
    data = json.loads(response.text)
    print("JSON解析成功!")
    print(f"数据结构: {list(data.keys())}\n")

    # 查找数据
    if 'value' in data:
        print(f"value字段类型: {type(data['value'])}")
        if isinstance(data['value'], dict):
            print(f"value的键: {list(data['value'].keys())}")

            if 'list' in data['value']:
                lottery_list = data['value']['list']
                print(f"\n获取到 {len(lottery_list)} 条记录")
                print(f"\n前5条数据:")

                for i, item in enumerate(lottery_list[:5]):
                    print(f"\n{i+1}. 期号: {item.get('lotteryDrawNum', 'N/A')}")
                    print(f"   日期: {item.get('lotteryDrawTime', 'N/A')}")

                    # 查找号码字段
                    draw_result = item.get('lotteryDrawResult', '')
                    print(f"   开奖结果: {draw_result}")

                    # 解析号码
                    if draw_result:
                        # 大乐透格式通常是: 01 02 03 04 05 + 01 02
                        parts = draw_result.split('+')
                        if len(parts) == 2:
                            front = [int(x.strip()) for x in parts[0].split() if x.strip().isdigit()]
                            back = [int(x.strip()) for x in parts[1].split() if x.strip().isdigit()]
                            print(f"   前区: {front}")
                            print(f"   后区: {back}")

except json.JSONDecodeError as e:
    print(f"JSON解析失败: {e}")
    print(f"\n原始内容前500字符:")
    print(response.text[:500])
except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")
    print(f"\n原始内容前500字符:")
    print(response.text[:500])
