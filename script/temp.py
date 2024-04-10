import numpy as np
import subprocess
import math


def call_external_program(params):
    # 这里替换为调用外部程序的实际代码
    # 假设外部程序通过命令行接收参数并返回一个数值
    result = subprocess.run(
        ["your_program", *map(str, params)], capture_output=True, text=True
    )
    return float(result.stdout)


def simulated_annealing(objective, bounds, max_iterations, initial_temp, cooling_rate):
    # 初始化参数
    current_params = (
        np.random.rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0]) + bounds[:, 0]
    )
    current_value = objective(current_params)
    best = current_params
    best_value = current_value

    # 初始温度
    temp = initial_temp

    # 主循环
    for i in range(max_iterations):
        # 生成新解
        candidate_params = current_params + np.random.randn(len(bounds)) * (temp**0.5)
        # 限制参数在规定范围内
        candidate_params = np.clip(candidate_params, bounds[:, 0], bounds[:, 1])

        # 计算新解的目标函数值
        candidate_value = objective(candidate_params)

        # 计算接受概率
        if candidate_value < current_value or np.random.rand() < math.exp(
            (current_value - candidate_value) / temp
        ):
            current_params, current_value = candidate_params, candidate_value

            # 更新最佳解
            if candidate_value < best_value:
                best, best_value = candidate_params, candidate_value

        # 冷却过程
        temp *= 1 - cooling_rate

        print(f"Iteration {i+1}: Best Value = {best_value} at Params = {best}")

    return best


# 定义问题的边界
bounds = np.array([[0, 1]] * 6)  # 假设每个参数都在0到1之间

# 运行算法
optimized_params = simulated_annealing(call_external_program, bounds, 1000, 100, 0.01)

print("Optimized parameters:", optimized_params)
