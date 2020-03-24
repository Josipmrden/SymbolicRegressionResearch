import math
import numpy as np

class LocalNeighboringField:
    def __init__(self, center, local_field):
        self.center = center
        self.local_field = local_field

    def get_point(self, index):
        return self.local_field[index]

    def get_x(self, index):
        point = self.get_point(index)
        return point[0]

    def get_y(self, index):
        point = self.get_point(index)
        return point[1]

    def get_X_matrix(self):
        size = len(self.local_field)
        dim = (size, 5)
        X = np.zeros(dim)

        for i in range(size):
            x = (self.local_field[i])[0]
            y = (self.local_field[i])[1]
            X[i][0] = x * x
            X[i][1] = x * y
            X[i][2] = y * y
            X[i][3] = x
            X[i][4] = y

        return X

def get_distance(p1, p2):
    dist = 0.0
    for i in range(len(p1)):
        dist += (p1[i] - p2[i]) * (p1[i] - p2[i])
    return math.sqrt(dist)

def get_max_distance_index(distances):
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

    return index

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

    return max_distance

def get_local_field(center, points, no_neighbors):
    local_field = []
    distances = []

    max_distance = -1
    for i in range(len(points)):
        point = points[i]
        distance = get_distance(center, point)

        if len(local_field) < no_neighbors:
            local_field.append(point)
            distances.append(distance)
            if max_distance == -1 or max_distance < distance:
                max_distance = distance
        elif max_distance > distance:
            index = get_max_distance_index(distances)
            local_field[index] = point
            distances[index] = distance
            max_distance = get_max_distance(distances)

    return LocalNeighboringField(center, local_field)