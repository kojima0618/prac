import pandas as pd
import openpyxl

# テキストファイルのパス
hands_file = 'h2_hands.txt'
node_file = 'h2_node.txt'
time_file = 'h2_time.txt'
memory_file_ps = 'h2_memory_psutil.txt'
memory_file_mp = 'h2_memory_mp.txt'

# テキストファイルの内容をリストに読み込む
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read().split()
    return [float(i) for i in data]

# データを読み込む
hands_data = read_text_file(hands_file)
node_data = read_text_file(node_file)
time_data = read_text_file(time_file)
memory_data_ps = read_text_file(memory_file_ps)
memory_data_mp = read_text_file(memory_file_mp)


# データフレームを作成する
data = {
    'hands': hands_data,
    'node': node_data,
    'time': time_data,
    'mem_ps': memory_data_ps,
    'mem_mp': memory_data_mp
}

df = pd.DataFrame(data)

# データフレームをExcelファイルに書き込む
output_file = 'output_ids.xlsx'
df.to_excel(output_file, sheet_name = 'IDS', index=False)

print(f'Data successfully written to {output_file}')