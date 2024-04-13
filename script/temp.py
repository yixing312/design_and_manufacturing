# 读取 ../data/ans/ans.txt
# 每一行有一个数字
# 绘图

import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("../data/ans/ans.txt")
# 将data拟合指数曲线
data = [data[i] for i in range(len(data)) if i % 13 == 0]
x = np.arange(len(data))
params = np.polyfit(x, np.log(data), 1)
fit = np.exp(params[1]) * np.exp(params[0] * x)
print(params)
plt.plot(data)
plt.plot(fit)
plt.show()

x = np.arange(len(data) * 100)
fit = np.exp(params[1]) * np.exp(params[0] * x)
plt.plot(fit)
plt.show()
