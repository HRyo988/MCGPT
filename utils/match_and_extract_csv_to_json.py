import pandas as pd
import json
import os

# Paths to the input files
json_file_path = './data/labels/5_details.json'
csv_file_path = './data/labels/shot_type_record.csv'

# Load the JSON file
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

# Create a dictionary for easy lookup of names and scores from the JSON data
name_score_dict = {entry['name']: entry['score'] for entry in json_data}

# Extract names from the JSON data
names = list(name_score_dict.keys())

# Load the CSV file
df = pd.read_csv(csv_file_path)

# Print the column names to check for the correct name
print("CSV Columns:", df.columns)

# Filter rows in the CSV file where the video_name column matches the names from the JSON data
filtered_df = df[df['video_name'].apply(lambda x: x.split('_')[-1])  # Extract the part after the last underscore
                 .isin(names)]  # Match with the names from the JSON data

# Extract the required columns
result = []
for index, row in filtered_df.iterrows():
    name = row['video_name'].split('_')[-1]  # Extract name from video_name
    result.append({
        "score": name_score_dict.get(name, None),  # Get the score from the dictionary
        "name": name,
        "video_name": row["video_name"],  # Column name for video name
        "distance": row["distance"],  # Column name for distance
        "shot_type": row["shot_type"]  # Column name for shot type
    })

# Specify the path to save the new JSON file
output_json_file_path = './data/labels/filtered_details.json'

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(output_json_file_path), exist_ok=True)

# Write the filtered data to the new JSON file
with open(output_json_file_path, 'w') as json_file:
    json.dump(result, json_file, indent=4, ensure_ascii=False)

print(f'The filtered JSON file has been saved at: {output_json_file_path}')