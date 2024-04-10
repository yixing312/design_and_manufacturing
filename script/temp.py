import numpy as np


def approximate_gradient(func_task, task, epsilon=1e-4):
    """
    用有限差分法近似梯度。
    """
    grad = np.zeros_like(task)
    for i in range(len(task)):
        task_plus = np.copy(task)
        task_plus[i] += epsilon
        task_minus = np.copy(task)
        task_minus[i] -= epsilon
        task_queue = [task_plus, task_minus]
        value_list = func_task(task_queue)  # 调用外部函数
        grad[i] = (value_list[0] - value_list[1]) / (2 * epsilon)
    return grad


def gradient_descent(func_task, bounds, learning_rate, num_iterations):
    """
    执行梯度下降优化。
    """
    task = np.mean(bounds, axis=0)  # 初始化为边界的中点
    history = []

    for _ in range(num_iterations):
        grad = approximate_gradient(func_task, task)
        task = task - learning_rate * grad  # 更新任务点
        task = np.clip(task, bounds[0], bounds[1])  # 保持任务点在边界内
        value = func_task([task])[0]  # 计算新的任务点的函数值
        history.append((task, value))

    return task, history


# 示例用法
# 这里我们没有实际的func_task实现，所以以下代码只是一个框架
# 你需要提供实际的func_task函数
bounds = [
    [4, 4, 4, 4, 4, 4],
    [6, 6, 6, 6, 6, 6],
]
learning_rate = 0.01
num_iterations = 50

# 假设func_task是已经定义的
# final_task, history = gradient_descent(func_task, bounds, learning_rate, num_iterations)
