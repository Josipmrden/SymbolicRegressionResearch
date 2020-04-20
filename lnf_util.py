import math
import numpy as np
import bisect

class LocalNeighboringField:
    def __init__(self, center, local_field):
        self.center = center
        self.local_field = local_field

    def get_local_field_element(self, index):
        return self.local_field[index]

    def get_point(self, index):
        return self.get_local_field_element(index)[1]

    def get_2D_X_matrix(self, ind1, ind2):
        size = len(self.local_field)
        dim = (size, 5)
        X = np.zeros(dim)

        for i in range(size):
            x = (self.get_point(i))[ind1]
            y = (self.get_point(i))[ind2]
            X[i][0] = x * x
            X[i][1] = y * y
            X[i][2] = x * y
            X[i][3] = x
            X[i][4] = y

        return X

    @staticmethod
    def get_local_field(center, points, no_neighbors):
        local_field = []
        max_distance = -1

        for i in range(len(points)):
            point = points[i]
            distance = LocalNeighboringField.get_distance_between_points(center, point)
            element = (distance, point)

            if len(local_field) < no_neighbors:
                bisect.insort(local_field, element)
            elif max_distance > distance:
                local_field = local_field[:no_neighbors - 1]
                bisect.insort(local_field, element)

            if max_distance == -1 or max_distance < distance:
                max_distance = distance

        return LocalNeighboringField(center, local_field)

    @staticmethod
    def get_distance_between_points(p1, p2):
        dist = 0.0
        for i in range(len(p1)):
            dist += (p1[i] - p2[i]) * (p1[i] - p2[i])
        return math.sqrt(dist)

def import_dataset(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()

    sample_size = len(lines)
    data = []
    for i in range(sample_size):
        sample_str = lines[i]
        data.append([float(x) for x in sample_str.split()])

    return data

if __name__ == '__main__':
    points = import_dataset('./datasets/Feynman_with_units/cut/I.13.4-100')
    distances_dict = {}

    for center in points:
        lnf = LocalNeighboringField.get_local_field(center, points, 10)
