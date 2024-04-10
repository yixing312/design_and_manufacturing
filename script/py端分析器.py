import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import time
from get_data import get_data_list  # 读取文件并输出位列表
from 分析同轴度 import print_all  # 读取文件并输出位列表


# 实现一个任务队列，队列中每个元素为一个六元的元组
# 实现函数，将任务队列写入 ../data/task_queue.txt 中


def write_task_queue(Task_queue):
    # 给每个任务新建文件夹
    for task in Task_queue:
        data_path = "../data/Ansys/" + str(task)
        os.makedirs(data_path)
    # 每个任务占据一行内容
    with open("../data/task_queue.txt", "w", encoding="utf8") as f:
        for task in Task_queue:
            f.write(str(task) + "\n")


def get_concentricity(data_all):
    # 计算同轴度
    x1 = [float(data_all["1x"][i][2]) for i in range(len(data_all["1x"]))]
    z1 = [float(data_all["1x"][i][4]) for i in range(len(data_all["1x"]))]
    dx1 = [float(data_all["1x"][i][-1]) for i in range(len(data_all["1x"]))]
    dz1 = [float(data_all["1y"][i][-1]) for i in range(len(data_all["1y"]))]
    x2 = [float(data_all["2x"][i][2]) for i in range(len(data_all["2x"]))]
    z2 = [float(data_all["2x"][i][4]) for i in range(len(data_all["2x"]))]
    dx2 = [float(data_all["2x"][i][-1]) for i in range(len(data_all["2x"]))]
    dz2 = [float(data_all["2y"][i][-1]) for i in range(len(data_all["2y"]))]
    x3 = [float(data_all["3x"][i][2]) for i in range(len(data_all["3x"]))]
    z3 = [float(data_all["3x"][i][4]) for i in range(len(data_all["3x"]))]
    dx3 = [float(data_all["3x"][i][-1]) for i in range(len(data_all["3x"]))]
    dz3 = [float(data_all["3y"][i][-1]) for i in range(len(data_all["3y"]))]
    x1 = np.array(x1) + np.array(dx1)
    x2 = np.array(x2) + np.array(dx2)
    x3 = np.array(x3) + np.array(dx3)
    z1 = np.array(z1) + np.array(dz1)
    z2 = np.array(z2) + np.array(dz2)
    z3 = np.array(z3) + np.array(dz3)
    points = np.column_stack((x1, z1))
    hull = ConvexHull(points)
    hull_points1 = points[hull.vertices]
    points = np.column_stack((x2, z2))
    hull = ConvexHull(points)
    hull_points2 = points[hull.vertices]
    points = np.column_stack((x3, z3))
    hull = ConvexHull(points)
    hull_points3 = points[hull.vertices]
    hull_points = np.concatenate((hull_points1, hull_points2, hull_points3))
    center = (0, 120)
    r = np.linalg.norm(hull_points - center, axis=1)
    max_radius = np.max(r)
    min_radius = np.min(r)
    concentricity = max_radius - min_radius
    return concentricity


def get_ansys(task):
    data_path = "../data/" + str(task)
    file_list = [file for file in os.listdir(data_path) if file.endswith(".txt")]
    data_all = {}
    for file in file_list:
        data = get_data_list(os.path.join(data_path, file))
        data_all[file[:-4]] = data
        print("读取文件：", file, "成功！")
    concentricity = get_concentricity(data_all)
    return concentricity


def print_ansys(task):
    data_path = "../data/" + str(task)
    file_list = [file for file in os.listdir(data_path) if file.endswith(".txt")]
    data_all = {}
    for file in file_list:
        data = get_data_list(os.path.join(data_path, file))
        data_all[file[:-4]] = data
        print("读取文件：", file, "成功！")
    print_all(data_all)
    plt.savefig(data_path + "/output.png")


if __name__ == "__main__":
    # task_queue = [(4, 4, 4, 4, 4, 4)]  # 任务队列,初始值为最初的任务
    bounds = [
        [4, 4, 4, 4, 4, 4],
        [6, 6, 6, 6, 6, 6],
    ]
    lower_bound = np.array(bounds[0])
    upper_bound = np.array(bounds[1])
    random_values = np.random.rand(len(lower_bound))
    task_queue = [random_values * (upper_bound - lower_bound) + lower_bound]
    write_task_queue(task_queue)  # 写入任务队列

    print("当前任务队列：", task_queue)

    # 读取数据
    ansys_ans = []
    task_stack = []
    print_queue = []
    while 1:
        if os.path.exists("../data/task_queue.txt"):
            # print("任务队列文件存在！")
            time.sleep(1)
            continue
        print("任务队列已经完成，规划新任务")
        for i in task_queue:
            # ansys_ans.append(get_ansys(i))
            task_stack.append(i)
            print_queue.append(i)

        # 根据 ansys_ans 的结果和 task_stack 的任务

        # TODO 退火算法获取新的任务队列
        task_queue = [np.random.rand(6) * (upper_bound - lower_bound) + lower_bound]
        # 写入新的任务队列
        write_task_queue(task_queue)

        # 此时空闲下来，完成绘图工作
        # for i in print_queue:
        #     print_ansys(i)
