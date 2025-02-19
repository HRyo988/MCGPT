import json
import os
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import numpy as np

# JSONデータのパス
data_path = "./data_analysis/data.json"

# 動画名の詳細を生成する関数
def generate_video_details(video_name):
    idx_map = {
        "0": ["Video 1"],
        "1": ["Video 2"],
        "2": ["Video 3"],
        "12": ["Video 2", "Video 3"]
    }
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

# idxごとのデータ集計用辞書
idx_rank_data = defaultdict(list)
rank_1_counts = Counter()

# データの解析
for video in videos:
    # 動画名に基づいて idx を取得
    idx_types = generate_video_details(video["video_name"])
    
    # 動画の順位（rank）を取得
    rank = video.get("rank", None)
    
    # idx ごとに処理
    for idx in idx_types:
        if rank is not None:
            # idx ごとの順位データを追加
            idx_rank_data[idx].append(rank)
            # rank 1を取った回数をカウント
            if rank == 1:
                rank_1_counts[idx] += 1

    # # 中間結果を出力して確認
    # print(f"Video: {video['video_name']}")
    # print(f"  idx_types: {idx_types}")
    # print(f"  rank: {rank}")
    # print(f"  Current idx_rank_data: {dict(idx_rank_data)}")
    # print(f"  Current rank_1_counts: {dict(rank_1_counts)}\n")

# idxごとの順位統計を計算
idx_statistics = {}
for idx, ranks in idx_rank_data.items():
    rank_array = np.array(ranks)
    idx_statistics[idx] = {
        "mean": np.mean(rank_array),
        "median": np.median(rank_array),
        "std": np.std(rank_array),
        "total": len(ranks),
        "rank_1_count": rank_1_counts[idx]
    }

# 結果の表示
print("Rank Statistics by idx:")
for idx, stats in idx_statistics.items():
    print(f"\n{idx}:")
    print(f"  Mean rank: {stats['mean']:.2f}")
    print(f"  Median rank: {stats['median']}")
    print(f"  Standard deviation: {stats['std']:.2f}")
    print(f"  Total ranks: {stats['total']}")
    print(f"  Rank 1 count: {stats['rank_1_count']}")

# グラフの保存先ディレクトリ
output_dir = "./data_analysis/graphs"
os.makedirs(output_dir, exist_ok=True)

# 各 idx ごとの順位データの箱ひげ図（Box Plot）
plt.figure(figsize=(10, 6))
plt.boxplot([idx_rank_data[idx] for idx in idx_rank_data.keys()], labels=idx_rank_data.keys())
plt.title("Rank Distribution by Video Types")
plt.xlabel("Video Types")
plt.ylabel("Rank")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
output_file_boxplot = os.path.join(output_dir, "rank_distribution_by_idx.png")
plt.savefig(output_file_boxplot, format="png", dpi=300)
plt.close()

# 各 idx ごとの平均、中央値、標準偏差を比較する棒グラフ
means = [stats["mean"] for stats in idx_statistics.values()]
medians = [stats["median"] for stats in idx_statistics.values()]
stds = [stats["std"] for stats in idx_statistics.values()]

x = np.arange(len(idx_statistics))  # idxごとの位置

plt.figure(figsize=(10, 6))
width = 0.25  # バーの幅
plt.bar(x - width, means, width, label="Mean", color="lightblue")
plt.bar(x, medians, width, label="Median", color="orange")
plt.bar(x + width, stds, width, label="Std Dev", color="lightgreen")

plt.xlabel("Video Types")
plt.ylabel("Rank Values")
plt.title("Mean, Median, and Standard Deviation by Video Types")
plt.xticks(x, idx_statistics.keys())
plt.legend(loc="upper left")
plt.tight_layout()
output_file_stats = os.path.join(output_dir, "rank_stats_by_Video.png")
plt.savefig(output_file_stats, format="png", dpi=300)
plt.close()

# Rank 1 回数の棒グラフ
plt.bar(rank_1_counts.keys(), rank_1_counts.values(), color='lightblue')
plt.title("Rank 1 Counts by Video Types")
plt.xlabel("Video Types")
plt.ylabel("Rank 1 Counts")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
output_file_rank1 = os.path.join(output_dir, "rank1_counts.png")
plt.savefig(output_file_rank1, format="png", dpi=300)
plt.close()

# 保存したグラフのパスを表示
print(f"Rank distribution box plot saved at: {output_file_boxplot}")
print(f"Rank stats bar graph saved at: {output_file_stats}")
print(f"Rank 1 counts graph saved at: {output_file_rank1}")