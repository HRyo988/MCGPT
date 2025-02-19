import json
import cv2
import base64
import os
import datetime
from dotenv import load_dotenv
import openai
from collections import Counter
import csv

# .envファイルを読み込む
load_dotenv()

# 環境変数からAPIキーを取得
openai.api_key = os.getenv("OPENAI_API_KEY")

# APIキーを確認（デバッグ用）
if openai.api_key is None:
    raise ValueError("APIキーが正しく設定されていません！")

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY"))

# JSONファイルのパス
json_path = './data/labels/5_details.json'

# JSONファイルを読み込む
with open(json_path, 'r') as json_file:
    video_data = json.load(json_file)

# video_name を抽出する
video_names = [item['name'] for item in video_data]

# ビデオ名と個数を表示
# print("ビデオ名リスト:")
# for video_name in video_names:
#     print(video_name)
# print(f"合計ビデオ数: {len(video_names)}\n")

missing_videos = []  # 見つからないビデオのリスト

# ビデオファイルの存在確認
for video_name in video_names:
    video_path = f"./data/evaluated/Video_{video_name}.mp4"
    if not os.path.exists(video_path):
        missing_videos.append(video_name)

# 全てのビデオが存在するか判定
if missing_videos:
    print("以下のビデオが見つかりませんでした:")
    for missing_video in missing_videos:
        print(missing_video)
    print(f"見つからなかったビデオ数: {len(missing_videos)}")
    print("処理を中止します。")
else:
    print("全てのビデオが存在します。")

    frame_lists = []

    # フレームのリストを作成する関数
    def extract_frames(video_path, frame_interval=30):
        video = cv2.VideoCapture(video_path)
        frames = []
        frame_count = 0
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            if frame_count % frame_interval == 0:  # 指定したフレーム間隔ごとにフレームを保存
                _, buffer = cv2.imencode(".jpg", frame)
                frames.append(base64.b64encode(buffer).decode("utf-8"))
            frame_count += 1
        video.release()
        return frames

    # 11~20番目のビデオ（インデックス10~19）に対してフレーム抽出を行う
    frame_lists = []
    idx = 40 # インデックスを指定

    video_name = video_names[idx]  # インデックスでビデオ名を取得
    # video_name = 'B6201'
    video_path = f"./data/evaluated/Video_{video_name}.mp4"
    frames = extract_frames(video_path)
    frame_lists.append(frames)
    print(f"\n{idx + 1}: {len(frames)} frames read for Video_{video_name}.\n")
    
# Load prompts
sp_path = './prompts/system_prompt.txt'
up_path = './prompts/user_prompt.txt'
with open(sp_path, 'r', encoding='utf-8') as sp_file:
    system_prompt = sp_file.read()
with open(up_path, 'r', encoding='utf-8') as up_file:
    user_prompt = up_file.read()

PROMPT_MESSAGES = [
{
    "role": "system",
    "content": [
        system_prompt,
    ],
    "role": "user",
    "content": [
        "These are frames from a <video 1>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[0][0::30]),
        user_prompt
        ],
    },
]

# OpenAI APIを呼び出す
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
}

results = []

results.append({
    "model": params["model"],
    "Videos": video_names[idx],
    "Range_IDX": idx,
    "system_prompt": system_prompt,
    "user_prompt": user_prompt,
})

outputs = []

for iter in range(20):
    # result = client.chat.completions.create(**params)
    result = openai.ChatCompletion.create(**params)
    output = result.choices[0].message.content
    outputs.append(output) 

    print(f"-----Iteration: {iter}-----")
    print(output)

    # 結果を保存
    results.append({
        "iteration": iter,
        "output": output
    })

# 全ての output を結合
all_outputs = "\n".join(outputs)

# 行を分割して解析
lines = all_outputs.split("\n")
combinations = []

# distance と moving のペアを抽出
current_distance = None
current_moving = None

for line in lines:
    if line.startswith("distance"):
        current_distance = line.split(" ", 1)[1]
    elif line.startswith("moving"):
        current_moving = line.split(" ", 1)[1]
    
    # 両方の値が揃ったらリストに追加してリセット
    if current_distance and current_moving:
        combinations.append((current_distance, current_moving))
        current_distance = None
        current_moving = None

# 頻度をカウント
combination_counts = Counter(combinations)

# 結果を表示
print("\nCombination Frequencies:")
for combo, count in combination_counts.items():
    print(f"{combo}: {count} times")

# 結果を CSV ファイルに保存
output_dir = f"./logs/validation/two params/{video_name}"
output_file = os.path.join(output_dir, "combination_frequencies.csv")

# ディレクトリが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Distance", "Moving", "Count"])  # ヘッダー行
    for combo, count in combination_counts.items():
        writer.writerow([combo[0], combo[1], count])  # 各組み合わせの行を出力

print(f"\n結果を '{output_file}' に保存しました！")

# Create logs directory and date-based folder
log_dir = f'./logs/validation/two params/{video_name}'
date_str = datetime.datetime.now().strftime('%Y-%m-%d')
date_dir = os.path.join(log_dir, date_str)
os.makedirs(date_dir, exist_ok=True)

# Generate a timestamp for the filename
timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_path = os.path.join(date_dir, f'results_{timestamp_str}.json')

# Save all fold data to a JSON file
with open(log_file_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"Results have been logged to {log_file_path}")