import pandas as pd
import json
import os

# Path to the CSV file
csv_file_path = './data/labels/shot_details.csv'

# Load the CSV file
df = pd.read_csv(csv_file_path)

# Set the specific value for the "MOSFull" column (example: specific value is 5)
specific_value = 5

# Filter the rows where "MOSFull" column matches the specific value and extract the "name" from the 2nd column
filtered_df = df[df['MOSFull'] == specific_value]

# Convert the filtered data to JSON format
result = [{"score": row["MOSFull"], "name": row["name"]} for index, row in filtered_df.iterrows()]

# Specify the path to save the JSON file
json_file_path = f'./data/labels/{specific_value}_details.json'

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

# Write the JSON data to the file
with open(json_file_path, 'w') as json_file:
    json.dump(result, json_file, indent=4, ensure_ascii=False)

print(f'The JSON file has been saved at: {json_file_path}')

