# 读取 ../data/ans/ans.txt
# 每一行有一个数字
# 绘图

import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("../data/ans/ans.txt")
# 将data拟合指数曲线
x = np.arange(len(data))
# params = np.polyfit(x, np.log(data), 1)
# fit = np.exp(params[1]) * np.exp(params[0] * x)
# print(params)
plt.plot(data)
# plt.plot(fit)
plt.title("gradient_descent")
plt.xlabel("epoch")
plt.ylabel("concentricity")
plt.show()
