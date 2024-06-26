import os
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
import random

from get_data import get_data_list  # 读取文件并输出位列表
from 分析同轴度 import print_all  # 读取文件并输出位列表

from plan_tasks.random_task import random_task
from plan_tasks.random_task import random_tasks
from plan_tasks.simulated_annealing import simulated_annealing
from plan_tasks.gradient_descent import gradient_descent
from plan_tasks.linearity import linear
from plan_tasks.linearity import bounds_traversal
from plan_tasks.linearity import linear_interpolation


Data_path = "../data/"


def write_task_queue(Task_queue):
    """
    给每个任务新建文件夹并生成任务队列文件
    """
    global Data_path
    # 给每个任务新建文件夹
    for task in Task_queue:
        task_str = ",".join([str(i) for i in task])  # 将任务转换为字符串]
        print("任务：", task_str)
        data_path = Data_path + "Ansys_data/" + task_str
        if not os.path.exists(data_path):
            os.makedirs(data_path)
    # 每个任务占据一行内容
    with open(Data_path + "task_queue.txt", "w", encoding="utf8") as f:
        for task in Task_queue:
            # 将task写入文件，采用逗号隔开
            task_str = ",".join([str(i) for i in task])
            f.write(task_str + "\n")


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
    center = (2.033, 120)

    points = np.column_stack((x1, z1))
    points_list = []
    points_list.extend(points)
    hull = ConvexHull(points)
    hull_points1 = points[hull.vertices]

    r = np.sqrt(np.sum((hull_points1 - center) ** 2, axis=1))
    max_radius = np.max(r)
    min_radius = np.min(r)
    concentricity1 = max_radius - min_radius

    points = np.column_stack((x2, z2))
    points_list.extend(points)
    hull = ConvexHull(points)
    hull_points2 = points[hull.vertices]

    r = np.sqrt(np.sum((hull_points2 - center) ** 2, axis=1))
    max_radius = np.max(r)
    min_radius = np.min(r)
    concentricity2 = max_radius - min_radius

    points = np.column_stack((x3, z3))
    points_list.extend(points)
    hull = ConvexHull(points)
    hull_points3 = points[hull.vertices]
    r = np.sqrt(np.sum((hull_points3 - center) ** 2, axis=1))
    max_radius = np.max(r)
    min_radius = np.min(r)
    concentricity3 = max_radius - min_radius

    return min(concentricity1, concentricity2, concentricity3)

    hull_points = np.concatenate((hull_points1, hull_points2, hull_points3))

    # center = (2.033, 120)

    # 定义目标函数：极差最小化
    def objective_function(x):
        # 计算点 x 到各散点的距离
        distances = np.sqrt(np.sum((points_list - x) ** 2, axis=1))
        # 极差 = 最大距离 - 最小距离
        return np.max(distances) - np.min(distances)

    # !通过优化获得最优中心
    initial_point = np.mean(points, axis=0)
    # bounds = [(1, 119), (3, 121)]

    # result_with_bounds = minimize(
    #     objective_function,
    #     initial_point,
    #     # method="L-BFGS-B", bounds=bounds,
    #     method="Powell",
    # )

    # # 输出最优解
    # center = (result_with_bounds.x[0], result_with_bounds.x[1])

    print(center)
    center = (2.033, 120)
    # center = np.mean(hull_points, axis=0)
    # print(center)
    # r = np.linalg.norm(hull_points - center, axis=1)
    r = np.sqrt(np.sum((hull_points - center) ** 2, axis=1))
    max_radius = np.max(r)
    min_radius = np.min(r)
    concentricity = max_radius - min_radius
    return concentricity


def get_ansys(task):
    data_path = Data_path + "Ansys_data/" + ",".join([str(i) for i in task])
    file_list = [file for file in os.listdir(data_path) if file.endswith(".txt")]
    data_all = {}
    for file in file_list:
        data = get_data_list(os.path.join(data_path, file))
        data_all[file[-6:-4]] = data
        print("读取文件：", file, "成功！")
    concentricity = get_concentricity(data_all)
    # concentricity = random.random()
    return concentricity


def plan_task(Ansys_ans, Task_stack, Bounds):
    # # !随机获取一个任务，无所谓历史任务
    # task_list = random_task(Ansys_ans, Task_stack, Bounds)
    # # !随机获取一个任务队列，数量随机
    task_list = random_tasks(Ansys_ans, Task_stack, Bounds)
    # # !退火算法，每次迭代生成一个新任务
    # task_list = simulated_annealing(Ansys_ans, Task_stack, Bounds)
    # # !梯度下降法，每次迭代生成13个新任务
    # task_list = gradient_descent(Ansys_ans, Task_stack, Bounds)
    # # !线性插值，每次迭代生成10个任务
    # task_list = linear(Ansys_ans, Task_stack, Bounds)
    # # !边界遍历，每次迭代生成64个任务
    # task_list = bounds_traversal(Ansys_ans, Task_stack, Bounds)
    # # !插值遍历，当前插值数为3，生成729个任务
    # task_list = linear_interpolation([], [], Bounds)
    # print(task_list)
    return np.array(task_list)


def Init_task(Bounds):
    # # !随机获取一个任务，无所谓历史任务
    # task_list = random_task([], [], Bounds)
    # # !随机获取一个任务队列，数量随机
    # task_list = random_tasks([], [], Bounds)
    # # !边界遍历，每次迭代生成64个任务
    # task_list = bounds_traversal([], [], Bounds)
    # # !其他初始化方法
    task_list = [
        [3750.0, 3750.0, 3750.0, 3750.0, 3750.0, 3750.0],
        # [1000, 5000, 1000, 1000, 5000, 5000]
        # [5000, 1000, 1000, 5000, 5000, 1000]
    ]
    return np.array(task_list)


def print_ansys(task):
    data_path = Data_path + "Ansys_data/" + ",".join([str(i) for i in task])
    file_list = [file for file in os.listdir(data_path) if file.endswith(".txt")]
    data_all = {}
    for file in file_list:
        data = get_data_list(os.path.join(data_path, file))
        data_all[file[-6:-4]] = data
        print("读取文件：", file, "成功！")
    print_all(data_all)
    plt.savefig(data_path + "/output.png")


if __name__ == "__main__":
    # ! 扭矩边界
    # bounds = [
    #     [4, 4, 4, 4, 4, 4],
    #     [6, 6, 6, 6, 6, 6],
    # ]
    # ! 施力边界
    bounds = [
        [1000, 1000, 1000, 1000, 1000, 1000],
        [5000, 5000, 5000, 5000, 5000, 5000],
    ]
    task_queue = Init_task(bounds)  # 生成任务队列
    write_task_queue(task_queue)  # 写入任务队列

    start_time = time.time()
    end_time = time.time()
    exp_name = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())

    # 读取数据
    ansys_ans = []
    task_stack = []
    print_stack = []
    time_stack = []
    epoch = 1
    while 1:
        if os.path.exists(Data_path + "task_queue.txt"):
            # print("任务队列文件存在！")
            time.sleep(1)
            continue
        end_time = time.time()
        time_stack.append(end_time - start_time)
        print("任务队列已经完成，规划新任务")
        for i in task_queue:
            ansys_ans.append(get_ansys(i))
            task_stack.append(i)
            print_stack.append(i)
        print("Ansys_ans: ", ansys_ans)
        # 根据 ansys_ans 的结果和 task_stack 的任务
        # TODO 任务规划算法
        task_queue = plan_task(ansys_ans, task_stack, bounds)
        # 写入新的任务队列
        write_task_queue(task_queue)
        start_time = time.time()
        # 此时空闲下来，完成绘图工作

        if task_queue.size == 0:
            break

        epoch -= 1
        if epoch == 0:
            break

    while 1:
        if os.path.exists(Data_path + "task_queue.txt"):
            # print("任务队列文件存在！")
            time.sleep(1)
            continue
        end_time = time.time()
        time_stack.append(end_time - start_time)
        for i in task_queue:
            ansys_ans.append(get_ansys(i))
            task_stack.append(i)
            print_stack.append(i)
        with open(Data_path + "task_queue.txt", "w", encoding="utf8") as f:
            f.write("end")

            break

    os.mkdir(Data_path + exp_name)
    with open(Data_path + exp_name + "/task.txt", "w", encoding="utf8") as f:
        for i in task_stack:
            f.write(str(i) + "\n")

    with open(Data_path + exp_name + "/ans.txt", "w", encoding="utf8") as f:
        for j in ansys_ans:
            f.write(str(j) + "\n")

    # for i in print_stack:
    #     print_ansys(i)

    print("任务队列已经完成！")
