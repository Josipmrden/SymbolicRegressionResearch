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
from functions import calc_sphere_rad5_xc0_yc0_zc0, sphere_calc_func, calc_1_6_20_a, calc_1_18_4
import math

lows = [5, 10, 20, 50, 100, 200]
highs = [10, 20, 30, 60, 110, 220]
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

def generate_harmonic_oscillator_nonlinear_points_test():
    dataset = DataSet.import_dataset('./datasets/hmo_nl')
    points = dataset.data
    dataset_points = []
    for point in points:
        x = point[0]
        x_dot = point[1]
        x_dot_dot = 0.25 * x_dot * math.sin(x) + 11.4 * math.cos(x)
        dataset_points.append([x, x_dot, x_dot_dot])

    return DataSet(dataset_points)

def harmonic_nonlinear_oscillator_test_calc(point):
    x = point[0]
    x_dot = point[1]
    x_dot_dot = point[2]
    return x_dot_dot - 0.25 * x_dot * math.sin(x) - 11.4 * math.cos(x)

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

def linear_test(low, high):
    points = generate_linear_points1(1000, 1, 5)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, calc_func, verbose=False)
    return error

def only_points_dataset(low, high):
    points = DataSet.import_dataset('./datasets/Feynman_with_units/cut/I.18.4')
    calc_func = calc_1_18_4

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, calc_func, verbose=False)
    return error

def sphere_test(low, high):
    radius = 5
    points = DataSet(generate_sphere(radius, 20))
    sphere_func = sphere_calc_func(radius, 0, 0, 0)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, sphere_func, verbose=False)
    return error

def sqrt_test(low, high):
    points = generate_sqrt_points(1000, 1, 10)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, sqrt_calc, verbose=False)
    return error

def square_test(low, high):
    points = generate_square_points(1000, 1, 100)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, square_calc, verbose=False)
    return error

def hyperbola_test(low, high):
    points = generate_hyperbola_points(500, 1, 10)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, hyperbola_calc, verbose=False)
    return error

def ellipse_test(low, high):
    ra, rb, xc, yc = 3, 4, 1, 2
    points = generate_ellipse_points(1000, ra, rb, xc, yc)
    func = ellipse_func(ra, rb, xc, yc)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, func, verbose=False)
    return error

def moved_ellipse_test(low, high):
    ra, rb, xc, yc = 2.5, 5, 3, 4.5
    points = generate_ellipse_points(1000, ra, rb, xc, yc)
    func = ellipse_func(ra, rb, xc, yc)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, func, verbose=False)
    return error

def harmonic_oscillator_test(low, high):
    points = generate_harmonic_oscillator_points(1000, 0, 10)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error  = test_derivations(planes, harmonic_oscillator_calc, verbose=False)
    return error

def nonlinear_harmonic_oscillator_test(low, high):
    points = generate_harmonic_oscillator_nonlinear_points()

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, harmonic_nonlinear_oscillator_calc, verbose=False)
    return error

def nonlinear_harmonic_oscillator_test_test(low, high):
    points = generate_harmonic_oscillator_nonlinear_points_test()

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, harmonic_nonlinear_oscillator_calc, verbose=False)
    return error

def gauss_function_test(low, high):
    points = DataSet.import_dataset('./datasets/Feynman_with_units/cut/I.6.2a-1000')

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, calc_1_6_20_a, verbose=False)
    return error

def save_gauss_function_test():
    points = DataSet.import_dataset('./datasets/Feynman_with_units/cut/I.6.2a-1000')

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 200, 220)
    test_derivations(planes, calc_1_6_20_a, verbose=True)
    plane_creator.write_plane(planes, './chosen_datasets/gauss_200_220')
    DataSet.write_dataset(points, './chosen_points_datasets/gauss_200_220')

def circle_test(low, high):
    r, xc, yc = 5, 0, 0
    points = generate_circle_points(1000, r, xc, yc)
    func = circle_func(r, xc, yc)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, func, verbose=False)
    return error

def circle_moved_test(low, high):
    r, xc, yc = 6, 1, 2
    points = generate_circle_points(1000, r, xc, yc)
    func = circle_func(r, xc, yc)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
    #plot_kernel_with_dataset3D(points)
    error = test_derivations(planes, func, verbose=False)
    return error

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
    plane_creator.write_plane(planes, './chosen_datasets/hyperbolthree - 0.1 * two + 9.8 * sin(one)a_1.5_100_150')

def save_ellipse():
    ra, rb, xc, yc = 3, 4, 1, 2
    points = generate_ellipse_points(1000, ra, rb, xc, yc)
    func = ellipse_func(ra, rb, xc, yc)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 150, 200)
    test_derivations(planes, func, verbose=False)
    plane_creator.write_plane(planes, './chosen_datasets/ellipse_1_2_3_4_150_200')

def save_moved_ellipse():
    ra, rb, xc, yc = 2.5, 5, 3, 4.5
    points = generate_ellipse_points(1000, ra, rb, xc, yc)
    func = ellipse_func(ra, rb, xc, yc)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 150, 200)
    test_derivations(planes, func, verbose=False)
    plane_creator.write_plane(planes, './chosen_datasets/moved_ellipse_2.5_5_3_4.5_100_150')
    DataSet.write_dataset(points, './chosen_points_datasets/moved_ellipse_2.5_5_3_4.5_100_150')

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

def save_moved_circle():
    r, xc, yc = 6, 1, 2
    points = generate_circle_points(1000, r, xc, yc)
    func = circle_func(r, xc, yc)

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 100, 150)
    test_derivations(planes, func, verbose=False)
    #plane_creator.write_plane(planes, './chosen_datasets/moved_circle_6_1_2_100_150')
    DataSet.write_dataset(points, './chosen_points_datasets/moved_circle_6_1_2_100_150')

def save_nlhmo():
    points = generate_harmonic_oscillator_nonlinear_points()

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 33, 38)
    test_derivations(planes, harmonic_nonlinear_oscillator_calc, verbose=True)
    plane_creator.write_plane(planes, './chosen_datasets/nlhmo_33_38')

def save_nlhmo_test():
    points = generate_harmonic_oscillator_nonlinear_points()

    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 33, 38)
    test_derivations(planes, harmonic_nonlinear_oscillator_calc, verbose=True)
    plane_creator.write_plane(planes, './chosen_datasets/nlhmo_33_38')

def calculate_averages_of_planes(test):
    for (l, h) in zip(lows, highs):
        results = []
        for i in range(5):
            error, zo = test(l, h)
            results.append(error)
        print(f"Average: {np.average(results)}")
        print(f"Std: {np.std(results)}")

if __name__ == '__main__':
    #linear_test()
    #sqrt_test()
    #square_test()
    #calculate_averages_of_planes(circle_test)
    #calculate_averages_of_planes(sphere_test)
    #calculate_averages_of_planes(ellipse_test)
    #calculate_averages_of_planes(hyperbola_test)
    #calculate_averages_of_planes(harmonic_oscillator_test)
    #calculate_averages_of_planes(nonlinear_harmonic_oscillator_test)
    #calculate_averages_of_planes(linear_test)
    #calculate_averages_of_panes(sqrt_test)
    #calculate_averages_of_planes(square_test)
    #calculate_averages_of_planes(circle_moved_test)
    #calculate_averages_of_planes(moved_ellipse_test)
    #calculate_averages_of_planes(nonlinear_harmonic_oscillator_test_test)
    #calculate_averages_of_planes(gauss_function_test)
    #save_gauss_function_test()
    calculate_averages_of_planes(only_points_dataset)