import re
from collections import Counter

# ログファイルのパス
log_file_path = 'access_log'

# 拡張子を抽出する正規表現パターン
pattern = re.compile(r'GET /.*\.(\w+)\sHTTP')

# 拡張子のカウンター
ext_counter = Counter()

# ログファイルを読み込んで拡張子を集計
with open(log_file_path, 'r') as file:
    for line in file:
        match = pattern.search(line)
        if match:
            ext = match.group(1)  # 拡張子を取得
            ext_counter[ext] += 1

# 全アクセス数
total_accesses = sum(ext_counter.values())

# 拡張子ごとの数と割合を表示
for ext, count in ext_counter.most_common():
    percentage = (count / total_accesses) * 100
    print(f'{ext} {count}件 {percentage:.2f}%')
