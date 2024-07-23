import json
import re
from collections import namedtuple

# 結果をテキストファイルから読み込む関数
def read_distances_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines

# テキストファイルから距離データを抽出する関数
def parse_distance_lines(lines):
    distance_entries = []
    pattern = re.compile(r"Video1: (.+?) \(Label: (.+?)\), Video2: (.+?) \(Label: (.+?)\), Distance: (.+)")
    
    for line in lines:
        match = pattern.match(line)
        if match:
            distance_entries.append({
                'video_name1': match.group(1),
                'video_name2': match.group(3),
                'distance': float(match.group(5))
            })
    
    return distance_entries

# 最大、中間、最小の距離を抽出する関数
def extract_max_mid_min(distances):
    if not distances:
        return None

    sorted_distances = sorted(distances, key=lambda x: x['distance'])
    
    # 距離が0の場合、2番目に小さい組み合わせを選択
    if sorted_distances[0]['distance'] == 0:
        min_distance = sorted_distances[1] if len(sorted_distances) > 1 else sorted_distances[0]
    else:
        min_distance = sorted_distances[0]
    
    max_distance = sorted_distances[-1]
    mid_distance = sorted_distances[len(sorted_distances) // 2]

    return {
        'max': max_distance,
        'mid': mid_distance,
        'min': min_distance
    }

# JSONファイルを出力する関数
def save_distances_to_json(distances, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(distances, f, indent=4)
    print(f"Results have been written to {output_path}")

# 入力ファイルと出力ファイルのパス
input_txt_path = "./data/label_distances.txt"
output_json_path = "./data/processed_distances.json"

# テキストファイルを読み込み
lines = read_distances_from_file(input_txt_path)

# 15行ごとにデータを処理
results = []
for i in range(0, len(lines), 15):
    chunk = lines[i:i+15]
    distance_entries = parse_distance_lines(chunk)
    result = extract_max_mid_min(distance_entries)
    if result:
        results.append({
            'map': (i // 15) + 1,
            **result
        })

# JSONファイルに保存
save_distances_to_json(results, output_json_path)
