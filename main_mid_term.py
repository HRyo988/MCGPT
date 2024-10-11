from dotenv import load_dotenv
import openai
import os
import json
import datetime
from utils.extract_frames import FrameExtractor
from sklearn.model_selection import KFold

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def cross_validate_videos(videos, n_splits=3, fixed_split=(15, 7)):
    """
    Cross-validate videos with a fixed split configuration.
    
    Parameters:
        videos (list): List of video names.
        n_splits (int): Number of splits.
        fixed_split (tuple): Fixed split configuration, e.g., (15, 7).
        
    Returns:
        list: List of train and test video splits.
    """
    assert sum(fixed_split) == len(videos), "Sum of fixed_split must equal the number of videos."
    kf = KFold(n_splits=n_splits, shuffle=True)
    splits = []
    
    # Generate the fixed train-test split indices
    indices = list(range(len(videos)))
    train_indices = indices[:fixed_split[0]]
    test_indices = indices[fixed_split[0]:fixed_split[0]+fixed_split[1]]
    
    splits.append((
        [videos[i] for i in train_indices],
        [videos[i] for i in test_indices]
    ))
    
    return splits

def generate_video_frames_content(video_index, frames_list):
    """
    Generates the content for a video and its frames.
    
    Parameters:
        video_index (int): Index of the video.
        frames_list (list): List of frames for the video.
    
    Returns:
        list: Content list with video frames and corresponding metadata.
    """
    return [
        f"These are frames from train_video_{video_index + 1}",
        *map(lambda x: {"image": x, "resize": 768}, frames_list[video_index][0::30])
    ]

if __name__ == "__main__":
    # Path to the JSON file containing video distance data
    json_path = './data/labels/filtered_details.json'

    # Create an instance of FrameExtractor with the JSON data
    extractor = FrameExtractor(json_path)

    # JSONファイルを読み込む
    with open(json_path, 'r') as json_file:
        video_data = json.load(json_file)

    # video_name を抽出する
    video_names = [item['video_name'] for item in video_data]

    # N交差検証法を使用してデータを訓練・テストに分割
    n_splits = 3
    video_splits = cross_validate_videos(video_names, n_splits, fixed_split=(15, 7))

    # Load prompts
    sp_path = './prompts/system_prompt.txt'
    up_path = './prompts/user_prompt.txt'
    system_prompt = open(sp_path, 'r', encoding='utf-8').read()
    user_prompt = open(up_path, 'r', encoding='utf-8').read()
    
    # Initialize logs with prompts
    all_fold_logs = [
        {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }
    ]

    # Extract frames for each video
    print("Extract frames from all videos...")
    frames_dict = {video_name: extractor.extract_base64_frames([], [video_name]) for video_name in video_names}
    print("Done!")

    # k-fold
    for i, (train_videos, test_videos) in enumerate(video_splits):
        print(f"Fold {i + 1}:")
        print(f"Train videos: {train_videos}")
        print(f"Test videos: {test_videos}")

        # Extract frames for train and test videos
        train_frames_list = [frames_dict[v] for v in train_videos]
        test_frames_list = [frames_dict[v] for v in test_videos]

        # Prepare prompt messages for the API
        PROMPT_MESSAGES = [
            {    
                "role": "system",
                "content": [
                    system_prompt
                ],
            },
            {
                "role": "user",
                "content": [
                     f"These are frames from test_video_1.",
                    *[{"image": img, "resize": 768} for img in test_frames_list[0][0::30]],
                    user_prompt
                ]
            },
        ]

        # API parameters
        params = {
            "model": "gpt-4o",
            "messages": PROMPT_MESSAGES,
        }

        # Send the prompt to the OpenAI API and get the response
        result = openai.chat.completions.create(**params)

        # Print the response content
        print(result.choices[0].message.content)

        # Collect data for the current fold
        fold_log_data = {
            "fold": i + 1,
            "train_videos": train_videos,
            "test_videos": test_videos,
            "result": result.choices[0].message.content,
        }

        # Add the current fold data to the overall log
        all_fold_logs.append(fold_log_data)

    # Create logs directory and date-based folder
    log_dir = './logs'
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    date_dir = os.path.join(log_dir, date_str)
    os.makedirs(date_dir, exist_ok=True)

    # Generate a timestamp for the filename
    timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file_path = os.path.join(date_dir, f'all_folds_{timestamp_str}.json')

    # Save all fold data to a JSON file
    with open(log_file_path, 'w', encoding='utf-8') as f:
        json.dump(all_fold_logs, f, indent=4, ensure_ascii=False)

    print(f"All folds have been logged to {log_file_path}")