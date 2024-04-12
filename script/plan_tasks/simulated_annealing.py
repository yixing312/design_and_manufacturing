import random as rd
import numpy as np

Initial_temperature = 100
Stop_temperature = 1
Cooling_rate = 0.01

current_temperature = Initial_temperature
best_task_rank = 0
currect_task_rank = 0


def simulated_annealing(_Ansys_ans, _Task_stack, bounds):
    global current_temperature
    global best_task_rank
    global currect_task_rank

    new_task = _Task_stack[-1]
    new_value = _Ansys_ans[-1]
    bast_value = _Ansys_ans[best_task_rank]
    currect_task = _Task_stack[currect_task_rank]
    current_value = _Ansys_ans[currect_task_rank]

    if current_temperature <= Stop_temperature:
        return []

    if len(_Task_stack) == 1:
        return new_task + np.random.rand(6) * (current_temperature**0.5)

    # 比较上一次任务，根据接受原则决定是否接受新解，如果接受，更新当前解为新解
    # 新解尝试更新最优解
    if (
        acceptance_probability(current_value, new_value, current_temperature)
        > rd.random()
    ):
        currect_task_rank = len(_Task_stack) - 1
        if new_value < bast_value:
            best_task_rank = currect_task_rank

    # 在当前任务的基础上随机生成一个新任务

    new_task = currect_task + np.random.randn(6) * (current_temperature**0.5)
    new_task = np.clip(new_task, bounds[0], bounds[1])

    new_task = [new_task]
    # 冷却
    current_temperature *= 1 - Cooling_rate

    # 返回新任务
    return new_task


def acceptance_probability(energy, new_energy, temperature):
    if new_energy < energy:
        return 1
    return np.exp((energy - new_energy) / temperature)
