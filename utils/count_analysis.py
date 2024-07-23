import json
from collections import Counter

# Load data from JSON files
with open('./data/labels/5_details.json', 'r') as f:
    file1_data = json.load(f)

with open('./data/labels/filtered_details.json', 'r') as f:
    file2_data = json.load(f)

# Create a set of video names from file1
video_names = {entry['name'] for entry in file1_data}

# Function to count occurrences based on conditions
def count_occurrences(data, video_names):
    video_name_counts = Counter()
    distance_counts = Counter()
    shot_type_counts = Counter()
    a_counts = Counter()
    b_counts = Counter()

    # Count occurrences of 'A' and 'B' in video names
    for video_name in video_names:
        if 'A' in video_name:
            a_counts['A'] += 1
        elif 'B' in video_name:
            b_counts['B'] += 1

    # Count occurrences in the data based on video name, distance, and shot type
    for entry in data:
        video_name = entry['video_name']
        distance = entry['distance']
        shot_type = entry['shot_type'][1:]

        if video_name in video_names:
            video_name_counts[video_name] += 1
        else:
            distance_counts[distance] += 1
            shot_type_counts[shot_type] += 1
            distance_shot_type_key = f"{distance}_{shot_type}"  # Convert tuple to string
            video_name_counts[distance_shot_type_key] += 1

    return video_name_counts, distance_counts, shot_type_counts, a_counts, b_counts

# Get counts
video_name_counts, distance_counts, shot_type_counts, a_counts, b_counts = count_occurrences(file2_data, video_names)

# Count the number of entries in file1_data
file1_data_count = len(file1_data)

# Convert counts to dictionaries
results = {
    'sets': dict(video_name_counts),
    'distance': dict(distance_counts),
    'moving': dict(shot_type_counts),
    'a': dict(a_counts),
    'b': dict(b_counts),
    'file1_data_count': file1_data_count
}

# Save results to a JSON file
with open('./data/labels/results.json', 'w') as f:
    json.dump(results, f, indent=4)
