from abc import ABC, abstractmethod
from functions import get_epsyloned_point
from lnf_util import LocalNeighboringField
from functions import calculate_conic_coefficients
import numpy as np


class MultiDimPlane(ABC):
    def __init__(self, center, coeffs):
        self.center = center
        self.coeffs = coeffs

    def get_dim(self):
        return len(self.center)

    def derivation_at(self, point, ind1, ind2):
        v1_eps = get_epsyloned_point(point, ind1)
        v2_eps = get_epsyloned_point(point, ind2)

        still = self.value_at(point)
        v1_moved = self.value_at(v1_eps)
        v2_moved = self.value_at(v2_eps)

        dv1 = v1_moved - still
        dv2 = v2_moved - still
        result = - dv2 / dv1

        return result

    def __repr__(self):
        s = ""
        point_line = " ".join([str(x) for x in self.center])
        coeffs_line = " ".join([str(x) for x in self.coeffs])

        s += point_line + "\n"
        s += coeffs_line + "\n"
        return s

    @staticmethod
    def get_no_planes(multi_planes):
        return len(multi_planes)

    @abstractmethod
    def value_at(self, point):
        pass


class PlaneCreator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_X_matrix(self, lnf):
        pass

    def import_plane(self, filename):
        self.import_processed_dataset(filename)

    def write_plane(self, planes, filename):
        self.write_processed_dataset(planes, filename)

    @abstractmethod
    def get_plane_class(self):
        pass

    def create_planes_for_dataset(self, points, low_no_neighbors, high_no_neighbors, verbose=False):
        successful_indexes = []
        multiplanes = []

        for i in range(len(points)):
            point = points[i]

            found = None
            multiplane_coeffs = None

            for no_neighbors in range(low_no_neighbors, high_no_neighbors + 1):
                lnf = LocalNeighboringField.get_local_field(point, points, no_neighbors)
                try:
                    multiplane_coeffs = calculate_conic_coefficients(self.get_X_matrix(lnf))
                    found = True
                    break
                except np.linalg.LinAlgError:
                    continue

            if not found:
                if verbose:
                    print("{}: Jebiga".format(i))
                continue

            successful_indexes.append(i)
            mp = self.get_plane_class()(point, multiplane_coeffs)
            multiplanes.append(mp)

            if verbose:
                print("{}/{}".format(i + 1, len(points)))

        print("No points: {}".format(len(successful_indexes)))
        return successful_indexes, multiplanes

    def import_processed_dataset(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        count = 0

        sample_size_str, var_size_str = lines[0].split()
        lines = lines[1:]
        sample_size, var_size = int(sample_size_str), int(var_size_str)
        multi_ellipses = []

        for i in range(sample_size):
            point_str = lines[count]
            count += 1

            multiellipse_str = lines[count]
            count += 1

            point = [float(x) for x in point_str.split()]
            coeffs = [float(x) for x in multiellipse_str.split()]
            multi_ellipses.append(self.get_plane_class()(point, coeffs))

        return multi_ellipses

    def write_processed_dataset(self, multi_planes, filename):
        sample_size = len(multi_planes)
        var_size = len(multi_planes[0].center)

        with open(filename, 'w') as f:
            f.write(str(sample_size) + " " + str(var_size) + "\n")
            for mp in multi_planes:
                f.write(str(mp))
