import geoip2.database
import ipaddress
from pathlib import Path
import pandas as pd
import subprocess
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== 配置区域 ====================
TARGET_COUNTRIES = ["美国", "新加坡", "香港", "日本","台湾"]  # 可自行添加国家

DB_PATH = "GeoLite2-Country.mmdb"
INPUT_FILE = "ips.txt"
OUTPUT_FILE = "ips-useful.xlsx"

# 连通性检测配置
PING_TIMEOUT = 3
PING_COUNT = 2
MAX_WORKERS = 40  # ← 多线程数量（推荐30-60，根据你的带宽调整）


# ================================================

def get_chinese_country_name(iso_code: str) -> str:
    country_map = {
        "US": "美国", "SG": "新加坡", "CA": "加拿大", "CN": "中国",
        "JP": "日本", "KR": "韩国", "TW": "台湾", "HK": "香港",
        "GB": "英国", "DE": "德国", "FR": "法国", "RU": "俄罗斯",
        "AU": "澳大利亚", "IN": "印度", "BR": "巴西",
    }
    return country_map.get(iso_code.upper(), "未知")


def check_connectivity(ip_str: str) -> bool:
    """检测单个IP连通性"""
    try:
        if sys.platform.startswith('win'):
            cmd = ['ping', '-n', str(PING_COUNT), '-w', str(PING_TIMEOUT * 1000), ip_str]
        else:
            cmd = ['ping', '-c', str(PING_COUNT), '-W', str(PING_TIMEOUT), ip_str]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=8)
        output = result.stdout.decode('utf-8', errors='ignore').lower()

        return "ttl=" in output or "bytes=" in output or "time=" in output
    except:
        return False


def get_test_ip(network) -> str:
    """从网段中随机取一个IP进行测试"""
    if network.num_addresses <= 4:
        return str(network.network_address + 1)
    offset = random.randint(1, min(100, network.num_addresses - 2))
    return str(network.network_address + offset)


def process_line(line: str, reader):
    """处理单行（国家判断 + 连通性检测）"""
    line = line.strip()
    if not line or line.startswith('#'):
        return None

    try:
        network = ipaddress.ip_network(line, strict=False)
        test_ip = get_test_ip(network)

        # 查询国家
        response = reader.country(str(network.network_address))
        country_cn = get_chinese_country_name(response.country.iso_code)

        if country_cn not in TARGET_COUNTRIES:
            return None

        # 连通性检测
        is_reachable = check_connectivity(test_ip)

        if is_reachable:
            return [line, country_cn]
        else:
            return None

    except:
        return None


def main():
    if not Path(DB_PATH).exists():
        print(f"❌ 未找到数据库: {DB_PATH}")
        sys.exit(1)

    reader = geoip2.database.Reader(DB_PATH)
    results = []
    total = 0
    useful = 0

    # 先读取所有IP段
    lines = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"🚀 共读取 {len(lines)} 条IP段，开始多线程检测 (线程数: {MAX_WORKERS})...\n")

    # 使用多线程处理
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_list = {executor.submit(process_line, line, reader): line for line in lines}

        for future in as_completed(future_list):
            total += 1
            result = future.result()

            if result:
                results.append(result)
                useful += 1
                print(f"✅ 保留: {result[0]}  →  {result[1]}")
            else:
                # 只打印进度，避免刷屏太快
                if total % 10 == 0:
                    print(f"[{total}] 处理中... 当前保留: {useful}")

    reader.close()

    # 保存结果
    if results:
        df = pd.DataFrame(results, columns=["IP段", "国家"])
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"\n🎉 处理完成！")
        print(f"总共处理: {total} 条")
        print(f"最终保留: {useful} 条")
        print(f"结果已保存至: {OUTPUT_FILE}")
    else:
        print("\n❌ 没有找到符合条件的IP段")


if __name__ == "__main__":
    main()