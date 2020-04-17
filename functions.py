import math

epsylon = 10E-5

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

def calc1_6_20_a(point):
    theta = point[0]
    f = point[1]
    return f - math.exp(-theta*theta / 2.0) / math.sqrt(2.0 * math.pi)