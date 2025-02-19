import pandas as pd

# CSVファイルを読み込む
csv_file_path = './data/labels/shot_details.csv'  # CSVファイルのパスを指定
df = pd.read_csv(csv_file_path)

# nameとMOSFull列を抽出
selected_columns = df[['name', 'MOSFull']]

# 抽出したデータをJSON形式で保存
json_file_path = './data/labels/name_mos.json'  # 保存先のパスを指定
selected_columns.to_json(json_file_path, orient='records', lines=True)

print(f"JSON file saved to {json_file_path}")
