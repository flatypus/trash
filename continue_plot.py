import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt

# with open("target_0.txt", "r") as f:
#     plot_1_data = f.read().strip().split("\n")[0]
#     plot_1_data = plot_1_data.split(" ")
#     plot_1 = (int(plot_1_data[0]), int(plot_1_data[1]), float(plot_1_data[2]))
#     primary.append(plot_1)


# with open("target_1.txt", "r") as f:
#     plot_2_data = f.read().strip().split("\n")[0]
#     plot_2_data = plot_2_data.split(" ")
#     plot_2 = (int(plot_2_data[0]), int(plot_2_data[1]), float(plot_2_data[2]))
#     secondary.append(plot_2)
# plot 3d scatter

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')


def get_data(path):
    with open(path, "r") as f:
        plot_data = f.read().strip().split("\n")
        if len(plot_data) == 0 or plot_data[0].strip() == "":
            plot_data = []
            return plot_data
        plot_data = [i.split(" ") for i in plot_data]
        plot_data = [(int(i[0]), int(i[1]), float(i[2])) for i in plot_data]
        return plot_data


while True:
    plot_1 = get_data("target_0.txt")
    plot_2 = get_data("target_1.txt")

    primary, secondary = sorted(
        [plot_1, plot_2], key=lambda x: len(x))

    start = None

    for i, v in enumerate(primary):
        (x, y, t) = v
        if t > secondary[0][2]:
            start = i
            break

    primary = primary[start:]
    xyz = []

    last_secondary = secondary[0]
    for i, v in enumerate(primary):
        # the y value is the height for both primary and secondary, so just average them
        (x, y, t) = v
        # always ensure that the secondary is ahead of the primary
        if secondary[0][2] > t:
            continue
        # if the secondary is ahead of the primary, then we need to find the closest secondary
        # to the primary
        for j, v2 in enumerate(secondary):
            (x2, y2, t2) = v2
            if t2 > t:
                # if the secondary is ahead of the primary, then we need to find the closest secondary
                # to the primary
                if abs(t2-t) < abs(t2-last_secondary[2]):
                    last_secondary = v2
                break
        # now we have the closest secondary to the primary, so we can average the x and y values
        # and add them to the list
        xyz.append((x, x2, 1000-y, t))

    if len(xyz) == 0:
        ax.scatter([], [], [], c="red", marker='o', s=100, cmap='gist_rainbow')
        continue
    x, y, z, t = zip(*xyz)
    ax.scatter(x, y, z, c=t, marker='o', s=100, cmap='gist_rainbow')
    # ax.scatter(x, y, z, c=t, marker='o')
    print("plotting")
    plt.pause(0.02)


plt.show()
