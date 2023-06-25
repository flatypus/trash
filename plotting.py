import matplotlib.pyplot as plt

with open("target_0.txt", "r") as f:
    plot_1 = f.read().strip().split("\n")
    plot_1 = [i.split(" ") for i in plot_1]
    plot_1 = [(int(i[0]), int(i[1]), float(i[2])) for i in plot_1]


with open("target_1.txt", "r") as f:
    plot_2 = f.read().strip().split("\n")
    plot_2 = [i.split(" ") for i in plot_2]
    plot_2 = [(int(i[0]), int(i[1]), float(i[2])) for i in plot_2]

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

x, y, z, t = zip(*xyz)

# plot 3d scatter
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c=t, marker='o', s=100, cmap='gist_rainbow')
# ax.scatter(x, y, z, c=t, marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()
