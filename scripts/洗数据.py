"""本文件用于洗数据"""

import pandas as pd
import os

txt_file_path = "../data/截面数据_v1"

if __name__ == "__main__":
    file_list = [file for file in os.listdir(txt_file_path) if file.endswith(".txt")]

    for file in file_list:
        file_path = os.path.join(txt_file_path, file)
        data = []
        with open(file_path, "r", encoding="gbk") as f:
            lines = f.readlines()
            lines = lines[1:]
            line_data = []
            for line in lines:
                line_data.append(line.strip().split("\t"))
            data = pd.DataFrame(line_data)
        # data = pd.read_csv(file_path, delimiter="\t", encoding="gbk")
        csv_file_path = file_path.replace(".txt", ".csv")
        data.to_csv(csv_file_path, index=False)
