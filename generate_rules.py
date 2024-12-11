import json
import cv2
import base64
from openai import OpenAI
import os
import datetime

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY"))

json_path = './data/labels/filtered_details.json'

# JSONファイルを読み込む
with open(json_path, 'r') as json_file:
    video_data = json.load(json_file)

# video_name を抽出する
video_names = [item['video_name'] for item in video_data]

frame_lists = []

# フレームのリストを作成する関数
def extract_frames(video_path, frame_interval=30):
    video = cv2.VideoCapture(video_path)
    frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        frames.append(base64.b64encode(buffer).decode("utf-8"))
    video.release()
    return frames[::frame_interval]  # フレーム間隔を指定してフレームを抽出

# フレーム抽出をすべてのビデオに対して行う
for i, video_name in enumerate(video_names):
    video_path = f"./data/evaluated/{video_name}.mp4"
    frames = extract_frames(video_path)
    frame_lists.append(frames)
    print(f"{i}: {len(frames)} frames read.")


results = []
    
# Load prompts
sp_path = '.\prompts\generate_rules\system_prompt_generate_rules.txt'
up_path = '.\prompts\generate_rules\system_prompt_generate_rules.txt'
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
        "These are frames from a <video 2>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[1][0::30]),
        "These are frames from a <video 3>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[2][0::30]),
        "These are frames from a <video 4>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[3][0::30]),
        "These are frames from a <video 5>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[4][0::30]),
        "These are frames from a <video 6>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[5][0::30]),
        "These are frames from a <video 7>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[6][0::30]),
        "These are frames from a <video 8>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[7][0::30]),
        "These are frames from a <video 9>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[8][0::30]),
        "These are frames from a <video 10>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[9][0::30]),
        "These are frames from a <video 11>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[10][0::30]),
        "These are frames from a <video 12>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[11][0::30]),
        "These are frames from a <video 13>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[12][0::30]),
        "These are frames from a <video 14>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[13][0::30]),
        "These are frames from a <video 15>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[14][0::30]),
        "These are frames from a <video 16>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[15][0::30]),
        "These are frames from a <video 17>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[16][0::30]),
        "These are frames from a <video 18>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[17][0::30]),
        "These are frames from a <video 19>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[18][0::30]),
        "These are frames from a <video 20>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[19][0::30]),
        "These are frames from a <video 21>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[20][0::30]),
        "These are frames from a <video 22>.",
        *map(lambda x: {"image": x, "resize": 768}, frame_lists[21][0::30]),
        user_prompt
        ],
    },
]

# OpenAI APIを呼び出す
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
}

for iter in range(10):
    result = client.chat.completions.create(**params)
    output = result.choices[0].message.content

    print("----Iter {0}----".format(iter))
    print(output)

    # 結果を保存
    results.append({
        "iter": iter,
        "model": params["model"],
        "Videos": video_names,
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