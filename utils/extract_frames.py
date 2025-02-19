import cv2
import base64
import json
import os
import numpy as np

class FrameExtractor:
    def __init__(self, json_path):
        with open(json_path, 'r') as json_file:
            self.data = json.load(json_file)

    def get_video_names(self, map_number, entry_type, video_names_list):
        """
        Returns the video file names based on the specified map number and entry type.
        
        :param map_number: The map number (integer).
        :param entry_type: The entry type ('max', 'mid', 'min').
        :return: A tuple of video file names (video_name1, video_name2).
        """
        for item in self.data:
            if item['map'] == map_number:
                entry = item.get(entry_type)
                if entry:
                    print(f"{'Map:':<15} {map_number}")
                    print(f"{'Entry Type:':<15} {entry_type}")
                    print(f"{'Video 1:':<15} {entry['video_name1']}")
                    print(f"{'Video 2:':<15} {entry['video_name2']}")
                    video_names_list.append(entry['video_name1'])
                    video_names_list.append(entry['video_name2'])
                    return entry['video_name1'], entry['video_name2'], video_names_list
                else:
                    raise ValueError(f"Entry type '{entry_type}' not found for map {map_number}")

        raise ValueError(f"Map number {map_number} not found")

    def extract_base64_frames(self, frames_list, video_name_list):
        """
        Extracts frames from the video file and encodes them in base64.
        
        :param video_name: Name of the video file.
        :return: A list of base64-encoded frames.
        """
        for video_name in video_name_list:
            print(video_name)
            video_path = "./data/evaluated/" + video_name + ".mp4"
            # video_path = "./data/shot_types/moving/MAP.mp4"
            
            video = cv2.VideoCapture(video_path)

            frames = []
            while video.isOpened():
                success, frame = video.read()
                if not success:
                    break
                _, buffer = cv2.imencode(".jpg", frame)
                frames.append(base64.b64encode(buffer).decode("utf-8"))
            frames_list.append(frames)
            # print(video_name, len(frames))
            video.release()
        return frames_list

def save_sampled_frames(frames_list, output_dir="./output_frames/", num_frames=10):
    """
    Save a fixed number of evenly spaced frames as image files.

    :param frames_list: List of Base64-encoded frames (list of lists).
    :param output_dir: Directory to save the sampled frames.
    :param num_frames: Number of frames to sample and save per video.
    """
    os.makedirs(output_dir, exist_ok=True)  # 保存先ディレクトリを作成

    for video_index, video_frames in enumerate(frames_list):
        video_dir = os.path.join(output_dir, f"video_{video_index + 3}")
        os.makedirs(video_dir, exist_ok=True)  # 各動画ごとのディレクトリを作成

        total_frames = len(video_frames)
        if total_frames < num_frames:
            print(f"Warning: Video {video_index + 1} has less than {num_frames} frames. Saving all {total_frames} frames.")
            sampled_indices = range(total_frames)
        else:
            # 等間隔でフレームを選択
            sampled_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)

        for i, frame_index in enumerate(sampled_indices):
            frame_base64 = video_frames[frame_index]
            frame_data = base64.b64decode(frame_base64)
            frame_np = np.frombuffer(frame_data, dtype=np.uint8)
            frame_image = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)

            # フレーム画像を保存
            frame_path = os.path.join(video_dir, f"frame_{i + 1}.jpg")
            cv2.imwrite(frame_path, frame_image)

        print(f"Saved {len(sampled_indices)} sampled frames for video_{video_index + 1} in {video_dir}.")



if __name__ == "__main__":
    json_path = "./data/labels/5_details.json"
    frame_extractor = FrameExtractor(json_path)
    
    frames_list = []
    video_name_list = ['Video_C3002']
    frames_list = frame_extractor.extract_base64_frames(frames_list, video_name_list)
    save_sampled_frames(frames_list, output_dir="./output_frames/", num_frames=10)
