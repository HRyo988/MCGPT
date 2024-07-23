import os
import json

# 対象フォルダのパス
folder_path = "./data"

# 動画ファイルの拡張子（必要に応じて追加）
video_extensions = ['.mp4', '.avi', '.mov', '.mkv']

# フォルダ内の動画ファイル名を取得
video_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in video_extensions]

# 動画ファイル名とラベルを保持するリスト
video_labels = []

# 各動画ファイルに対するラベルをユーザーに入力してもらう
for video in video_files:
    label = input(f"Enter label for {video}: ")
    video_labels.append({"video_name": video, "label": label})

# JSONファイルの作成
json_path = os.path.join(folder_path, 'video_labels.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(video_labels, f, ensure_ascii=False, indent=4)

print(f"JSON file has been created at {json_path}")
