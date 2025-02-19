import matplotlib.pyplot as plt
from collections import Counter
import os

# 出力ディレクトリの作成
output_dir = './data_analysis/graphs/propose'
os.makedirs(output_dir, exist_ok=True)

# 提案ショットタイプのリスト
shot_types = [
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Medium Shot', 'Moving bird\'s-eye Shot',
    'Medium Shot', 'Survey Shot',
    'Close-up', 'Pedestal/Elevator Shot',
    'Close-up', 'Pedestal/Elevator Shot',
    'Medium Shot', 'Moving Aerial Tilt Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Medium Shot', 'Moving Aerial Tilt Shot',
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Medium Shot', 'Moving bird\'s-eye Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Very Long Shot', 'Bird\'s-eye Shot',
    'Medium Shot', 'Moving Aerial Tilt Shot',
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Medium Shot', 'Moving bird\'s-eye Shot',
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Medium Shot', 'Pedestal/Elevator Shot',
    'Very Long Shot', 'Moving Aerial Pan Shot',
    'Medium Shot', 'Moving bird\'s-eye Shot',
    'Medium Shot', 'Moving Aerial Tilt Shot',
    'Medium Shot', 'Moving bird\'s-eye Shot'
]

# ショットタイプのペア（距離と動き）ごとの出現回数
shot_pairs = [tuple(shot_types[i:i+2]) for i in range(0, len(shot_types), 2)]
pair_count = Counter(shot_pairs)

# 距離ごとの出現回数
distance_types = ['Close-up', 'Medium Shot', 'Very Long Shot']
distance_count = Counter(shot for shot in shot_types if shot in distance_types)

# 動きごとの出現回数（'motion'を'moving'に変更）
moving_types = ['Moving Aerial Pan Shot', 'Moving Aerial Tilt Shot', 'Pedestal/Elevator Shot', "Bird's-eye Shot", "Moving bird's-eye Shot", 'Survey Shot', 'Fly-through Shot']

# 出現回数をカウント
moving_count = Counter(shot for shot in shot_types if shot in moving_types)

# 出現回数が0のタイプも含める
moving_count = {moving: moving_count.get(moving, 0) for moving in moving_types}

# 可視化

# 1. ショットタイプの組み合わせ
plt.figure(figsize=(10, 6))
plt.bar([f'{pair[0]} - {pair[1]}' for pair in pair_count.keys()], pair_count.values(), color='lightcoral')
plt.title('Frequency of Shot Type Pairs')
plt.xlabel('Shot Type Pair')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'shot_type_pairs.png'))  # 保存


# 2. 距離の回数
plt.figure(figsize=(8, 6))
plt.bar(distance_count.keys(), distance_count.values(), color='skyblue')
plt.title('Frequency of Distance Types')
plt.xlabel('Distance Type')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'distance_types.png'))  # 保存

# 3. 動きの回数（'motion'から'moving'に変更）
plt.figure(figsize=(10, 6))
plt.bar(moving_count.keys(), moving_count.values(), color='lightgreen')
plt.title('Frequency of Moving Types')
plt.xlabel('Moving Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'moving_types.png'))  # 保存
