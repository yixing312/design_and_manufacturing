import os
import scipy.io as io
import numpy as np
import matplotlib.pyplot as plt
from get_data import get_data_list  # 读取文件并输出位列表

data_path = "../data/截面数据_v1"
if __name__ == "__main__":
    # 读取 data_path 下的所有后缀为 .txt 的文件，根据文件名封装为字典
    file_list = [file for file in os.listdir(data_path) if file.endswith(".txt")]
    data_all = {}
    for file in file_list:
        data = get_data_list(os.path.join(data_path, file))
        data_all[file[:-4]] = data
        print("读取文件：", file, "成功！")
    x1 = [float(data_all["1x"][i][2]) for i in range(len(data_all["1x"]))]
    y1 = [float(data_all["1y"][i][4]) for i in range(len(data_all["1y"]))]
    print(np.mean(x1), np.mean(y1))
    x1 = np.array(x1) - np.mean(x1)
    y1 = np.array(y1) - np.mean(y1)
    r1 = np.sqrt(x1**2 + y1**2)
    r1.sort()

    x2 = [float(data_all["2x"][i][2]) for i in range(len(data_all["2x"]))]
    y2 = [float(data_all["2y"][i][4]) for i in range(len(data_all["2y"]))]
    print(np.mean(x2), np.mean(y2))
    x2 = np.array(x2) - np.mean(x2)
    y2 = np.array(y2) - np.mean(y2)
    r2 = np.sqrt(x2**2 + y2**2)
    r2.sort()

    x3 = [float(data_all["3x"][i][2]) for i in range(len(data_all["3x"]))]
    y3 = [float(data_all["3y"][i][4]) for i in range(len(data_all["3y"]))]
    print(np.mean(x3), np.mean(y3))
    x3 = np.array(x3) - np.mean(x3)
    y3 = np.array(y3) - np.mean(y3)
    r3 = np.sqrt(x3**2 + y3**2)
    r3.sort()

    plt.plot(np.arange(len(r1)), r1, label="surface1")
    plt.plot(np.arange(len(r2)), r2, label="surface2")
    plt.plot(np.arange(len(r3)), r3, label="surface3")
    plt.legend()
    plt.show()
