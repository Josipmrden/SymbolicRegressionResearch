from sphere_points_generator import generate_sphere
from functions import get_derivation, calc_sphere_rad5_xc0_yc0_zc0, calculate_conic_coefficients
import math
from setup import *

class MultiDimEllipse(MultiDimPlane):
    def __init__(self, center, coeffs):
        super().__init__(center, coeffs)

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

class MultiDimEllipseCreator(PlaneCreator):
    def get_plane_class(self):
        return MultiDimEllipse

    def get_squared_no_columns(self, lnf):
        return int(len(lnf.get_point(0)))
    def get_linear_no_columns(self, lnf):
        return int(len(lnf.get_point(0)))
    def get_covariate_no_columns(self, lnf):
        point_dim = len(lnf.get_point(0))
        return int(point_dim * (point_dim - 1) / 2.0)
    def get_no_columns_multidim(self, lnf):
        return self.get_squared_no_columns(lnf) + self.get_linear_no_columns(lnf) + self.get_covariate_no_columns(lnf)
    def get_X_matrix(self, lnf):
        size = len(lnf.local_field)
        point_dim = len(lnf.get_point(0))
        no_columns = self.get_no_columns_multidim(lnf)
        dim = (size, no_columns)
        X = np.zeros(dim)

        squared = self.get_squared_no_columns(lnf)
        linear = self.get_linear_no_columns(lnf)

        for i in range(size):
            point = lnf.get_point(i)
            count = 0

            for j in range(squared):
                X[i][count] = point[j] * point[j]
                count += 1

            for j in range(point_dim - 1):
                for k in range(j + 1, point_dim):
                    X[i][count] = point[j] * point[k]
                    count += 1

            for j in range(linear):
                X[i][count] = point[j]
                count += 1
        return X

    def calculate_conic_coefficients(self, lnf):
        return calculate_conic_coefficients(self.get_X_matrix(lnf))

def create_sphere_files(path, ext, radius, points_sizes, low_no_neighbors, high_no_neighbors):
    for size in points_sizes:
        print("Interval coefficient: {}".format(size))
        data = generate_sphere(radius, size)
        print("Size of the generated dataset: {}".format(len(data)))

        for i in range(len(low_no_neighbors)):
            low = low_no_neighbors[i]
            high = high_no_neighbors[i]
            indexes, multi_ellipses = plane_creator.create_planes_for_dataset(data, low, high)

            filename = "{}{}-{}-{}{}".format(path, size, low, high, ext)
            plane_creator.write_processed_dataset(multi_ellipses, filename)
            print("Saved " + filename)

def test_derivations(multi_ellipses, derivation_func, verbose=True):
    sample_size, var_size = len(multi_ellipses), len(multi_ellipses[0].center)
    error = 0.0

    for i in range(len(multi_ellipses)):
        ellipse = multi_ellipses[i]
        point = ellipse.center
        for j in range(var_size - 1):
            for k in range(j + 1, var_size):
                conederr = ellipse.derivation_at(point, j, k)
                calc_derr = derivation_func(calc_sphere_rad5_xc0_yc0_zc0, point, j, k)
                error += math.log(1 + math.fabs(conederr - calc_derr))
                if verbose:
                    print('{} {} {} {} {}'.format(i, j, k, calc_derr, conederr))

    error /= len(multi_ellipses)

    return error

def test_derivations_from_files(path, ext, sizes, lows, highs, verbose):
    for size in sizes:
        for i in range(len(lows)):
            low = lows[i]
            high = highs[i]
            filename = "{}{}-{}-{}{}".format(path, size, low, high, ext)
            multi_cones = plane_creator.import_plane(filename)
            print("Size of multicones: {}".format(len(multi_cones)))
            error = test_derivations(multi_cones, get_derivation, verbose=verbose)
            print("{} : {}".format(filename, error))

if __name__ == '__main__':
    sizes = [30]
    lows = [30, 50, 70, 100, 150]
    highs = [50, 70, 100, 150, 200]
    path = "./datasets/sphere_me"
    ext = ".txt"
    radius = 5

    plane_creator = MultiDimEllipseCreator()
    #create_sphere_files(path, ext, radius, sizes, lows, highs)
    ellipses = plane_creator.import_processed_dataset("./datasets/sphere_me30-150-200.txt")
    error = test_derivations(ellipses, get_derivation)
    print(str(error))
    #test_derivations_from_files(path, ext, sizes, lows, highs, verbose=False)