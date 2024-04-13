import numpy as np

Learning_rate = 2 * 1e7
Epsilon = 5
limit_gard = 1e-4


def gradient_descent(_Ansys_ans, _Task_stack, bounds):
    """
    梯度下降法，每次迭代生成一系列任务
    """
    global Learning_rate
    global Epsilon
    global limit_gard

    if len(_Task_stack) == 1:
        return generate_perturbed_tasks(_Task_stack[-1], bounds, Epsilon)

    gard = approximate_gradient(_Ansys_ans[-12:], Epsilon)
    # if np.all(np.abs(gard) < limit_gard):
    #     return []

    new_task = _Task_stack[-13] - [i * Learning_rate for i in gard]
    new_task = np.clip(new_task, bounds[0], bounds[1])

    new_tasks = [new_task]
    new_tasks.extend(generate_perturbed_tasks(new_task, bounds, Epsilon))

    return new_tasks


def approximate_gradient(ansys_ans, epsilon):
    """
    用有限差分法近似梯度。
    """
    gard = []
    for i in range(6):
        gard.append((ansys_ans[i] - ansys_ans[i + 6]) / (2 * epsilon))
    return gard


def generate_perturbed_tasks(task, bounds, epsilon):
    """
    生成扰动任务
    """
    perturbed_tasks = []
    for i in range(len(task)):
        task_plus = np.array(task, dtype=float)
        task_minus = np.array(task, dtype=float)
        task_plus[i] += epsilon
        task_minus[i] -= epsilon
        task_plus = np.clip(task_plus, bounds[0], bounds[1])
        task_minus = np.clip(task_minus, bounds[0], bounds[1])
        perturbed_tasks.append(task_plus)
        perturbed_tasks.append(task_minus)

    return perturbed_tasks
