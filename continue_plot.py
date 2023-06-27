import matplotlib.pyplot as plt
from time import time
from timer import Timer
import numpy as np
import math

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


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
    # distance from c2 to ball in cm
    d_2 = (d_cam * math.sin(alpha_1)) / math.sin(far_angle)
    # sine law (again)
    y = (d_2 * math.sin(alpha_2)) / math.sin(math.radians(90))
    x = math.sqrt((d_2**2) - (y**2))
    return (x, y)


def display(x, y, z):
    x = round(x, 2)
    y = round(y, 2)
    z = round(z, 2)
    print(f"({x}, {y}, {z})")


def predict_landing(xyz):
    # get x y and z values of the last four points
    points = [(x, y, z) for x, y, z, t in xyz[-4:]]
    delta_t = xyz[-1][3] - xyz[-4][3]
    # data = np.array(points)
    # datamean = data.mean(axis=0)
    # # Do an SVD on the mean-centered data.
    # uu, dd, vv = np.linalg.svd(data - datamean)
    # linepts = vv[0] * np.mgrid[-1000:1000:2j][:, np.newaxis]
    # linepts += datamean
    # final_points = linepts.T.tolist()
    # x1, x2 = final_points[0]
    # y1, y2 = final_points[1]
    # z1, z2 = final_points[2]
    x1, y1, z1 = points[0]
    x2, y2, z2 = points[3]
    if (x2 - x1) == 2000:
        return x, y
    else:
        vx = ((x2 - x1) / 100) / delta_t
        vy = ((y2 - y1) / 100) / delta_t
        vz = ((z2 - z1) / 100) / delta_t
        ax.plot([x2, x2+(x2-x1)], [y2, y2+(y2-y1)], [z2, z2+(z2-z1)], c="r")

        print(
            f"vx: {round(vx, 2)}m/s, vy: {round(vy, 2)}m/s, vz: {round(vz, 2)}m/s, delta_t: {round(delta_t, 2)}s")
        times = np.roots([0.5 * -9.81, vz, height])
        t = max(times)
        return (vx * t * 100), (vy * t * 100)


xyz = []
timer = Timer()

while True:
    timer.reset()
    dim_1, height_1 = get_data("target_0.txt")
    dim_2, height_2 = get_data("target_1.txt")

    if len(xyz) == 0:
        xyz.append((0, 0, 0, time()))
        continue

    if (xyz[-1][0] == dim_1 and xyz[-1][1] == dim_2 and xyz[-1][2] == 360 - height_1):
        continue
    if dim_1 is None:
        dim_1 = xyz[-1][0]
    if dim_2 is None:
        dim_2 = xyz[-1][1]

    if height_1 is None and height_2 is not None:
        height = height_2
    elif height_2 is None and height_1 is not None:
        height = height_1
    elif height_1 is None and height_2 is None:
        height = 360 - xyz[-1][2]
    else:
        height = (height_1 + height_2) / 2

    if len(xyz) > 30:
        xyz = xyz[1:]

    # angle (radians)
    alpha_1 = find_alpha(dim_1)
    alpha_2 = (math.pi/2) - find_alpha(dim_2)

    # print(alpha_1, alpha_2)
    x, y = get_x_y(alpha_1, alpha_2)
    # display(x, y, 360 - height)

    xyz.append((x, y, 360 - height, time()))
    ax.clear()

    ax.plot([0, 245], [0, 0], [0, 0], c="black")
    ax.plot([0, 0], [0, 360], [0, 0], c="black")
    ax.plot([0, 0], [0, 0], [0, 245], c="black")

    if len(xyz) == 0:
        ax.scatter([], [], [], c="red", marker='o', s=100, cmap='gist_rainbow')
    else:
        dim_1_list,  dim_2_list, height_list, time_list = zip(*xyz)
        ax.scatter(dim_1_list,  dim_2_list, height_list, c=time_list,
                   marker='o', s=50, cmap='gist_rainbow_r')
        ax.scatter(x, y, 360 - height, c="red", marker='o', s=160)

    # take the last four points and draw a best fit line through them
    if len(xyz) > 4:
        pred_x, pred_y = predict_landing(xyz)
        print(f"Predicted landing: ({round(pred_x, 2)}, {round(pred_y, 2)})")
        ax.scatter(pred_x, pred_y, 0, c="green", marker='o', s=160)
        ax.text2D(
            0.05, 0.95, f"Predicted landing: ({round(pred_x, 2)}, {round(pred_y, 2)})", transform=ax.transAxes)
    ax.set_xlabel('Side camera')
    ax.set_ylabel('Laptop camera')
    ax.set_zlabel('Height')
    # set axis bounds
    ax.set_xlim3d(0, 245)
    ax.set_ylim3d(0, 360)
    ax.set_zlim3d(0, 245)
    plt.pause(0.015)


plt.show()
