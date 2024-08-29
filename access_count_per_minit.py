import re
from collections import Counter
from datetime import datetime

# ログファイルのパス
log_file_path = 'access_log'

# 日時情報を抽出する正規表現パターン
pattern = r'\[(.*?)\]'

# ログファイルの読み込み
with open(log_file_path, 'r') as file:
    logs = file.readlines()

# 日時を格納するリスト
dates = []

# ログから日時を抽出
for log in logs:
    match = re.search(pattern, log)
    if match:
        # 日時のフォーマットをパースして変換
        date_str = match.group(1).split()[0]
        date_obj = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S')
        # 分単位で日時を整形
        dates.append(date_obj.strftime('%Y-%m-%d %H:%M'))

# 分単位でアクセス数をカウント
counter = Counter(dates)

# 時間順にソートして表示
for date in sorted(counter.keys()):
    print(f'{date}: {counter[date]} accesses')
