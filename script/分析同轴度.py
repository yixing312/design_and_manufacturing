import os
import scipy.io as io
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from get_data import get_data_list  # 读取文件并输出位列表
# from get_data import get_data_dict  # 读取文件并输出为以首行为键的字典


def print_cross_section(ax, data_x, data_y):
    """
    画出截面数据，并在角落展示该截面的圆度
    :param ax: 画布
    :param data: 截面数据
    :return: 圆度
    """
    x = [float(data_x[i][2]) for i in range(len(data_x))]
    y = [float(data_y[i][4]) for i in range(len(data_y))]
    dx = [float(data_x[i][-1]) for i in range(len(data_x))]
    dy = [float(data_y[i][-1]) for i in range(len(data_y))]
    x = np.array(x)
    y = np.array(y)
    dx = np.array(dx)
    dy = np.array(dy)
    ds = np.sqrt(dx**2 + dy**2)
    ax.quiver(x, y, dx, dy, ds, scale=1, cmap="rainbow")

    def get_circle(x, y):
        x0 = np.mean(x)
        y0 = np.mean(y)
        r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
        return plt.Circle((x0, y0), np.max(r), color="blue", fill=False)

    ax.add_artist(get_circle(x + dx, y + dy))

    def get_axis(x0, y0, x, y):
        r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
        return plt.Circle((x0, y0), np.max(r), color="red", fill=False)

    ax.add_artist(get_axis(0, 120, x, y))

    # ax.set_xticks([])
    # ax.set_yticks([])


def print_main(ax, data_all):
    """
    画出主图
    :param ax: 画布
    :param data: 主图数据
    :return:
    """
    x1 = [float(data_all["1x"][i][2]) for i in range(len(data_all["1x"]))]
    y1 = [float(data_all["1y"][i][3]) for i in range(len(data_all["1y"]))]
    z1 = [float(data_all["1x"][i][4]) for i in range(len(data_all["1x"]))]
    dx1 = [float(data_all["1x"][i][-1]) for i in range(len(data_all["1x"]))]
    dy1 = [float(data_all["1y"][i][-1]) for i in range(len(data_all["1y"]))]
    dz1 = np.zeros(len(data_all["1x"]))

    x2 = [float(data_all["2x"][i][2]) for i in range(len(data_all["2x"]))]
    y2 = [float(data_all["2y"][i][3]) for i in range(len(data_all["2y"]))]
    z2 = [float(data_all["2x"][i][4]) for i in range(len(data_all["2x"]))]
    dx2 = [float(data_all["2x"][i][-1]) for i in range(len(data_all["2x"]))]
    dy2 = [float(data_all["2y"][i][-1]) for i in range(len(data_all["2y"]))]
    dz2 = np.zeros(len(data_all["2x"]))

    x3 = [float(data_all["3x"][i][2]) for i in range(len(data_all["3x"]))]
    y3 = [float(data_all["3y"][i][3]) for i in range(len(data_all["3y"]))]
    z3 = [float(data_all["3x"][i][4]) for i in range(len(data_all["3x"]))]
    dx3 = [float(data_all["3x"][i][-1]) for i in range(len(data_all["3x"]))]
    dy3 = [float(data_all["3y"][i][-1]) for i in range(len(data_all["3y"]))]
    dz3 = np.zeros(len(data_all["3x"]))

    x = np.concatenate((x1, x2, x3))
    y = np.concatenate((y1, y2, y3))
    z = np.concatenate((z1, z2, z3))
    dx = np.concatenate((dx1, dx2, dx3)) * 10
    dy = np.concatenate((dy1, dy2, dy3)) * 10
    dz = np.concatenate((dz1, dz2, dz3)) * 10

    return ax.quiver(x, y, z, dx, dy, dz, cmap="rainbow")


def print_side(ax, data_all):
    """
    画出侧视图
    :param ax: 画布
    :param data: 侧视图数据
    :return: 同轴度范围
    """
    x1 = [float(data_all["1x"][i][2]) for i in range(len(data_all["1x"]))]
    z1 = [float(data_all["1x"][i][4]) for i in range(len(data_all["1x"]))]
    dx1 = [float(data_all["1x"][i][-1]) for i in range(len(data_all["1x"]))]
    x1 = np.array(x1) + np.array(dx1)
    z1 = np.array(z1)
    points = np.column_stack((x1, z1))
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    ax.scatter(hull_points[:, 0], hull_points[:, 1], s=3, label="C1")

    x2 = [float(data_all["2x"][i][2]) for i in range(len(data_all["2x"]))]
    z2 = [float(data_all["2x"][i][4]) for i in range(len(data_all["2x"]))]
    dx2 = [float(data_all["2x"][i][-1]) for i in range(len(data_all["2x"]))]
    x2 = np.array(x2) + np.array(dx2)
    z2 = np.array(z2)
    points = np.column_stack((x2, z2))
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    ax.scatter(hull_points[:, 0], hull_points[:, 1], s=3, label="C2")

    x3 = [float(data_all["3x"][i][2]) for i in range(len(data_all["3x"]))]
    z3 = [float(data_all["3x"][i][4]) for i in range(len(data_all["3x"]))]
    dx3 = [float(data_all["3x"][i][-1]) for i in range(len(data_all["3x"]))]
    x3 = np.array(x3) + np.array(dx3)
    z3 = np.array(z3)
    points = np.column_stack((x3, z3))
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    ax.scatter(hull_points[:, 0], hull_points[:, 1], s=3, label="C3")
    ax.legend()


def get_anays_ans(fig, data_all):
    """
    获取所有数据的分析结果
    :param fig: 画布
    :param data_all: 所有数据
    :return: 分析结果
    """
    x1 = [float(data_all["1x"][i][2]) for i in range(len(data_all["1x"]))]
    z1 = [float(data_all["1x"][i][4]) for i in range(len(data_all["1x"]))]
    dx1 = [float(data_all["1x"][i][-1]) for i in range(len(data_all["1x"]))]
    x1 = np.array(x1) + np.array(dx1)
    z1 = np.array(z1)
    points = np.column_stack((x1, z1))
    hull = ConvexHull(points)
    hull_points1 = points[hull.vertices]
    center = np.mean(hull_points1, axis=0)
    radii = np.linalg.norm(hull_points1 - center, axis=1)
    max_radius = np.max(radii)
    min_radius = np.min(radii)
    roundness1 = max_radius - min_radius
    fig.text(0.7, 0.25, f"Roundness1: {roundness1:.3f}", fontsize=12)

    x2 = [float(data_all["2x"][i][2]) for i in range(len(data_all["2x"]))]
    z2 = [float(data_all["2x"][i][4]) for i in range(len(data_all["2x"]))]
    dx2 = [float(data_all["2x"][i][-1]) for i in range(len(data_all["2x"]))]
    x2 = np.array(x2) + np.array(dx2)
    z2 = np.array(z2)
    points = np.column_stack((x2, z2))
    hull = ConvexHull(points)
    hull_points2 = points[hull.vertices]
    center = np.mean(hull_points2, axis=0)
    radii = np.linalg.norm(hull_points2 - center, axis=1)
    max_radius = np.max(radii)
    min_radius = np.min(radii)
    roundness2 = max_radius - min_radius
    fig.text(0.7, 0.2, f"Roundness2: {roundness2:.3f}", fontsize=12)

    x3 = [float(data_all["3x"][i][2]) for i in range(len(data_all["3x"]))]
    z3 = [float(data_all["3x"][i][4]) for i in range(len(data_all["3x"]))]
    dx3 = [float(data_all["3x"][i][-1]) for i in range(len(data_all["3x"]))]
    x3 = np.array(x3) + np.array(dx3)
    z3 = np.array(z3)
    points = np.column_stack((x3, z3))
    hull = ConvexHull(points)
    hull_points2 = points[hull.vertices]
    center = np.mean(hull_points2, axis=0)
    radii = np.linalg.norm(hull_points2 - center, axis=1)
    max_radius = np.max(radii)
    min_radius = np.min(radii)
    roundness3 = max_radius - min_radius
    fig.text(0.7, 0.15, f"Roundness3: {roundness3:.3f}", fontsize=12)

    hull_points = np.concatenate((hull_points1, hull_points2, hull_points2))
    center = (0, 120)
    r = np.linalg.norm(hull_points - center, axis=1)
    max_radius = np.max(r)
    min_radius = np.min(r)
    concentricity = max_radius - min_radius
    fig.text(0.7, 0.1, f"concentricity: {concentricity:.3f}", fontsize=12)


def print_all(data_all):
    """
    以一图流展示所有数据，包括三张截面图、主图、侧视图、数据总结表
    :param data_all: 所有数据
    :return:
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(331)
    ax2 = fig.add_subplot(332)
    ax3 = fig.add_subplot(333)
    ax1.set_title("cross_section1")
    ax2.set_title("cross_section2")
    ax3.set_title("cross_section3")
    print_cross_section(ax1, data_all["1x"], data_all["1y"])
    print_cross_section(ax2, data_all["2x"], data_all["2y"])
    print_cross_section(ax3, data_all["3x"], data_all["3y"])

    ax4 = plt.subplot2grid((3, 3), (1, 0), rowspan=2, colspan=2, projection="3d")
    fig.colorbar(print_main(ax4, data_all))

    ax5 = fig.add_subplot(336)
    print_side(ax5, data_all)

    get_anays_ans(fig, data_all)

    plt.show()


data_path = "../data/截面数据_v1"

if __name__ == "__main__":
    # 读取 data_path 下的所有后缀为 .txt 的文件，根据文件名封装为字典
    file_list = [file for file in os.listdir(data_path) if file.endswith(".txt")]
    data_all = {}
    for file in file_list:
        data = get_data_list(os.path.join(data_path, file))
        data_all[file[:-4]] = data
        print("读取文件：", file, "成功！")
    print_all(data_all)
