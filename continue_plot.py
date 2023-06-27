import matplotlib.pyplot as plt
from time import time
from timer import Timer
import math

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# set axis bounds
ax.set_xlim3d(0, 245)
ax.set_ylim3d(0, 360)
ax.set_zlim3d(0, 245)


def get_data(path):
    with open(path, "r") as f:
        plot_data = f.read().strip()
        if plot_data == "no ball found" or plot_data == "":
            return (None, None)
        else:
            x, y = plot_data.split()
            return (int(x), int(y))


# finds the angle of the ball from the camera within the plane of the camera
def find_alpha(x):
    # cosine law
    if x is None:
        return
    # 453 pixels is 640/sqrt(2) pixels
    # 90 degrees is camera field of view, 45 is from isoceles triangle
    m = math.sqrt((x**2) + (453**2) -
                  (2 * x * 453 * math.cos(math.radians(45))))
    # sine law
    alpha = math.asin((math.sin(math.radians(45)) * x) / m)
    return alpha


def get_x_y(alpha_1, alpha_2):
    far_angle = math.pi - alpha_1 - alpha_2
    # distance between c1 and c2 in cm
    d_cam = 245
    # distance from c1 to ball in cm
    d_1 = (d_cam * math.sin(alpha_2)) / math.sin(far_angle)
    d_2 = (d_cam * math.sin(alpha_1)) / math.sin(far_angle)
    y = (d_2 * math.sin(alpha_2)) / math.sin(math.radians(90))
    x = math.sqrt((d_2**2) - (y**2))
    return (x, y)


xyz = []
timer = Timer()

while True:
    timer.reset()
    dim_1, height_1 = get_data("target_0.txt")
    dim_2, height_2 = get_data("target_1.txt")

    if len(xyz) == 0:
        xyz.append((0, 0, 0, time()))
        continue

    if (xyz[-1][0] == dim_1 and xyz[-1][1] == height_1 and xyz[-1][2] == dim_2):
        continue

    dim_1 = dim_1 if dim_1 is not None else xyz[-1][0]
    dim_2 = dim_2 if dim_2 is not None else xyz[-1][1]

    if height_1 is None and height_2 is not None:
        height = height_2
    elif height_2 is None and height_1 is not None:
        height = height_1
    elif height_1 is None and height_2 is None:
        height = xyz[-1][2]
    else:
        height = (height_1 + height_2) / 2

    if len(xyz) > 30:
        xyz = xyz[1:]

    # angle (radians)
    alpha_1 = find_alpha(dim_1)
    alpha_2 = 2 * math.pi - find_alpha(dim_2)

    # print(alpha_1, alpha_2)
    x, y = get_x_y(alpha_1, alpha_2)

    print(f"({x}, {y}, {360 - height})")
    xyz.append((x, y, 360 - height, time()))

    if len(xyz) == 0:
        ax.scatter([], [], [], c="red", marker='o', s=100, cmap='gist_rainbow')
        continue
    dim_1_list,  dim_2_list, height_list, time_list = zip(*xyz)
    ax.clear()
    ax.scatter(dim_1_list,  dim_2_list, height_list, c=time_list,
               marker='o', s=50, cmap='gist_rainbow_r')
    ax.scatter(x, y, 360 - height, c="red",
               marker='o', s=160, cmap='gist_rainbow_r')

    ax.set_xlabel('Side camera')
    ax.set_ylabel('Laptop camera')
    ax.set_zlabel('Height')
    ax.set_xlim3d(0, 640)
    ax.set_ylim3d(0, 360)
    ax.set_zlim3d(0, 640)
    plt.pause(0.015)


plt.show()
