import os
import pandas as pd
import glob
from collections import Counter
import json

# ディレクトリのパス
output_dir = "./generated_rules/two params"
csv_output_file = os.path.join(output_dir, "count_shottype.csv")
json_output_file = os.path.join(output_dir, "count_shottype.json")

# ディレクトリが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)

# CSVファイルのパスを指定（複数読み込み）
csv_files = glob.glob("./generated_rules/two params/*.csv")

# 出力用のファイルを読み込み対象から除外
csv_files = [
    file for file in csv_files if not file.endswith("count_shottype.csv")]

print(csv_files)
# 全てのCSVを読み込んで結合
df_list = []
combined_df = pd.DataFrame()  # 空のデータフレームを初期化

# print("=== Individual DataFrames ===")
for idx, file in enumerate(csv_files):
    # CSVファイルを読み込む
    df = pd.read_csv(file)
    # リストに追加
    df_list.append(df)
    # 縦方向に結合
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# 左3列でカテゴリ化
group_columns = ["height", "complexity"]
value_columns = ["distance", "moving"]

# CSV用の最頻出値計算関数
# def calculate_mode(sub_df):
#     # print(f"\nProcessing group:\n{sub_df[group_columns].iloc[0].to_dict()}")  # グループ情報を表示
#     # print(f"Group data:\n{sub_df}")  # グループ内のデータを表示
#     result = {}
#     for col in value_columns:
#         most_common = Counter(sub_df[col]).most_common(1)[0]
#         print(f"Most common in '{col}': {most_common}")  # 各列の最頻値を表示
#         result[col] = most_common[0]
#     return pd.Series(result)

# # CSV形式の最終結果データフレームを作成
# result_df = combined_df.groupby(group_columns).apply(calculate_mode).reset_index()

# CSV用の最頻出ペア値計算関数
def calculate_mode_set(sub_df):
    # 2列の値をセットとして組み合わせ、頻度を計算
    combined_pairs = list(zip(sub_df["distance"], sub_df["moving"]))
    most_common_pair = Counter(combined_pairs).most_common(1)[0]
    print(f"Most common pair in 'distance' and 'moving': {most_common_pair}")  # 最頻出ペアを表示
    return pd.Series({" distance": most_common_pair[0][0], " moving": most_common_pair[0][1]})

# CSV形式の最終結果データフレームを作成
result_df = combined_df.groupby(group_columns).apply(calculate_mode_set).reset_index()


# 各グループのデータ数を確認
group_sizes = combined_df.groupby(group_columns).size().reset_index(name='group_size')

# 確認: 各グループの合計が10であるか
# print("\nVerification of group counts:")
# for _, row in group_sizes.iterrows():
#     if row['group_size'] != 10:
#         print(f"Group {row[group_columns].to_dict()} does not have 10 records (count = {row['group_size']})")
#     else:
#         print(f"Group {row[group_columns].to_dict()} is correct (count = 10)")

# CSV形式で結果を保存
result_df.to_csv(csv_output_file, index=False)
print(f"Results saved to {csv_output_file}")

# 計算過程を保持するための辞書を作成
category_process = {}

# 各カテゴリごとの最頻出値を計算（JSON用）
# def calculate_mode_json(sub_df, category_dict):
#     group_key = tuple(sub_df[group_columns].iloc[0].to_dict().values())
#     # タプルを文字列に変換
#     group_key_str = str(group_key)
    
#     # print(f"\nProcessing group:\n{sub_df[group_columns].iloc[0].to_dict()}")  # グループ情報を表示
#     # print(f"Group data:\n{sub_df}")  # グループ内のデータを表示
#     result = {}
    
#     for col in value_columns:
#         most_common = Counter(sub_df[col]).most_common()  # 頻出順に並べる
#         # print(f"Most common in '{col}': {most_common}")  # 各列の最頻値を表示
#         result[col] = most_common  # 頻出順に保存

#     # カテゴリごとに結果を保存
#     category_dict[group_key_str] = result

# # 計算過程を実行（JSON用）
# for _, group in combined_df.groupby(group_columns):
#     calculate_mode_json(group, category_process)

# JSON用の最頻出ペア値計算関数
def calculate_mode_set_json(sub_df, category_dict):
    group_key = tuple(sub_df[group_columns].iloc[0].to_dict().values())
    group_key_str = str(group_key)
    
    # 2列の値をセットとして組み合わせ、頻度を計算
    combined_pairs = list(zip(sub_df["distance"], sub_df["moving"]))
    most_common_pairs = Counter(combined_pairs).most_common()  # 頻出順に並べる
    print(f"Most common pairs: {most_common_pairs}")  # 最頻出ペアを表示
    
    # 保存形式を変更（ペアごとに頻度を記録）
    category_dict[group_key_str] = {str(pair[0]): pair[1] for pair in most_common_pairs}

# 計算過程を実行（JSON用）
for _, group in combined_df.groupby(group_columns):
    calculate_mode_set_json(group, category_process)


# JSON形式で結果を保存
with open(json_output_file, "w") as json_file:
    json.dump(category_process, json_file, indent=4)

print(f"Results saved to {json_output_file}")
