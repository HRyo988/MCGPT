import json
import os
from collections import Counter
import matplotlib.pyplot as plt

# JSONデータのパス
data_path = "./data_analysis/data.json"

# 動画名の詳細を生成する関数
def generate_video_details(video_name):
    # idx の解析
    idx_map = {
        "0": ["ビデオ1"],
        "1": ["ビデオ2"],
        "2": ["ビデオ3"],
        "12": ["ビデオ2", "ビデオ3"]  # Count for both categories
    }
    # idxを解析（末尾）
    idx = "12" if video_name.endswith("12") else video_name[-1]
    return idx_map.get(idx, ["Unknown"])

# JSONデータの読み込み
if os.path.exists(data_path):
    with open(data_path, "r") as file:
        data = json.load(file)
else:
    raise FileNotFoundError(f"Data not found at the specified path: {data_path}")

# 動画データの取得
videos = data.get("videos", [])

# idx の詳細を収集
idx_details = []
for video in videos:
    idx_details.extend(generate_video_details(video["video_name"]))

# idx の種類ごとのカウント
idx_counts = Counter(idx_details)

# 結果表示
print("Counts by idx type:")
for idx_type, count in idx_counts.items():
    print(f"{idx_type}: {count}")

# グラフの保存先ディレクトリ
output_dir = "./data_analysis/graphs"
os.makedirs(output_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

# グラフ描画と保存
plt.bar(idx_counts.keys(), idx_counts.values(), color='skyblue')
plt.title("Distribution of idx Types")  # グラフタイトル
plt.xlabel("idx Types")  # x軸ラベル
plt.ylabel("Number of Videos")  # y軸ラベル
plt.xticks(rotation=45)  # ラベルを斜めにする
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# 保存
output_file = os.path.join(output_dir, "idx_distribution.png")
plt.savefig(output_file, format="png", dpi=300)  # PNG形式で保存
plt.close()  # グラフを閉じる

print(f"Graph saved at: {output_file}")

