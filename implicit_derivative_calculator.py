import math
epsylon = 10e-5

def testComparability(points):
    dxdy = []
    assumed = []
    by_equation = []
    for i in range(len(points)):
        point = points[i]
        currentVarValues = point
        if i == 0:
            nextVarValues = points[i+1]
            dxexp = nextVarValues[0] - currentVarValues[0]
            dyexp = nextVarValues[1] - currentVarValues[1]
        elif i == len(points) - 1:
            prevVarValues = points[i -1]
            dxexp = currentVarValues[0] - prevVarValues[0]
            dyexp = currentVarValues[1] - prevVarValues[1]
        else:
            nextVarValues = points[i+1]
            prevVarValues = points[i-1]
            dxexp = nextVarValues[0] - prevVarValues[0]
            dyexp = nextVarValues[1] - prevVarValues[1]

            if (math.fabs(dyexp) < epsylon):
                dyexp = nextVarValues[1] - currentVarValues[1]

        derivation = dxexp / dyexp
        dxdy.append(derivation)

        afterx = calculate(point[0] + epsylon, point[1])
        aftery = calculate(point[0], point[1] + epsylon)

        still = calculate(point[0], point[1])
        dxafter = (afterx - still) / epsylon
        dyafter = (aftery - still) / epsylon

        derivation_assumed = - dyafter / dxafter
        assumed.append(derivation_assumed)
        if point[0] == 0:
            derivation_by_equation = "Infinity"
        else:
            derivation_by_equation = -point[1] / point[0]
        by_equation.append(derivation_by_equation)

    fitness = 0.0
    for i in range(len(assumed)):
        actual = dxdy[i]
        real = assumed[i]
        by_eq = by_equation[i]
        print('{0} {1} {2}'.format(actual, real, by_eq))
        fitness += math.log(1 + math.fabs(actual - real))

    print("Fitness: {0}".format(fitness))


#napraviti isti kurac ko u c++ da se vidi greška
# def calculate(x, y):
#     return x*x + y*y - 25
def calculate(x, y):
    return x*x + y*y - 1

def test_derivatives(points):
    for i in range(len(points)):
        point = points[i]
        movedx = calculate(point[0] + epsylon, point[1])
        still = calculate(point[0], point[1])
        movedy = calculate(point[0], point[1] + epsylon)
        moved_x = calculate(point[0] - epsylon, point[1])
        moved_y = calculate(point[0], point[1] - epsylon)

        dx = (movedx - still) / epsylon
        dy = (movedy - still) / epsylon
        dx_ = (still - moved_x) / epsylon
        dy_ = (still - moved_y) / epsylon
        result = dy / dx
        result_ = dy_ / dx_
        result_ = (result_ + result) / 2
        actual = point[1] / point[0]

        print('{0} {1} {2}'.format(result, result_, actual))

def test_implicit_derivative(point):

    pass

def read_file(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()

    sample_length, var_length = None, None
    points = []

    for i in range(len(lines)):
        line = lines[i]
        params = line.split()
        if i == 0:
            sample_length = int(params[0])
            var_length = int(params[1])
        else:
            points.append([float(var) for var in params])

    return sample_length, var_length, points

if __name__ == '__main__':
    _, _, points = read_file('./datasets/ordered.txt')

    testComparability(points)

