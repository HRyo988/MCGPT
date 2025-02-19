import json
import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
from openai import OpenAI
import os
import datetime
from sklearn.model_selection import ShuffleSplit

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY"))

# 動画のパスを指定
moving = 'MAP'
video_path = f'./data/shot_types/moving/{moving}.mp4'

# フレーム間隔を設定
frame_interval = 30

# 動画を読み込む
video = cv2.VideoCapture(video_path)

# フレームを保存するリスト
frames = []

# フレームを抽出する
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    frames.append(base64.b64encode(buffer).decode("utf-8"))

# 動画を閉じる
video.release()

# フレーム間隔を指定してフレームを取得
selected_frames = frames[::frame_interval]

# 結果を表示
print(f"Total frames: {len(frames)}")
print(f"Selected frames (interval {frame_interval}): {len(selected_frames)}")

results = []
    
# Load prompts
sp_path = './prompts/generate_prompts/system_moving.txt'
up_path = './prompts/generate_prompts/user_moving.txt'
with open(sp_path, 'r', encoding='utf-8') as sp_file:
    system_prompt = sp_file.read()
with open(up_path, 'r', encoding='utf-8') as up_file:
    user_prompt = up_file.read()

PROMPT_MESSAGES = [
{
    "role": "system",
    "content": system_prompt,
    "role": "user",
    "content": [
        "These are frames from a <video 1>.",
        *map(lambda x: {"image": x, "resize": 768}, selected_frames[0::30]),
        user_prompt
        ],
    },
]

# OpenAI APIを呼び出す
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
}

result = client.chat.completions.create(**params)
output = result.choices[0].message.content

print(output)

# 結果を保存
results.append({
    "model": "gpt-4o",
    "Moving": moving,
    "system_prompt": system_prompt,
    "user_prompt": user_prompt,
    "output": output
})

# Create logs directory and date-based folder
log_dir = './logs'
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