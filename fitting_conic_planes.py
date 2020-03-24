import random
import math
from implicit_derivative_calculator import read_file
from lnf_util import get_local_field
import numpy as np

epsylon = 10E-5

class Cone:
    def __init__(self, center, A, B, C, D, E):
        self.center = center
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E

    def value(self):
        x = self.center[0]
        y = self.center[1]
        A = self.A
        B = self.B
        C = self.C
        D = self.D
        E = self.E

        result = A*x*x + B*x*y + C*y*y + D*x + E*y - 1

        return result

    def value_at(self, point):
        x = point[0]
        y = point[1]
        A = self.A
        B = self.B
        C = self.C
        D = self.D
        E = self.E

        result = A*x*x + B*x*y + C*y*y + D*x + E*y - 1

        return result

    def derr_x(self):
        x = self.center[0]
        y = self.center[1]
        A = self.A
        B = self.B
        D = self.D
        result = 2*A*x + B*y + D
        return result

    def derr_y(self):
        x = self.center[0]
        y = self.center[1]
        B = self.B
        C = self.C
        E = self.E
        result = 2*C*y + B*x + E
        return result

    def derr_formula(self):
        x = self.center[0]
        y = self.center[1]
        x_eps = x + epsylon
        y_eps = y + epsylon
        still = self.value()
        x_moved = self.value_at((x_eps, y))
        y_moved = self.value_at((x, y_eps))
        dx = x_moved - still
        dy = y_moved - still
        result = - dy/dx
        return result

    def implicit_derivative(self):
        pass

    def derr_determinant(self):
        A = self.A
        B = self.B
        C = self.C
        D = self.D
        E = self.E

        first = A * (C - E * E * 0.25)
        second = B * 0.5 * (B * 0.5 - D * E * 0.25)
        third = D * 0.5 * (B * E * 0.25 - C * D * 0.5)
        result = first - second + third

        return result

def get_cones_for_dataset(points, low_no_neighbors, high_no_neighbors):
    global no_neighbors
    successful_indexes = []
    cones = []

    for i in range(len(points)):
        point = points[i]

        found = False
        cone = None

        for no_neighbors in range(low_no_neighbors, high_no_neighbors):
            lnf = get_local_field(point, points, no_neighbors)
            try:
                cone = get_cone(lnf)
                found = True
                break
            except np.linalg.LinAlgError:
                continue

        if not found:
            print("{} Jebiga".format(i))
        else:
            successful_indexes.append(i)
            cones.append(cone)

    return successful_indexes, cones

def fill_experimental_values(points):
    experimental_derivations = []

    for i in range(len(points)):
        point = points[i]
        currentVarValues = point

        if i == 0:
            nextVarValues = points[i + 1]
            dx = nextVarValues[0] - currentVarValues[0]
            dy = nextVarValues[1] - currentVarValues[1]
        elif i == len(points) - 1:
            prevVarValues = points[i - 1]
            dx = currentVarValues[0] - prevVarValues[0]
            dy = currentVarValues[1] - prevVarValues[1]
        else:
            nextVarValues = points[i + 1]
            prevVarValues = points[i - 1]
            dx = nextVarValues[0] - prevVarValues[0]
            dy = nextVarValues[1] - prevVarValues[1]

            if math.fabs(dy) < epsylon:
                dy = nextVarValues[1] - currentVarValues[1]

        derrex = dx / dy
        experimental_derivations.append(derrex)

    return experimental_derivations

def derivatives_test(points, derivation_calculation_function, low, high):
    experimentaldxdy = fill_experimental_values(points)
    indexes, cones = get_cones_for_dataset(points, low_no_neighbors=low, high_no_neighbors=high)

    log1 = 0.0
    log2 = 0.0
    log3 = 0.0
    log4 = 0.0
    for i in range(len(indexes)):
        index = indexes[i]
        point = points[i]

        experimental = experimentaldxdy[index]
        cone = cones[i]
        actual = derivation_calculation_function(point)

        derr_x = cone.derr_x()
        derr_y = cone.derr_y()

        derr_determinant = cone.derr_determinant()
        derrc = - derr_y / derr_x

        derr_formula = cone.derr_formula()


        print('{} {} {} {} {} {}'.format(index, experimental, actual, derrc, derr_determinant, derr_formula))
        log1 += math.log(1 + abs(actual - experimental))
        log2 += math.log(1 + abs(actual - derrc))
        log3 += math.log(1 + abs(actual - derr_determinant))
        log4 += math.log(1 + abs(actual - derr_formula))
    print("1. Index, 2. Experimental, 3. Calculation, 4. Derivation of cone implicit, 5. Derivation by determinant of coeffs, 6. Derivation by formula of cone")
    print("#NO indexes: {}".format(len(indexes)))

    print(log1)
    print(log2)
    print(log3)
    print(log4)

def calculate(x, y):
    return x*x + y*y - 25

def calculate_derivation(point):
    x = point[0]
    y = point[1]
    x_eps = x + epsylon
    y_eps = y + epsylon
    still = calculate(x, y)
    moved_x = calculate(x_eps, y)
    moved_y = calculate(x, y_eps)
    dx = moved_x - still
    dy = moved_y - still
    derr = - dy/dx

    return derr

def calculate_conic_coefficients(x):
    xt = x.T
    ones = np.ones((x.shape[0], 1))
    xtx = np.matmul(xt, x)
    xtx1 = np.linalg.inv(xtx)
    xtx1xt = np.matmul(xtx1, xt)
    result = np.matmul(xtx1xt, ones)

    A = result[0][0]
    B = result[1][0]
    C = result[2][0]
    D = result[3][0]
    E = result[4][0]

    return A,B,C,D,E

def get_cone(lnf):
    x = lnf.get_X_matrix()
    A,B,C,D,E = calculate_conic_coefficients(x)
    cone = Cone(lnf.center, A, B, C, D, E)
    return cone

def get_data_for_writing(points, low_no_neighbors, high_no_neighbors):
    indexes, cones = get_cones_for_dataset(points, low_no_neighbors, high_no_neighbors)
    print("Total number of points: {}".format(len(points)))
    print("Total number of cones: {}".format(len(cones)))
    print("Percent of points used: {}".format(len(cones)/len(points)))
    return cones

def write_data(cones, filename, sample_length, var_length):
    with open(filename, 'w') as f:
        f.write(str(sample_length) + " " + str(var_length) + "\n")
        for cone in cones:
            #print('{}'.format(-cone.derr_y() / cone.derr_x()))
            center = cone.center
            A, B, C, D, E = cone.A, cone.B, cone.C, cone.D, cone.E
            center_params = [str(x) for x in center]
            coeff_params = [str(x) for x in [A, B, C, D, E]]
            center_line = " ".join(center_params)
            coeff_line = " ".join(coeff_params)
            f.write(center_line + "\n")
            f.write(coeff_line + "\n")

        f.close()

if __name__ == '__main__':
    sample_length, var_length, points = read_file('./datasets/ordered.txt')

    derivatives_test(points, calculate_derivation, low=100, high=150)
    #data = get_data_for_writing(points, low_no_neighbors=100, high_no_neighbors=150)
    #write_data(data, './datasets/cones_circle_unordered.txt', sample_length, var_length)