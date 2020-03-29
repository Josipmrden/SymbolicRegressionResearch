from sphere_points_generator import generate_sphere
from lnf_util import get_local_field
from fitting_conic_planes import Cone, get_cone
import numpy as np
import math

epsylon = 10E-5

class MultiCone:
    def __init__(self, center, cones):
        self.center = center
        self.cones = cones

    def get_derivation_at(self, point, ind1, ind2):
        cone = self.cones[(ind1, ind2)]
        v1 = point[ind1]
        v2 = point[ind2]

        return cone.derr_formula((v1, v2))

    @staticmethod
    def get_cones_for_dataset_ND(points, low_no_neighbors, high_no_neighbors):
        successful_indexes = []
        multi_cones = []
        var_size = len(points[0])

        for i in range(len(points)):
            point = points[i]

            found = None
            point_cones = {}
            for j in range(0, var_size - 1):
                for k in range(j+1, var_size):
                    found = False
                    cone = None
                    for no_neighbors in range(low_no_neighbors, high_no_neighbors+1):
                        lnf = get_local_field(point, points, no_neighbors)
                        try:
                            cone = get_cone(lnf, j, k)
                            found = True
                            break
                        except np.linalg.LinAlgError:
                            continue

                    if not found:
                        break
                    else:
                        point_cones[(j, k)] = cone
                if not found:
                    break
            if not found:
                print("Jebiga")
                continue
            #print("Appended {} / {}".format(i, len(points)))

            successful_indexes.append(i)
            mc = MultiCone(point, point_cones)
            multi_cones.append(mc)

        print("No points: {}".format(len(successful_indexes)))
        return successful_indexes, multi_cones

def calculate(point):
    x, y, z = point[0], point[1], point[2]
    return x*x + y*y + z*z - 25

def get_epsyloned_point(point, ind):
    new_point = []
    for i in range(len(point)):
        if i == ind:
            new_point.append(point[i] + epsylon)
        else:
            new_point.append(point[i])
    return new_point

def calculate_derivation(point, ind1, ind2):
    v1_eps = get_epsyloned_point(point, ind1)
    v2_eps = get_epsyloned_point(point, ind2)
    still = calculate(point)
    moved_v1 = calculate(v1_eps)
    moved_v2 = calculate(v2_eps)
    dv1 = moved_v1 - still
    dv2 = moved_v2 - still
    derr = - dv2/dv1

    return derr

def test_derivations(multi_cones, calculation_function, verbose=True):
    sample_size, var_size = len(multi_cones), len(multi_cones[0].center)
    error = 0.0
    combinations_no = var_size * (var_size - 1) / 2.0
    for i in range(sample_size):
        mc = multi_cones[i]
        point = mc.center
        for j in range(var_size - 1):
            for k in range(j + 1, var_size):
                conederr = mc.get_derivation_at(point, j, k)
                calc_derr = calculation_function(point, j, k)
                error += math.log(1 + math.fabs(conederr - calc_derr))
                if verbose:
                    print('{} {} {} {} {}'.format(i, j, k, calc_derr, conederr))

    error /= combinations_no

    return error

def read_dataset(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    sample_size_str, var_size_str = lines[0].split()
    lines = lines[1:]
    sample_size, var_size = int(sample_size_str), int(var_size_str)
    count = 0
    multi_cones = []
    for i in range(sample_size):
        point_str = lines[count]
        count += 1
        point = [float(x) for x in point_str.split()]
        cones = {}
        for j in range(var_size - 1):
            for k in range(j + 1, var_size):
                cone_str = lines[count]
                count += 1
                A, B, C, D, E = tuple([float(x) for x in cone_str.split()])
                cone = Cone(point, A, B, C, D, E)
                cones[(j, k)] = cone
        mc = MultiCone(point, cones)
        multi_cones.append(mc)
    return multi_cones

def write_multi_cones(multi_cones, filename):
    sample_size = len(multi_cones)
    var_size = len(multi_cones[0].center)

    with open(filename, 'w') as f:
        f.write(str(sample_size) + " " + str(var_size) + "\n")
        for mc in multi_cones:
            point_line = " ".join([str(x) for x in mc.center])
            f.write(point_line + "\n")
            for i in range(0, var_size - 1):
                for j in range(i + 1, var_size):
                    cone = mc.cones[(i, j)]
                    cone_line = " ".join([str(cone.A), str(cone.B), str(cone.C), str(cone.D), str(cone.E)])
                    f.write(cone_line + "\n")

def create_files_for_testing(radius, points_sizes, low_no_neighbors, high_no_neighbors):
    for size in points_sizes:
        print("Interval coefficient: {}".format(size))
        data = generate_sphere(radius, size)
        print("Size of the generated dataset: {}".format(len(data)))
        for i in range(len(low_no_neighbors)):
            low = low_no_neighbors[i]
            high = high_no_neighbors[i]

            indexes, multi_cones = MultiCone.get_cones_for_dataset_ND(data, low, high)

            filename = "./datasets/sphere_dataset{}-{}-{}.txt".format(size, low, high)
            write_multi_cones(multi_cones, filename)
            print("Saved " + filename)

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

#verified
def test_veracity_of_sphere():
    data = generate_sphere(5, 20)
    results = [float(calculate(x)) for x in data]
    print(sum(results))

if __name__ == '__main__':
    sizes = [15]
    lows = [30, 50, 70, 100, 150]
    highs = [30, 70, 100, 150, 200]
    #create_files_for_testing(5, sizes, lows, highs)
    test_derivations_from_files("./datasets/sphere_dataset", ".txt", sizes, lows, highs, verbose=False)
