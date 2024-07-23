from dotenv import load_dotenv
import openai
import os
import json
import datetime
from utils.extract_frames import FrameExtractor

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


if __name__ == "__main__":
    # Path to the JSON file containing video distance data
    json_path = './data/processed_distances.json'

    # Create an instance of FrameExtractor with the JSON data
    extractor = FrameExtractor(json_path)

    # List of video names to be processed
    video_name_list = ['1.mp4', '2.mp4']

    # Specify the map number and entry type to get the video names for comparison
    map_number = 3          # 1, 2 or 3
    entry_type = 'min'      # 'max', 'mid' or 'min' 

    # Retrieve video names based on the map number and entry type, updating the video_name_list
    _, _, video_name_list = extractor.get_video_names(map_number, entry_type, video_name_list)

    # List to store frames extracted from the specified videos
    frames_list = []

    # Extract frames from the videos specified in video_name_list and add them to frames_list
    frames_list = extractor.extract_base64_frames(frames_list, video_name_list)



    # Load prompts
    sp_path = './prompts/system_prompt.txt'
    up_path = './prompts/user_prompt.txt'
    system_prompt = open(sp_path, 'r', encoding='utf-8').read()
    user_prompt = open(up_path, 'r', encoding='utf-8').read()


    PROMPT_MESSAGES = [
        {
            "role": "system",
            "content": [
                system_prompt,
                "These are frames from a <video 1>.",
                *map(lambda x: {"image": x, "resize": 768}, frames_list[0][0::30]),
                "These are frames from a <video 2>.",
                *map(lambda x: {"image": x, "resize": 768}, frames_list[1][0::30]),
            ],
            "role": "user",
            "content": [
                "These are frames from a <video a>. What is the shooting technique used in the video",
                *map(lambda x: {"image": x, "resize": 768}, frames_list[2][0::30]),
                "These are frames from a <video b>. What is the shooting technique used in the video",
                *map(lambda x: {"image": x, "resize": 768}, frames_list[3][0::30]),
                user_prompt
            ],
        },
    ]
    params = {
        "model": "gpt-4o",
        "messages": PROMPT_MESSAGES,
    }

    # Send the prompt to the OpenAI API and get the response
    result = openai.chat.completions.create(**params)

    # Print the response content
    print(result.choices[0].message.content)

    # Create logs directory and date-based folder
    log_dir = './logs'
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    date_dir = os.path.join(log_dir, date_str)
    os.makedirs(date_dir, exist_ok=True)

    # Generate a timestamp for the filename
    timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file_path = os.path.join(date_dir, f'{timestamp_str}.json')

    # Collect data to be saved
    log_data = {
        "system_prompt_file": sp_path,
        "user_prompt_file": up_path,
        "video_names": video_name_list,
        "result": result.choices[0].message.content,
    }

    # Save data to a JSON file
    with open(log_file_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

    print(f"Results have been logged to {log_file_path}")