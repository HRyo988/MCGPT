import cv2
import base64
import json

class FrameExtractor:
    def __init__(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

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
            video = cv2.VideoCapture('./data/' + video_name)
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
