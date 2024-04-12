import numpy as np


def random_task(_Ansys_ans, _Task_stack, bounds):
    lower_bound = np.array(bounds[0])
    upper_bound = np.array(bounds[1])
    random_values = np.random.rand(6)
    task_queue = [random_values * (upper_bound - lower_bound) + lower_bound]
    return task_queue


def random_tasks(_Ansys_ans, _Task_stack, bounds):
    # 随机获得一个整数
    random_num = np.random.randint(1, 10)
    task_queue = []
    for _ in range(random_num):
        task_queue.extend(random_task(_Ansys_ans, _Task_stack, bounds))
    return task_queue
