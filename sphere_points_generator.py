import math
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def get_circle_point_for_t(radius, t):
    x = radius * math.cos(t)
    y = radius * math.sin(t)

    return x, y

def generate_circle(radius, no_points):
    i = 0
    circle_points = []
    while i < no_points:
        t = float(i) / no_points
        angle = 2 * math.pi * t
        x, y = get_circle_point_for_t(radius, angle)
        circle_points.append([x, y])
        i += 1
    return circle_points

def generate_sphere(radius, no_points):
    vars = ['x', 'y', 'z']

    points = set()
    checkpoints = set()
    half = int(no_points / 2)

    for i in range(half + 1):
        t = i / half
        checkpoints.add(t * radius)
        checkpoints.add(- t * radius)

    for var in vars:
        for v1 in checkpoints:
            circles = generate_circle(math.sqrt(radius * radius - v1 * v1), no_points)
            for c in circles:
                if var == 'x':
                    points.add((v1, c[0], c[1]))
                elif var == 'y':
                    points.add((c[0], v1, c[1]))
                else:
                    points.add((c[0], c[1], v1))

    print("Generated {} data points".format(len(points)))
    return list(points)

def print_dataset(dataset):
    for p in dataset:
        print('{} {} {}'.format(p[0], p[1], p[2]))

if __name__ == '__main__':
    dataset = generate_sphere(5, 15)
    print_dataset(dataset)
    print(len(dataset))

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    xdata = np.array([x[0] for x in dataset])
    ydata = np.array([x[1] for x in dataset])
    zdata = np.array([x[2] for x in dataset])
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
    plt.show()