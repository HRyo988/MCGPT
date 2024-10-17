import json
import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
from openai import OpenAI
import os
import datetime
from sklearn.model_selection import ShuffleSplit

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

# ShuffleSplit を使ったランダムな分割
ss = ShuffleSplit(n_splits=3, test_size=7, train_size=15, random_state=42)

results = []

# ランダムに分割を行う
for fold, (train_index, test_index) in enumerate(ss.split(video_names)):
    print(f"\nFold {fold + 1}:")
    print(f"Training indices: {train_index}")
    print(f"Testing indices: {test_index}")
    
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
    		"These are frames from a train <video 1>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[0]][0::30]),
            "These are frames from a train <video 2>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[1]][0::30]),
            "These are frames from a train <video 3>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[2]][0::30]),
            "These are frames from a train <video 4>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[3]][0::30]),
            "These are frames from a train <video 5>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[4]][0::30]),
            "These are frames from a train <video 6>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[5]][0::30]),
            "These are frames from a train <video 7>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[6]][0::30]),
            "These are frames from a train <video 8>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[7]][0::30]),
            "These are frames from a train <video 9>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[8]][0::30]),
            "These are frames from a train <video 10>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[9]][0::30]),
            "These are frames from a train <video 11>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[10]][0::30]),
            "These are frames from a train <video 12>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[11]][0::30]),
            "These are frames from a train <video 13>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[12]][0::30]),
            "These are frames from a train <video 14>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[13]][0::30]),
            "These are frames from a train <video 15>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[train_index[14]][0::30]),
        ],
        "role": "user",
        "content": [
            "These are frames from a test <video 1>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[test_index[0]][0::30]),
            "These are frames from a test <video 2>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[test_index[1]][0::30]),
            "These are frames from a test <video 3>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[test_index[2]][0::30]),
            "These are frames from a test <video 4>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[test_index[3]][0::30]),
            "These are frames from a test <video 5>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[test_index[4]][0::30]),
            "These are frames from a test <video 6>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[test_index[5]][0::30]),
            "These are frames from a test <video 7>.",
            *map(lambda x: {"image": x, "resize": 768}, frame_lists[test_index[6]][0::30]),
            user_prompt
            ],
        },
    ]
    
    # OpenAI APIを呼び出す
    params = {
        "model": "gpt-4o-mini",
        "messages": PROMPT_MESSAGES,
    }
    
    result = client.chat.completions.create(**params)
    output = result.choices[0].message.content
    
    # 結果を表示
    print(f"Result for Fold {fold + 1}:")
    print(output)
    
    # 結果を保存
    results.append({
        "fold": fold + 1,
        "model": "gpt-4o",
        "Videos": video_names,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "train_indes": train_index.tolist(),
        "test_indes": test_index.tolist(),
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