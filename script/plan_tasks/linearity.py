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
