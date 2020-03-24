import sys
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt

class Circle:
    def __init__(self, radius, xc, yc):
        self.radius = radius
        self.xc = xc
        self.yc = yc

    def calculate(self, t):
        angle = 2 * math.pi * t
        x = math.cos(angle) * self.radius + self.xc
        y = math.sin(angle) * self.radius + self.yc
        return x, y


class Ellipse:
    def __init__(self, radius_a, radius_b, xc, yc):
        self.radius_a = radius_a
        self.radius_b = radius_b
        self.xc = xc
        self.yc = yc

    def calculate(self, t):
        angle = 2 * math.pi * t
        x = math.cos(angle) * self.radius_a + self.xc
        y = math.sin(angle) * self.radius_b + self.yc
        return x, y


def circle(t, radius, center):
    angle = 2 * math.pi * t
    x = math.cos(angle)*radius + center[0]
    y = math.sin(angle)*radius + center[1]
    return x, y

def ellipse(t, a, b, center):
    angle = 2 * math.pi * t
    x = math.cos(angle)*a + center[0]
    y = math.sin(angle)*b + center[1]
    return x, y

def create_points(steps, function):
    points = []
    for i in range(steps):
        t = np.random.random()
        point = list((function.calculate(t)))
        points.append(point)

    return points

def create_points_ordered(begin, end, step, function):
    points = []
    t = begin
    while True:
        if t >= end:
            break
        point = list((function.calculate(t)))
        points.append(point)
        t += step

    return points

def shuffle_points(points):
    permutation = np.random.permutation(len(points))
    new_points = []
    for i in range(len(points)):
        new_points.append(points[permutation[i]])

    return new_points

def save_points(points, file_name):
    file = open(file_name, 'w')
    sample_number = len(points)
    var_number = len(points[0])

    file.write("{0} {1}\n".format(sample_number, var_number))
    for i in range(sample_number):
        line = " ".join([str(x) for x in points[i]])
        file.write(line + "\n")

    file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Implicit function generator")
    parser.add_argument('--lower_bound', '-L', type=int,
                        help='lower bound integer for variable')
    parser.add_argument('--upper_bound', '-U', type=int,
                        help='upper bound integer for variable')
    parser.add_argument('--steps', '-S', type=int)
    parser.add_argument('--step_begin', '-SB', type=float)
    parser.add_argument('--step_end', '-SE', type=float)
    parser.add_argument('--step_step', '-SS', type=float)
    parser.add_argument('--method', '-M', default='circle', choices=['circle', 'ellipse'])
    parser.add_argument('--radius', '-R', type=float)
    parser.add_argument('--radius_a', '-RA', type=float)
    parser.add_argument('--radius_b', '-RB', type=float)
    parser.add_argument('--center_x', '-xc', type=float)
    parser.add_argument('--center_y', '-yc', type=float)
    parser.add_argument('--points_number', '-N', type=int)
    parser.add_argument('--shuffle')
    parser.add_argument('--save')



    args = parser.parse_args()
    function = None
    if args.method:
        if args.method.lower() == 'circle':
            if not args.radius or (not args.center_x and args.center_x != 0.0) or (not args.center_y and args.center_y != 0.0):
                print("You haven't provided all arguments!")
                exit(1)
            function = Circle(args.radius, args.center_x, args.center_y)
        elif args.method.lower() == 'ellipse':
            if not args.radius_a or not args.radius_b or not args.center_x or not args.center_y:
                print("You haven't provided all arguments!")
                exit(1)
            function = Ellipse(args.radius_a, args.radius_b, args.center_x, args.center_y)
        else:
            print('Method not supported!')
            exit(1)

    points = None
    if args.steps:
        points = create_points(args.steps, function)
    elif not args.step_begin or not args.step_end or not args.step_step:
        points = create_points_ordered(args.step_begin, args.step_end, args.step_step, function)
    else:
        print("Step not configured well!")
        exit(1)

    if args.shuffle:
        points = shuffle_points(points)

    if args.save:
        save_points(points, args.save)