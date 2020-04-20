import random
from dataset_analyzer import DataPreprocessor, DataSet
from feynmann_equation_derivation_testbench import test_derivations
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ellipse_plane import MultiDimEllipseCreator, MultiDimEllipse
from linear_plane import \
    MultiLinearCovariatePlaneCreator, \
    MultiLinearBasicPlaneCreator, \
    MultiLinearBasicPlane, \
    MultiLinearCovariatePlane
from plane_base import *
from sphere_points_generator import generate_sphere
from functions import calc_sphere_rad5_xc0_yc0_zc0

def plot_kernel_with_dataset3D(dataset):
    data = dataset.data
    fig = plt.figure()
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

def linear_test():
    points = generate_linear_points1(1000, 1, 5)
    lows = [10]
    highs = [20]
    plane_creator = MultiLinearBasicPlaneCreator()
    for low, high in zip(lows, highs):
        planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, low, high)
        plot_kernel_with_dataset3D(points)
        test_derivations(planes, calc_func, verbose=False)

def sphere_test():
    points = DataSet(generate_sphere(5, 30))
    plane_creator = MultiDimEllipseCreator()
    planes = DataPreprocessor.get_planes_for_dataset(plane_creator, points, 10, 20)
    test_derivations(planes, calc_sphere_rad5_xc0_yc0_zc0, verbose=False)

if __name__ == '__main__':
    linear_test()
    sphere_test()