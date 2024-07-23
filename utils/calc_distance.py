import json
import os

def load_video_labels(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        video_labels = json.load(f)
    return video_labels

def euclidean_distance(label1, label2):
    return abs(label1 - label2)

def calculate_label_distances(video_labels):
    distances = []
    for idx in range(3):
        for i in range(len(video_labels)):
            for j in range(i + 1, 6):
                label1 = float(video_labels[i+2+6*idx]['label'])
                label2 = float(video_labels[j+2+6*idx]['label'])
                distance = euclidean_distance(label1, label2)
                distances.append({
                    'video1': video_labels[i+2+6*idx]['video_name'],
                    'video2': video_labels[j+2+6*idx]['video_name'],
                    'label1': label1,
                    'label2': label2,
                    'distance': distance
                })
    return distances

def save_distances_to_file(distances, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in distances:
            f.write(f"Video1: {item['video1']} (Label: {item['label1']}), Video2: {item['video2']} (Label: {item['label2']}), Distance: {item['distance']}\n")
    print(f"Results have been written to {output_path}")

# JSONファイルのパス
json_path = "./data/video_labels.json"

# 出力ファイルのパス
output_path = "./data/label_distances.txt"

# 処理を実行
video_labels_list = load_video_labels(json_path)
label_distances = calculate_label_distances(video_labels_list)
save_distances_to_file(label_distances, output_path)