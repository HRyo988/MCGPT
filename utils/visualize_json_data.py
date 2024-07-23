import json
import matplotlib.pyplot as plt
import os

# JSONファイルのパス
file_path = './data/labels/results.json'
# 画像を保存するディレクトリ
output_dir = './data/labels/images'

# ディレクトリが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)

# JSONファイルを読み込む
with open(file_path, 'r') as file:
    data = json.load(file)

# データの集計
totals = {
    'Total': data["file1_data_count"],
    'Manual': sum(data["a"].values()) + sum(data["b"].values()),
    'Automatic': data["file1_data_count"] - (sum(data["a"].values()) + sum(data["b"].values())),
}

# 合計個数のグラフを作成
plt.figure(figsize=(10, 6))
plt.bar(totals.keys(), totals.values(), color=['blue', 'green', 'red', 'purple'])
plt.xlabel('Category')
plt.ylabel('Total Count')
plt.title('Total Counts Across Categories')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Total_Counts_Across_Categories.png'))
plt.close()

# `sets` セクションのグラフ作成
plt.figure(figsize=(10, 6))
plt.bar(data["sets"].keys(), data["sets"].values(), color='skyblue')
plt.xlabel('Set Type')
plt.ylabel('Count')
plt.title('Counts for Sets Section')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Counts_for_Sets_Section.png'))
plt.close()

# `distance` セクションのグラフ作成
plt.figure(figsize=(10, 6))
plt.bar(data["distance"].keys(), data["distance"].values(), color='lightgreen')
plt.xlabel('Distance Type')
plt.ylabel('Count')
plt.title('Counts for Distance Section')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Counts_for_Distance_Section.png'))
plt.close()

# `moving` セクションのグラフ作成
plt.figure(figsize=(10, 6))
plt.bar(data["moving"].keys(), data["moving"].values(), color='salmon')
plt.xlabel('Moving Type')
plt.ylabel('Count')
plt.title('Counts for Moving Section')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Counts_for_Moving_Section.png'))
plt.close()
