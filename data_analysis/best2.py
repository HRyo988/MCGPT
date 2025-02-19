# import json
# import os
# from collections import defaultdict
# import matplotlib.pyplot as plt

# # JSONデータのパス
# data_path = "./data_analysis/data.json"

# # 動画名の詳細を生成する関数（動画名からidx情報を取得）
# def generate_video_details(video_name):
#     idx_map = {
#         "0": ["MCVQA best"],
#         "1": ["MCVQA best input"],
#         "2": ["human best input"],
#         "12": ["MCVQA best input", "human best input"]
#     }
#     idx = "12" if video_name.endswith("12") else video_name[-1]
#     return idx_map.get(idx, ["Unknown"])

# # JSONデータの読み込み
# if os.path.exists(data_path):
#     with open(data_path, "r") as file:
#         data = json.load(file)
# else:
#     raise FileNotFoundError(f"Data not found at the specified path: {data_path}")

# # 動画データの取得
# videos = data.get("videos", [])

# # teamごとの idx 別のベスト回数（rank 1）カウント
# team_best_counts = defaultdict(lambda: defaultdict(int))

# # idxの種類を定義（全てのidxタイプをリスト化）
# idxs = ["MCVQA best", "MCVQA best input", "human best input"]

# # データの解析
# for video in videos:
#     # 動画名に基づいて idx を取得
#     idx_types = generate_video_details(video["video_name"])
    
#     # 動画の順位（rank）を取得
#     rank = video.get("rank", None)
    
#     # teamの情報を取得（ビデオ名の2番目の数字を取得）
#     video_team = video["video_name"][1]  # 動画名の2番目の数字をteamとして扱う
    
#     # idx ごとに処理
#     for idx in idx_types:
#         if rank == 1:
#             # rank 1の場合、team ごとの idx 別回数をカウント
#             team_best_counts[video_team][idx] += 1

# # グラフを描画
# output_dir = "./data_analysis/graphs"
# os.makedirs(output_dir, exist_ok=True)

# # 各teamごとに個別のグラフを描画
# for video_team in team_best_counts.keys():
#     idx_counts = team_best_counts[video_team]
    
#     # 各idxのrank 1回数をリストに変換
#     counts = [idx_counts.get(idx, 0) for idx in idxs]
    
#     # グラフの描画
#     plt.figure(figsize=(10, 6))
#     plt.bar(idxs, counts, color='lightblue')
    
#     # グラフの設定
#     plt.title(f"Rank 1 Counts by idx for objects: {video_team}")
#     plt.xlabel("idx Types")
#     plt.ylabel("Rank 1 Counts")
#     plt.grid(axis="y", linestyle="--", alpha=0.7)
#     plt.tight_layout()

#     # グラフを保存
#     output_file = os.path.join(output_dir, f"rank_1_counts_by_idx_for_objects_{video_team}.png")
#     plt.savefig(output_file, format="png", dpi=300)
#     plt.close()

#     # 結果の表示
#     print(f"Rank 1 counts graph for team {video_team} saved at: {output_file}")

# # すべてのteamをまとめたグラフを描画
# plt.figure(figsize=(10, 6))

# # それぞれのteamごとに色を設定
# colors = ['lightblue', 'orange', 'lightgreen', 'lightcoral', 'yellow', 'lightseagreen', 'lavender', 'lightpink', 'beige', 'lightgray', 'lightsteelblue', 'linen']

# # 各teamのidx別rank 1回数を集計して棒グラフに描画
# for i, video_team in enumerate(team_best_counts.keys()):
#     idx_counts = team_best_counts[video_team]
#     counts = [idx_counts.get(idx, 0) for idx in idxs]
#     plt.bar([idx + (i * 0.2) for idx in range(len(idxs))], counts, width=0.2, label=f"Team {video_team}", color=colors[i % len(colors)])

# # グラフの設定
# plt.title("Rank 1 Counts by idx for all objects")
# plt.xlabel("idx Types")
# plt.ylabel("Rank 1 Counts")
# plt.xticks(range(len(idxs)), idxs)
# plt.legend(loc="upper left")
# plt.grid(axis="y", linestyle="--", alpha=0.7)
# plt.tight_layout()

# # まとめたグラフを保存
# output_file_all_teams = os.path.join(output_dir, "rank_1_counts_by_idx_for_all_objects.png")
# plt.savefig(output_file_all_teams, format="png", dpi=300)
# plt.close()

# # 結果の表示
# print(f"Rank 1 counts graph for all objects saved at: {output_file_all_teams}")


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

# teamごとの idx 別のベスト回数（rank 1）カウント
team_best_counts = defaultdict(lambda: defaultdict(int))

# idxの種類を定義（全てのidxタイプをリスト化）
idxs = ["Video 1", "Video 2", "Video 3"]

# データの解析
for video in videos:
    # 動画名に基づいて idx を取得
    idx_types = generate_video_details(video["video_name"])
    
    # 動画の順位（rank）を取得
    rank = video.get("rank", None)
    
    # teamの情報を取得（ビデオ名の2番目の数字を取得）
    video_team = video["video_name"][1]  # 動画名の2番目の数字をteamとして扱う
    
    # idx ごとに処理
    for idx in idx_types:
        if rank == 1:
            # rank 1の場合、team ごとの idx 別回数をカウント
            team_best_counts[video_team][idx] += 1

# グラフを描画
output_dir = "./data_analysis/graphs"
os.makedirs(output_dir, exist_ok=True)

# 1つの大きなfigureに全てのteamのグラフを表示
fig, axes = plt.subplots(4, 3, figsize=(15, 15))  # 4行3列のサブプロット
axes = axes.flatten()  # 2次元配列を1次元に変換

# それぞれのteamごとにグラフを描画
for i, (video_team, idx_counts) in enumerate(team_best_counts.items()):
    if i >= 11:  # 11個目のグラフを超えたら描画しない
        break
    
    # 各idxのrank 1回数をリストに変換
    counts = [idx_counts.get(idx, 0) for idx in idxs]
    
    # サブプロットの設定
    ax = axes[i]
    ax.bar(idxs, counts, color='lightblue')
    
    # グラフの設定
    ax.set_title(f"Rank 1 Counts by Video for team: {video_team}")
    ax.set_xlabel("Video Types")
    ax.set_ylabel("Rank 1 Counts")
    ax.set_ylim(0, 3.5)  # 縦軸の最大値を3.5に設定
    ax.grid(axis="y", linestyle="--", alpha=0.7)

# グラフ全体のタイトルとレイアウト
fig.suptitle("Rank 1 Counts by Video for all teams", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])  # サブプロット間の余白を調整

# まとめたグラフを保存
output_file_all_teams = os.path.join(output_dir, "rank_1_counts_by_idx_for_all_teams_combined.png")
plt.savefig(output_file_all_teams, format="png", dpi=300)
plt.close()

# 結果の表示
print(f"Rank 1 counts graph for all teams saved at: {output_file_all_teams}")
