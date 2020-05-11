from plane_base import MultiDimPlane, PlaneCreator
import numpy as np
from functions import calculate_conic_coefficients

class ThirdOrderPolynomialPlane(MultiDimPlane):
    def __init__(self, center, coeffs):
        super().__init__(center, coeffs)

    def value_at(self, point):
        point_dim = len(point)
        result = 0.0
        count = 0

        # THIRD ORDER
        for dim1 in range(point_dim):
            squared = point[dim1] ** 2
            for dim2 in range(point_dim):
                result += self.coeffs[count] * squared * point[dim2]
                count += 1

        for dim1 in range(point_dim - 2):
            for dim2 in range(dim1 + 1, point_dim - 1):
                for dim3 in range(dim2 + 1, point_dim):
                    result += self.coeffs[count] * point[dim1] * point[dim2] * point[dim3]
                    count += 1

        # SECOND ORDER
        for dim in range(point_dim):
            result += self.coeffs[count] * point[dim] * point[dim]
            count += 1

        for dim1 in range(point_dim - 1):
            for dim2 in range(dim1 + 1, point_dim):
                result += self.coeffs[count] * point[dim1] * point[dim2]
                count += 1

        # FIRST ORDER
        for dim in range(point_dim):
            result += self.coeffs[count] * point[dim]
            count += 1

        result -= 1.0
        return result

class ThirdOrderPolynomialPlaneCreator(PlaneCreator):
    def get_plane_class(self):
        return ThirdOrderPolynomialPlane
    def get_X_matrix(self, lnf):
        point_dim = len(lnf.get_point(0))
        X = []

        for i in range(len(lnf.local_field)):
            point = lnf.get_point(i)
            X_row = []

            #THIRD ORDER
            for dim1 in range(point_dim):
                squared = point[dim1] ** 2
                for dim2 in range(point_dim):
                    X_row.append(squared * point[dim2])
            for dim1 in range(point_dim - 2):
                for dim2 in range(dim1 + 1, point_dim - 1):
                    for dim3 in range(dim2 + 1, point_dim):
                        X_row.append(point[dim1] * point[dim2] * point[dim3])

            #SECOND ORDER
            for dim in range(point_dim):
                X_row.append(point[dim] * point[dim])
            for dim1 in range(point_dim - 1):
                for dim2 in range(dim1 + 1, point_dim):
                    X_row.append(point[dim1] * point[dim2])

            #FIRST ORDER
            for dim in range(point_dim):
                X_row.append(point[dim])

            X.append(X_row)

        X_matrix = np.array(X)

        return X_matrix

    def calculate_conic_coefficients(self, lnf):
        return calculate_conic_coefficients(self.get_X_matrix(lnf))