import pandas as pd

# CSVファイルからデータを読み込む
file_path = './generated_rules/count_shottype.csv'
df = pd.read_csv(file_path)

# ルール変換のための関数
def convert_to_rule(row):
    rule = f"   - If height = {row['height']} and complexity = {row[' complexity']} and surroundings = {row[' surroundings']}, then distance = {row[' distance']} and moving = {row[' moving']}."
    return rule

# ルールを生成
rules = df.apply(convert_to_rule, axis=1)

# ルールをテキストファイルに保存
output_file = './generated_rules/rules.txt'
with open(output_file, "w") as file:
    for rule in rules:
        file.write(rule + "\n")

print(f"ルールが '{output_file}' に保存されました。")
