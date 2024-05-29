import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

distance = [
    [0.237, 0.345, 0.365, 0.389, 0.398, 0.425],
    [0.282, 0.323, 0.394, 0.419, 0.375, 0.366],
    [0.341, 0.397, 0.261, 0.337, 0.486, 0.337],
    [0.259, 0.368, 0.335, 0.448, 0.353, 0.396],
    [0.37, 0.427, 0.306, 0.315, 0.427, 0.314],
    [0.311, 0.456, 0.283, 0.36, 0.457, 0.292],
]

# distance = [
#     [0.327, 0.35, 0.497, 0.326, 0.389, 0.521],
#     [0.378, 0.309, 0.535, 0.366, 0.379, 0.443],
#     [0.436, 0.378, 0.388, 0.298, 0.485, 0.425],
#     [0.368, 0.36, 0.457, 0.404, 0.338, 0.483],
#     [0.474, 0.418, 0.439, 0.257, 0.407, 0.415],
#     [0.396, 0.456, 0.429, 0.308, 0.447, 0.374],
# ]


def plot_circle_with_variances(distances):
    num_circles = len(distances)
    num_sectors = len(distances[0])

    fig, axs = plt.subplots(2, 3, figsize=(12, 8))
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    axs = axs.ravel()

    for i in range(num_circles):
        ax = axs[i]
        circle_distances = distances[i]
        angles = np.linspace(0, 2 * np.pi, num_sectors, endpoint=False)
        radii = np.array(circle_distances)

        # Plot sectors
        for j in range(num_sectors):
            sector_color = plt.cm.viridis(circle_distances[j] / max(circle_distances))
            # Handle wrap-around for the last sector
            if j == num_sectors - 1:
                wedge = patches.Wedge(
                    (0, 0),
                    radii[j],
                    np.degrees(angles[j]),
                    np.degrees(angles[0]),
                    color=sector_color,
                )
            else:
                wedge = patches.Wedge(
                    (0, 0),
                    radii[j],
                    np.degrees(angles[j]),
                    np.degrees(angles[j + 1]),
                    color=sector_color,
                )
            ax.add_patch(wedge)

        # Calculate variance
        variance = np.var(np.sort(circle_distances)[:2])
        # variance = np.var(
        #     np.array([circle_distances[i] - circle_distances[i + 3] for i in range(3)])
        # )

        ax.set_aspect("equal", "box")
        # ax.set_xticks([])
        # ax.set_yticks([])
        ax.set_xlim(-0.6, 0.6)
        ax.set_ylim(-0.6, 0.6)
        ax.set_title(f"Phase {i+1}\nVariance: {variance:.4f}")
    plt.savefig("../data/装配方式/装配相位分布.png")
    plt.show()


# Plot circles with sectors and calculate variances
plot_circle_with_variances(distance)
