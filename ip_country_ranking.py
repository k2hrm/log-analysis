import re
import requests
from collections import Counter
from pathlib import Path

def exchangeCountry(country_code: str) -> str:
    return country_code

# ApnicのクエリAPIを叩き、IPアドレスの国籍を取得する関数
def getApnic(str_ipaddress: str) -> str:
    url = f"https://wq.apnic.net/query?searchtext={str_ipaddress}"

    # プロキシの設定
    proxies = {
        "http": "http://proxy.iiji.jp:8080",
        "https": "http://proxy.iiji.jp:8080",
    }

    response = requests.get(url, proxies=proxies)
    country = ""

    for data_dict in response.json():
        if data_dict["type"] == "object" and "attributes" in data_dict.keys():
            for attribute_dict in data_dict["attributes"]:
                if attribute_dict["name"].lower() == "country":
                    country = attribute_dict["values"][0]
                    break

    return exchangeCountry(country)

# ログファイルのパス
log_file_path = 'access_log'

# IPアドレスを抽出する正規表現パターン（2つ目のIPアドレスを取得）
pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

# ログファイルの読み込み
with open(log_file_path, 'r') as file:
    logs = file.readlines()

# 2つ目のIPアドレスを格納するリスト
ip_addresses = []

# ログから2つ目のIPアドレスを抽出
for log in logs:
    match = re.search(pattern, log)
    if match:
        ip_addresses.append(match.group(2))  # 2つ目のIPアドレスを使用

# 各IPアドレスのアクセス数をカウント
ip_count = Counter(ip_addresses)

# 全アクセス数を計算
total_accesses = len(ip_addresses)

# アクセス数の多い順にソートし、上位10件を取得
sorted_ip_count = sorted(ip_count.items(), key=lambda x: x[1], reverse=True)[:10]

# 結果の表示（上位10件のみ）
for ip, count in sorted_ip_count:
    percentage = (count / total_accesses) * 100
    country = getApnic(ip)
    print(f'{ip} - {count}件 ({percentage:.2f}%) - {country}')