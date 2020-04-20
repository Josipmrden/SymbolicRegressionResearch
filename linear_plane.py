from setup import *

class MultiLinearCovariatePlane(MultiDimPlane):
    def __init__(self, center, coeffs):
        super().__init__(center, coeffs)

    def value_at(self, point):
        result = 0.0
        count = 0

        for i in range(self.get_dim()):
            result += self.coeffs[count] * point[i]
            count += 1

        for i in range(self.get_dim() - 1):
            for j in range(i + 1, self.get_dim()):
                result += self.coeffs[count] * point[i] * point[j]
                count += 1

        result -= 1.0

        return result

class MultiLinearCovariatePlaneCreator(PlaneCreator):
    def get_plane_class(self):
        return MultiLinearCovariatePlane
    def get_linear_no_columns(self, lnf):
        return int(len(lnf.get_point(0)))
    def get_covariate_no_columns(self, lnf):
        point_dim = len(lnf.get_point(0))
        return int(point_dim * (point_dim - 1) / 2.0)
    def get_no_columns_multidim(self, lnf):
        return self.get_linear_no_columns(lnf) + self.get_covariate_no_columns(lnf)

    def get_X_matrix(self, lnf):
        size = len(lnf.local_field)
        no_columns = self.get_no_columns_multidim(lnf)
        point_dim = len(lnf.get_point(0))
        dim = (size, no_columns)
        X = np.zeros(dim)

        for i in range(size):
            point = lnf.get_point(i)
            count = 0

            for j in range(len(point)):
                X[i][count] = point[j]
                count += 1

            for j in range(point_dim - 1):
                for k in range(j + 1, point_dim):
                    X[i][count] = point[j] * point[k]
                    count += 1

        return X

class MultiLinearBasicPlane(MultiDimPlane):
    def __init__(self, center, coeffs):
        super().__init__(center, coeffs)

    def value_at(self, point):
        result = 0.0

        for i in range(self.get_dim()):
            result += self.coeffs[i] * point[i]

        result -= 1.0

        return result

class MultiLinearBasicPlaneCreator(PlaneCreator):
    def get_plane_class(self):
        return MultiLinearBasicPlane

    def get_X_matrix(self, lnf):
        size = len(lnf.local_field)
        point_dim = len(lnf.get_point(0))
        dim = (size, point_dim)
        X = np.zeros(dim)

        for i in range(size):
            point = lnf.get_point(i)
            count = 0

            for j in range(len(point)):
                X[i][count] = point[j]
                count += 1

        return X

