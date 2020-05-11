import random
from os import walk
from jieba import calc

from dataset_analyzer import DataPreprocessor, DataSet
from feynmann_equation_derivation_testbench import test_derivations
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ellipse_plane import MultiDimEllipseCreator
from linear_plane import MultiLinearCovariatePlaneCreator, MultiLinearBasicPlaneCreator
from polynomial_plane import ThirdOrderPolynomialPlaneCreator
from plane_base import *
from sphere_points_generator import generate_sphere
from functions import calc_sphere_rad5_xc0_yc0_zc0, sphere_calc_func
import math

lows = [2, 30, 50, 70, 100, 150, 200, 250, 300]
highs = [5, 50, 70, 100, 150, 200, 250, 300, 350]
plane_creator = MultiDimEllipseCreator()

def plot_kernel_with_dataset3D(dataset):
    data = dataset.data
    plt.figure()
    ax = plt.axes(projection='3d')

    xdata = np.array([x[0] for x in data])
    ydata = np.array([x[1] for x in data])
    zdata = np.array([x[2] for x in data])
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Reds')
    plt.show()

def calc_func(point):
    p1 = point[0]
    p2 = point[1]
    U = point[2]
    return U - p1 * p2

def generate_linear_points1(no_points, low_range, high_range):
    points = []
    for i in range(no_points):
        point = []
        mult = 1.0
        for j in range(2):
            var = random.random() * (high_range - low_range) + low_range
            point.append(var)
            mult *= var
        point.append(mult)
        points.append(point)

    return DataSet(points)

def sqrt_calc(point):
    p1 = point[0]
    U = point[1]
    return U - math.sqrt(p1)

def generate_sqrt_points(no_points, low_range, high_range):
    points = []
    for i in range(no_points):
        point = []
        var = random.random() * (high_range - low_range) + low_range
        point.append(var)
        point.append(math.sqrt(var))
        points.append(point)

    return DataSet(points)

def square_calc(point):
    p1 = point[0]
    U = point[1]
    return U - p1 * p1

def generate_square_points(no_points, low_range, high_range):
    points = []
    for i in range(no_points):
        point = []
        var = random.random() * (high_range - low_range) + low_range
        point.append(var)
        point.append(var * var)
        points.append(point)

    return DataSet(points)

def hyperbola_calc(point):
    x = point[0]
    y = point[1]
    return x**3 + x - y**2 - 1.5

def generate_hyperbola_points(no_points, low_range, high_range):
    points = []
    for i in range(no_points):
        x = random.random() * (high_range - low_range) + low_range
        y_squared = x**3 + x - 1.5
        y = math.sqrt(y_squared)
        points.append([x, -y])
        points.append([x, y])
        i+=1

    return DataSet(points)

def generate_ellipse_points(no_points, ra, rb, xc, yc):
    points = []
    for i in range(no_points):
        t = random.random()
        angle = 2 * math.pi * t
        x = math.cos(angle) * ra + xc
        y = math.sin(angle) * rb + yc
        points.append([x, y])
    return DataSet(points)

def ellipse_func(ra, rb, xc, yc):
    def ellipse_calc(point):
        x = point[0]
        y = point[1]
        result = (x - xc) ** 2 / ra ** 2 + (y - yc) ** 2 / rb ** 2 - 1
        return result

    return ellipse_calc

def generate_harmonic_oscillator_points(no_points, low_range, high_range):
    points = []
    for i in range(no_points):
        t = random.random() * (high_range - low_range) + low_range
        x = math.exp(0.05 * t) * (math.cos(1.73133 * t) - 0.0288795 * math.sin(1.73133 * t))
        x_dot = math.exp(0.05*t) * (5.5265 * 10e-8 * math.cos(1.73133*t) - 1.73277 * math.sin(1.73133*t))
        x_dot_dot = -3*x + 0.1*x_dot
        points.append([x, x_dot, x_dot_dot])

    return DataSet(points)

def generate_harmonic_oscillator_nonlinear_points():
    dataset = DataSet.import_dataset('./datasets/hmo_nl')
    points = dataset.data
    dataset_points = []
    for point in points:
        x = point[0]
        x_dot = point[1]
        x_dot_dot = 0.1 * x_dot - 9.8 * math.sin(x)
        dataset_points.append([x, x_dot, x_dot_dot])

    return DataSet(dataset_points)

def harmonic_oscillator_calc(point):
    x = point[0]
    x_dot = point[1]
    x_dot_dot = point[2]
    return x_dot_dot - 0.1 * x_dot + 3*x

def harmonic_nonlinear_oscillator_calc(point):
    x = point[0]
    x_dot = point[1]
    x_dot_dot = point[2]
    return x_dot_dot - 0.1 * x_dot + 9.8 * math.sin(x)

def circle_func(r, xc, yc):
    def circle_calc(point):
        x = point[0]
        y = point[1]
        result = (x - xc) ** 2 + (y - yc) ** 2 - r*r
        return result

    return circle_calc

def generate_circle_points(no_points, radius, xc, yc):
    points = []
    for i in range(no_points):
        t = random.random()
        angle = 2 * math.pi * t
        x = math.cos(angle) * radius + xc
        y = math.sin(angle) * radius + yc
        points.append([x, y])

    return DataSet(points)

def linear_test():
    points = generate_linear_points1(1000, 1, 5)

    for low, high in zip(lows, highs):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        #plot_kernel_with_dataset3D(points)
        test_derivations(planes, calc_func, verbose=False)

def sphere_test():
    radius = 5
    points = DataSet(generate_sphere(radius, 30))
    sphere_func = sphere_calc_func(radius, 0, 0, 0)

    for low, high in zip(lows, highs):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        #plot_kernel_with_dataset3D(points)
        test_derivations(planes, sphere_func, verbose=False)

def sqrt_test():
    points = generate_sqrt_points(1000, 1, 10)

    for low, high in zip(lows, highs):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        #plot_kernel_with_dataset3D(points)
        test_derivations(planes, sqrt_calc, verbose=False)

def square_test():
    points = generate_square_points(1000, 1, 100)

    for low, high in zip(lows, highs):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        #plot_kernel_with_dataset3D(points)
        test_derivations(planes, square_calc, verbose=False)

def hyperbola_test():
    points = generate_hyperbola_points(1250, 1, 10)
    lows = [2, 50, 100, 150, 200, 250, 300]
    highs = [5, 100, 150, 200, 250, 300, 350]

    for low, high in zip(lows, highs):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        #plot_kernel_with_dataset3D(points)
        test_derivations(planes, hyperbola_calc, verbose=False)

def ellipse_test():
    ra, rb, xc, yc = 3, 4, 1, 2
    points = generate_ellipse_points(1000, ra, rb, xc, yc)
    func = ellipse_func(ra, rb, xc, yc)

    for low, high in zip(lows, highs):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        #plot_kernel_with_dataset3D(points)
        test_derivations(planes, func, verbose=False)

def harmonic_oscillator_test():
    points = generate_harmonic_oscillator_points(1000, 0, 10)

    for low, high in zip(lows, highs):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        #plot_kernel_with_dataset3D(points)
        test_derivations(planes, harmonic_oscillator_calc, verbose=False)

def nonlinear_harmonic_oscillator_test():
    points = generate_harmonic_oscillator_nonlinear_points()

    lows_loc = [33]
    highs_loc = [38]
    for low, high in zip(lows_loc, highs_loc):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        #plot_kernel_with_dataset3D(points)
        test_derivations(planes, harmonic_nonlinear_oscillator_calc, verbose=True)

def circle_test():
    r, xc, yc = 5, 0, 0
    points = generate_circle_points(1000, r, xc, yc)
    func = circle_func(r, xc, yc)

    for low, high in zip(lows, highs):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        #plot_kernel_with_dataset3D(points)
        test_derivations(planes, func, verbose=False)

#############CHOSEN##################################
def save_sphere():
    radius = 5
    points = DataSet(generate_sphere(radius, 30))
    sphere_func = sphere_calc_func(radius, 0, 0, 0)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 250, 300)
    test_derivations(planes, sphere_func, verbose=False)
    plane_creator.write_plane(planes, './chosen_datasets/sphere_5_0_0_250_300')

def save_hyperbola():
    points = generate_hyperbola_points(1250, 1, 10)
    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 100, 150)
    test_derivations(planes, hyperbola_calc, verbose=False)
    plane_creator.write_plane(planes, './chosen_datasets/hyperbola_1.5_100_150')

def save_ellipse():
    ra, rb, xc, yc = 3, 4, 1, 2
    points = generate_ellipse_points(1000, ra, rb, xc, yc)
    func = ellipse_func(ra, rb, xc, yc)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 150, 200)
    test_derivations(planes, func, verbose=False)
    plane_creator.write_plane(planes, './chosen_datasets/ellipse_1_2_3_4_150_200')

def save_harmonic_oscillator():
    points = generate_harmonic_oscillator_points(1000, 0, 10)
    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 50, 100)
    test_derivations(planes, harmonic_oscillator_calc, verbose=False)
    plane_creator.write_plane(planes, './chosen_datasets/harmosc_50_100')

def save_circle():
    r, xc, yc = 4, 0, 0
    points = generate_circle_points(1000, r, xc, yc)
    func = circle_func(r, xc, yc)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 100, 150)
    test_derivations(planes, func, verbose=False)
    plane_creator.write_plane(planes, './chosen_datasets/circle_4_0_0_100_150')

def save_nlhmo():
    points = generate_harmonic_oscillator_nonlinear_points()

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 33, 38)
    test_derivations(planes, harmonic_nonlinear_oscillator_calc, verbose=True)
    plane_creator.write_plane(planes, './chosen_datasets/nlhmo_33_38')


if __name__ == '__main__':
    #linear_test()
    #sphere_test()
    #sqrt_test()
    #square_test()
    #hyperbola_test()
    #ellipse_test()
    #harmonic_oscillator_test()
    #circle_test()
    #nonlinear_harmonic_oscillator_test()

    #save_sphere()
    #save_hyperbola()
    #save_ellipse()
    #save_harmonic_oscillator()
    #save_circle()
    #save_nlhmo()
    for (dirpath, dirnames, filenames) in walk('./chosen_datasets'):
        for i, file in enumerate(filenames):
            src_filename = dirpath + "/" + file
            dest_filename =  "./chosen_points_datasets/" + file
            file = open(src_filename, 'r')
            lines = file.readlines()
            file.close()
            file = open(dest_filename, 'w')
            for i in range(len(lines)):
                if i == 0 or i % 2 == 1:
                    file.write(lines[i])
            file.close()