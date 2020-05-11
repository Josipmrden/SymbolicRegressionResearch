import math
import numpy as np

epsylon = 10E-5

#((A^TxA)^-1)xA^Tx1
def calculate_conic_coefficients(x):
    xt = x.T
    ones = np.ones((x.shape[0], 1))
    xtx = np.matmul(xt, x)
    xtx1 = np.linalg.inv(xtx)
    xtx1xt = np.matmul(xtx1, xt)
    result = np.matmul(xtx1xt, ones)

    coeffs = [result[i][0] for i in range(x.shape[1])]
    return list(coeffs)

def least_squares_XAB(x, b):
    xt = x.T
    xtx = np.matmul(xt, x)
    xtx1 = np.linalg.inv(xtx)
    xtx1xt = np.matmul(xtx1, xt)
    result = np.matmul(xtx1xt, b)

    coeffs = [result[i][0] for i in range(x.shape[1])]
    return list(coeffs)

def get_derivation(func, point, ind1, ind2):
    v1_eps = get_epsyloned_point(point, ind1)
    v2_eps = get_epsyloned_point(point, ind2)
    still = func(point)
    moved_v1 = func(v1_eps)
    moved_v2 = func(v2_eps)
    dv1 = moved_v1 - still
    dv2 = moved_v2 - still
    derr = - dv2/dv1

    return derr

def get_epsyloned_point(point, ind):
    new_point = []
    for i in range(len(point)):
        if i == ind:
            new_point.append(point[i] + epsylon)
        else:
            new_point.append(point[i])
    return new_point

def calc_sphere_rad5_xc0_yc0_zc0(point):
    x, y, z = point[0], point[1], point[2]
    return x*x + y*y + z*z - 25

def sphere_calc_func(radius, xc, yc, zc):
    def calc_sphere(point):
        x, y, z = point[0], point[1], point[2]
        return (x-xc)**2 + (y-yc)**2 + (z-zc)**2 - radius*radius
    return calc_sphere

"""
Solved by Eureka: N0

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 16
"""
def calc_1_6_20_a(point):
    theta = point[0]
    f = point[1]
    return f - math.exp(-theta*theta / 2.0) / math.sqrt(2.0 * math.pi)

"""
Solved by Eureka: N0

Solved by AI-Feynman: YES
Data needed: 100
Solution time (s): 2992
"""
def calc_1_6_2(point):
    sigma = point[0]
    theta = point[1]
    f = point[2]
    return f - math.exp(-theta*theta / (2.0 * sigma * sigma)) / math.sqrt(2.0 * math.pi * sigma * sigma)


"""
Solved by Eureka: N0

Solved by AI-Feynman: YES
Data needed: 100
Solution time (s): 544
"""
def calc_1_8_14(point):
    x1 = point[0]
    x2 = point[1]
    y1 = point[2]
    y2 = point[3]
    d = point[4]
    return d - math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 12
"""
def calc_1_11_19(point):
    x1 = point[0]
    x2 = point[1]
    x3 = point[2]
    y1 = point[3]
    y2 = point[4]
    y3 = point[5]
    A = point[6]
    return A - (x1*y1 + x2*y2 + x3*y3)

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 100
Solution time (s): 184
"""
def calc_1_12_1(point):
    mi = point[0]
    nn = point[1]
    F = point[2]
    return F - mi * nn

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 22
"""
def calc_1_13_4(point):
    m = point[0]
    v = point[1]
    u = point[2]
    w = point[3]
    K = point[4]
    return K - 0.5*m*(v*v + u*u + w*w)

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 12
"""
def calc_1_14_3(point):
    m = point[0]
    g = point[1]
    z = point[2]
    U = point[3]
    return U - m*g*z

"""
Solved by Eureka: NO

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 13
"""
def calc_1_15_10(point):
    m0 = point[0]
    v = point[1]
    c = point[2]
    p = point[3]
    return p - m0*v / math.sqrt(1 - v**2/c**2)

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 17
"""
def calc_1_18_16(point):
    m = point[0]
    r = point[1]
    v = point[2]
    theta = point[3]
    L = point[4]
    return L - m *r*v*math.sin(theta)

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 100
Solution time (s): 530
"""
def calc_1_26_2(point):
    n = point[0]
    theta2 = point[1]
    theta1 = point[2]
    return theta1 - math.asin(n * math.sin(theta2))

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 100
Solution time (s): 7032
"""
def calc_1_37_4(point):
    I1 = point[0]
    I2 = point[1]
    delta = point[2]
    I_star = point[3]
    return I_star - (I1 + I2 + 2*math.sqrt(I1*I2)*math.cos(delta))

"""
Solved by Eureka: NO

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 20
"""
def calc_1_40_1(point):
    n0 = point[0]
    m = point[1]
    x = point[2]
    T = point[3]
    g = point[4]
    kb = point[5]
    n = point[6]
    return n - n0 * math.exp(-m*g*x/(kb*T))

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 29
"""
def calc_1_50_26(point):
    x1 = point[0]
    w = point[1]
    t = point[2]
    alpha = point[3]
    x = point[4]
    return x - x1 * (math.cos(w*t) + alpha*math.cos(w*t)*math.cos(w*t))

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 10
"""
def calc_2_4_23(point):
    q = point[0]
    e = point[1]
    r = point[2]
    Ve = point[3]
    return Ve - q / (4 * math.pi * e * r)

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 23
"""
def calc_2_6_15b(point):
    e = point[0]
    p_d = point[1]
    theta = point[2]
    r = point[3]
    Ef = point[4]
    return Ef - (3.0 / (4.0*math.pi*e)) * (p_d / r**3) * math.cos(theta) * math.sin(theta)

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 13
"""
def calc_2_10_9(point):
    qden = point[0]
    e = point[1]
    kappa = point[2]
    ef = point[3]
    return ef - (qden / e) * 1. / (1 + kappa)

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 21
"""
def calc_2_21_32(point):
    q = point[0]
    e = point[1]
    r = point[2]
    v = point[3]
    c = point[4]
    Ve = point[5]
    return Ve - q / (4 * math.pi * e * r * (1 - v / c))

"""
Solved by Eureka: NO

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 62
"""
def calc_2_24_17(point):
    w = point[0]
    c = point[1]
    d = point[2]
    k = point[3]
    return k - math.sqrt((w**2 / c**2) - (math.pi**2 / d**2))

"""
Solved by Eureka: NO

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 30
"""
def calc_2_35_18(point):
    n0 = point[0]
    kb = point[1]
    T = point[2]
    mim = point[3]
    B = point[4]
    n = point[5]
    return n - n0 / (math.exp(mim*B/kb/T) + math.exp(-mim*B/kb/T))

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 15
"""
def calc_2_37_1(point):
    mim = point[0]
    B = point[1]
    kappa = point[2]
    E = point[3]
    return E - mim * (1 + kappa) * B

"""
Solved by Eureka: NO

Solved by AI-Feynman: YES
Data needed: 1000
Solution time (s): 39
"""
def calc_3_8_54(point):
    E = point[0]
    t = point[1]
    hi = point[2]
    py = point[3]
    return py - math.sin(E * t / (hi/(2*math.pi))) ** 2

"""
Solved by Eureka: YES

Solved by AI-Feynman: YES
Data needed: 10
Solution time (s): 14
"""
def calc_3_15_12(point):
    U = point[0]
    k = point[1]
    d = point[2]
    E = point[3]
    return E - 2*U*(1 - math.cos(k*d))





