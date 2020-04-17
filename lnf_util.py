import math
import numpy as np

class LocalNeighboringField:
    def __init__(self, center, local_field):
        self.center = center
        self.local_field = local_field

    def get_point(self, index):
        return self.local_field[index]

    def get_squared_no_columns(self):
        return int(len(self.local_field[0]))
    def get_linear_no_columns(self):
        return int(len(self.local_field[0]))
    def get_covariate_no_columns(self):
        point_dim = len(self.local_field[0])
        return int(point_dim * (point_dim - 1) / 2.0)
    def get_no_columns_multidim(self):
        return self.get_squared_no_columns() + self.get_linear_no_columns() + self.get_covariate_no_columns()

    def get_2D_X_matrix(self, ind1, ind2):
        size = len(self.local_field)
        dim = (size, 5)
        X = np.zeros(dim)

        for i in range(size):
            x = (self.local_field[i])[ind1]
            y = (self.local_field[i])[ind2]
            X[i][0] = x * x
            X[i][1] = y * y
            X[i][2] = x * y
            X[i][3] = x
            X[i][4] = y

        return X

    def get_X_matrix_multidim(self):
        size = len(self.local_field)
        point_dim = len(self.local_field[0])
        no_columns = self.get_no_columns_multidim()
        dim = (size, no_columns)
        X = np.zeros(dim)

        squared = self.get_squared_no_columns()
        linear = self.get_linear_no_columns()

        for i in range(size):
            point = self.local_field[i]
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

    @staticmethod
    def get_local_field(center, points, no_neighbors):
        local_field = []
        distances = []

        max_distance = -1
        max_index = -1
        for i in range(len(points)):
            point = points[i]
            distance = LocalNeighboringField.get_distance_between_points(center, point)

            if len(local_field) < no_neighbors:
                local_field.append(point)
                distances.append(distance)
                if max_distance == -1 or max_distance < distance:
                    max_distance = distance
                    max_index = i
            elif max_distance > distance:
                local_field[max_index] = point
                distances[max_index] = distance
                max_distance, max_index = LocalNeighboringField.get_max_distance(distances)

        return LocalNeighboringField(center, local_field)

    @staticmethod
    def get_distance_between_points(p1, p2):
        dist = 0.0
        for i in range(len(p1)):
            dist += (p1[i] - p2[i]) * (p1[i] - p2[i])
        return math.sqrt(dist)

    @staticmethod
    def get_max_distance(distances):
        max_distance = -1
        index = -1

        for i in range(len(distances)):
            distance = distances[i]
            if index == -1:
                index = i
                max_distance = distance
                continue
            if distance > max_distance:
                index = i
                max_distance = distance

        return max_distance, index