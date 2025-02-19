import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt

# JSONデータのパス
data_path = "./data_analysis/data.json"

# 動画名の詳細を生成する関数（動画名からidx情報を取得）
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

# mapごとの idx 別のベスト回数（rank 1）カウント
map_best_counts = defaultdict(lambda: defaultdict(int))

# idxの種類を定義（全てのidxタイプをリスト化）
idxs = ["Video 1", "Video 2", "Video 3"]

# データの解析
for video in videos:
    # 動画名に基づいて idx を取得
    idx_types = generate_video_details(video["video_name"])
    
    # 動画の順位（rank）を取得
    rank = video.get("rank", None)
    
    # mapの情報を取得（ビデオ名の最初の数字を取得）
    video_map = video["video_name"][0]  # 動画名の最初の数字をmapとして扱う
    
    # idx ごとに処理
    for idx in idx_types:
        if rank == 1:
            # rank 1の場合、map ごとの idx 別回数をカウント
            map_best_counts[video_map][idx] += 1

# グラフを描画
output_dir = "./data_analysis/graphs"
os.makedirs(output_dir, exist_ok=True)

# 各mapごとに個別のグラフを描画
for video_map in map_best_counts.keys():
    idx_counts = map_best_counts[video_map]
    
    # 各idxのrank 1回数をリストに変換
    counts = [idx_counts.get(idx, 0) for idx in idxs]
    
    # グラフの描画
    plt.figure(figsize=(10, 6))
    plt.bar(idxs, counts, color='lightblue')
    
    # グラフの設定
    plt.title(f"Rank 1 Counts by Video for map: {video_map}")
    plt.xlabel("Video Types")
    plt.ylabel("Rank 1 Counts")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    # グラフを保存
    output_file = os.path.join(output_dir, f"rank_1_counts_by_idx_for_map_{video_map}.png")
    plt.savefig(output_file, format="png", dpi=300)
    plt.close()

    # 結果の表示
    print(f"Rank 1 counts graph for map {video_map} saved at: {output_file}")

# すべてのmapをまとめたグラフを描画
plt.figure(figsize=(10, 6))

# それぞれのmapごとに色を設定
colors = ['lightblue', 'orange', 'lightgreen']

# 各mapのidx別rank 1回数を集計して棒グラフに描画
for i, video_map in enumerate(map_best_counts.keys()):
    idx_counts = map_best_counts[video_map]
    counts = [idx_counts.get(idx, 0) for idx in idxs]
    plt.bar([idx + (i * 0.2) for idx in range(len(idxs))], counts, width=0.2, label=f"Map {video_map}", color=colors[i])

# グラフの設定
plt.title("Rank 1 Counts by Video for all maps (0, 1, 2)")
plt.xlabel("Video Types")
plt.ylabel("Rank 1 Counts")
plt.xticks(range(len(idxs)), idxs)
plt.legend(loc="upper left")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# まとめたグラフを保存
output_file_all_maps = os.path.join(output_dir, "rank_1_counts_by_idx_for_all_maps.png")
plt.savefig(output_file_all_maps, format="png", dpi=300)
plt.close()

# 結果の表示
print(f"Rank 1 counts graph for all maps saved at: {output_file_all_maps}")
