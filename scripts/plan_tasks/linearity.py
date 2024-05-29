import numpy as np


def linear(_Ansys_ans, _Task_stack, bounds):
    """
    线性遍历
    """
    lower_bound = np.array(bounds[0])
    upper_bound = np.array(bounds[1])

    devide = 10
    task_queue = []
    for i in range(devide):
        task_queue.append((i / devide) * (upper_bound - lower_bound) + lower_bound)
    return task_queue


def bounds_traversal(_Ansys_ans, _Task_stack, bounds):
    "边界遍历"
    lower_bound = np.array(bounds[0])
    upper_bound = np.array(bounds[1])

    task_queue = []
    for i in range(64):
        task = lower_bound.copy()
        for j in range(6):
            if bool(i & (1 << j)):
                task[j] = upper_bound[j]

        task_queue.append(task)
    return task_queue


def linear_interpolation(_Ansys_ans, _Task_stack, bounds):
    "线性插值"
    lower_bound = np.array(bounds[0])
    upper_bound = np.array(bounds[1])

    task_queue = []
    for i in range(729):
        task = lower_bound.copy()
        for j in range(6):
            # 判断i三进制的第j位%3的余数
            task[j] += int(i / (3**j)) % 3 * (upper_bound[j] - lower_bound[j]) / 2

            # if bool(i & (1 << j)):
            #     task[j] = upper_bound[j]

        task_queue.append(task)
    return task_queue
