import numpy as np
from fitting_conic_planes_multidimensional import get_epsyloned_point, calculate, calculate_derivation
from sphere_points_generator import generate_sphere
from lnf_util import get_local_field
from fitting_conic_planes import calculate_conic_coefficients
import math

epsylon = 10E-5

class MultiDimEllipse:
    def __init__(self, center, coeffs):
        self.center = center
        self.coeffs = coeffs

    def get_dim(self):
        return len(self.center)

    def value_at(self, point):
        result = 0.0
        count = 0

        for i in range(self.get_dim()):
            result += self.coeffs[count] * point[i] * point[i]
            count += 1

        for i in range(self.get_dim() - 1):
            for j in range(i + 1, self.get_dim()):
                result += self.coeffs[count] * point[i] * point[j]
                count += 1

        for i in range(self.get_dim()):
            result += self.coeffs[count] * point[i]
            count += 1

        result -= 1.0

        return result

    def derivation_at(self, point, ind1, ind2):
        v1_eps = get_epsyloned_point(point, ind1)
        v2_eps = get_epsyloned_point(point, ind2)

        still = self.value_at(point)
        v1_moved = self.value_at(v1_eps)
        v2_moved = self.value_at(v2_eps)

        dv1 = v1_moved - still
        dv2 = v2_moved - still
        result = - dv2/dv1

        return result

    @staticmethod
    def get_multiellipse_for_dataset(points, low_no_neighbors, high_no_neighbors):
        successful_indexes = []
        multiellipses = []

        for i in range(len(points)):
            point = points[i]

            found = None
            multi_dim_ellipse_coeffs = None

            for no_neighbors in range(low_no_neighbors, high_no_neighbors+1):
                lnf = get_local_field(point, points, no_neighbors)
                try:
                    multi_dim_ellipse_coeffs = calculate_conic_coefficients(lnf.get_X_matrix_multidim())
                    found = True
                    break
                except np.linalg.LinAlgError:
                    continue

            if not found:
                print("{}: Jebiga".format(i))
                continue

            successful_indexes.append(i)
            mc = MultiDimEllipse(point, multi_dim_ellipse_coeffs)
            multiellipses.append(mc)

        print("No points: {}".format(len(successful_indexes)))
        return successful_indexes, multiellipses

def create_files_for_testing(path, ext, radius, points_sizes, low_no_neighbors, high_no_neighbors):
    for size in points_sizes:
        print("Interval coefficient: {}".format(size))
        data = generate_sphere(radius, size)
        print("Size of the generated dataset: {}".format(len(data)))
        for i in range(len(low_no_neighbors)):
            low = low_no_neighbors[i]
            high = high_no_neighbors[i]

            indexes, multi_ellipses = MultiDimEllipse.get_multiellipse_for_dataset(data, low, high)

            filename = "{}{}-{}-{}{}".format(path, size, low, high, ext)
            write_ellipses(multi_ellipses, filename)
            print("Saved " + filename)

def write_ellipses(multi_ellipses, filename):
    sample_size = len(multi_ellipses)
    var_size = len(multi_ellipses[0].center)

    with open(filename, 'w') as f:
        f.write(str(sample_size) + " " + str(var_size) + "\n")
        for me in multi_ellipses:
            point_line = " ".join([str(x) for x in me.center])
            f.write(point_line + "\n")
            coeffs_line = " ".join([str(x) for x in me.coeffs])
            f.write(coeffs_line + "\n")

def read_dataset(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    sample_size_str, var_size_str = lines[0].split()
    lines = lines[1:]
    sample_size, var_size = int(sample_size_str), int(var_size_str)
    count = 0
    multi_ellipses = []

    for i in range(sample_size):
        point_str = lines[count]
        count += 1
        multiellipse_str = lines[count]
        count += 1
        point = [float(x) for x in point_str.split()]
        coeffs = [float(x) for x in multiellipse_str.split()]
        multiellipse = MultiDimEllipse(point, coeffs)
        multi_ellipses.append(multiellipse)

    return multi_ellipses

def test_derivations(multi_ellipses, calculation_function, verbose=True):
    sample_size, var_size = len(multi_ellipses), len(multi_ellipses[0].center)
    error = 0.0
    combinations_no = var_size * (var_size - 1) / 2.0

    for i in range(len(multi_ellipses)):
        ellipse = multi_ellipses[i]
        point = ellipse.center
        for j in range(var_size - 1):
            for k in range(j + 1, var_size):
                conederr = ellipse.derivation_at(point, j, k)
                calc_derr = calculation_function(point, j, k)
                error += math.log(1 + math.fabs(conederr - calc_derr))
                if verbose:
                    print('{} {} {} {} {}'.format(i, j, k, calc_derr, conederr))

    error /= combinations_no

    return error

def test_derivations_from_files(path, ext, sizes, lows, highs, verbose):
    for size in sizes:
        for i in range(len(lows)):
            low = lows[i]
            high = highs[i]
            filename = "{}{}-{}-{}{}".format(path, size, low, high, ext)
            multi_cones = read_dataset(filename)
            print("Size of multicones: {}".format(len(multi_cones)))
            error = test_derivations(multi_cones, calculate_derivation, verbose=verbose)
            print("{} : {}".format(filename, error))

if __name__ == '__main__':
    sizes = [30]
    lows = [30, 50, 70, 100, 150]
    highs = [50, 70, 100, 150, 200]
    path = "./datasets/sphere_me"
    ext = ".txt"

    #create_files_for_testing(path, ext, 5, sizes, lows, highs)
    test_derivations_from_files(path, ext, sizes, lows, highs, verbose=True)