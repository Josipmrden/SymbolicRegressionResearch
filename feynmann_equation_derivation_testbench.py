from multi_dimensional_ellipse import MultiDimEllipse
from functions import *

def test_derivations(multi_ellipses, func, verbose=True):
    sample_size, var_size = len(multi_ellipses), len(multi_ellipses[0].center)
    error = 0.0
    offset_from_zero_total = 0.0
    for i in range(len(multi_ellipses)):
        ellipse = multi_ellipses[i]
        point = ellipse.center
        for j in range(var_size - 1):
            for k in range(j + 1, var_size):
                conederr = ellipse.derivation_at(point, j, k)
                calc_derr = get_derivation(func, point, j, k)
                offset_from_zero = func(point)
                offset_from_zero_total += offset_from_zero
                error += math.log(1 + math.fabs(conederr - calc_derr))
                if verbose:
                    print('{} {} {} {} {} {}'.format(i, j, k, calc_derr, conederr, offset_from_zero))

    error /= len(multi_ellipses)

    return error, offset_from_zero_total

def test_bench(filename, calculation_func, verbose=True):
    ellipses = MultiDimEllipse.import_processed_dataset(filename)
    error, offset_from_zero_total = test_derivations(ellipses, calculation_func, verbose=verbose)
    print(str(error))
    print(str(offset_from_zero_total))

def test_multiple_files(filenames, calculation_functions):
    for i in range(len(filenames)):
        filename = filenames[i]
        func = calculation_functions[i]
        test_bench(filename, func)

if __name__ == '__main__':
    #test_bench('poc/162a-100000-50-100', calc1_6_20_a, verbose=False)
    test_bench('poc/162a-2500-300-350', calc1_6_20_a, verbose=True)
    #test_bench('poc/162a-100000-50-100', calc1_6_20_a, verbose=False)