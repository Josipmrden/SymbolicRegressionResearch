from functions import *
from os import walk
from ellipse_plane import *

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
                offset_from_zero_total += math.fabs(offset_from_zero)
                error += math.log(1 + math.fabs(conederr - calc_derr))
                if verbose:
                    print('{} {} {} {} {} {}'.format(i, j, k, calc_derr, conederr, offset_from_zero))

    error /= len(multi_ellipses)
    print(f"Zero offset: {offset_from_zero_total}, Derivation error: {error}, #NO Ellipses: {len(multi_ellipses)}")
    return error, offset_from_zero_total

def test_bench(plane_creator, filename, calculation_func, verbose=False):
    planes = plane_creator.import_processed_dataset(filename)
    error, offset_from_zero_total = test_derivations(planes, calculation_func, verbose=verbose)
    print(f"{filename} -> Zero offset: {offset_from_zero_total}, Derivation error: {error}, #NO Planes: {len(planes)}")

def test_multiple_files(plane_creator, start_directory, dataset_filenames, calculation_functions):
    for (dirpath, dirnames, filenames) in walk(start_directory):
        for i, file in enumerate(filenames):
            src_filename = dirpath + "/" + file
            for dataset_file, calc_func in zip(dataset_filenames, calculation_functions):
                if dataset_file in src_filename:
                    test_bench(plane_creator, src_filename, calc_func)

if __name__ == '__main__':
    #test_bench('poc/162a-100000-50-100', calc1_6_20_a, verbose=False)
    plane_creator = MultiDimEllipseCreator()
    test_bench(plane_creator, 'poc/162a-2500-300-350', calc_1_6_20_a)
    #test_bench('poc/162a-100000-50-100', calc1_6_20_a, verbose=False)
    filenames = [
        'I.6.2a',
        'I.8.14',
        'I.11.19',
        'I.13.4',
        'I.14.3',
        'I.15.10',
        'I.18.14',
        'I.26.2',
        'I.37.4',
        'I.40.1',
        'I.50.26',
        'II.4.23',
        'II.6.15b',
        'II.10.9',
        'II.21.32',
        'II.24.17',
        'II.35.18',
        'II.37.1',
        'III.8.54',
        'III.15.12',
    ]
    calc_funcs = [
        calc_1_6_20_a,
        calc_1_8_14,
        calc_1_11_19,
        calc_1_13_4,
        calc_1_14_3,
        calc_1_15_10,
        calc_1_18_16,
        calc_1_26_2,
        calc_1_37_4,
        calc_1_40_1,
        calc_1_50_26,
        calc_2_4_23,
        calc_2_6_15b,
        calc_2_10_9,
        calc_2_21_32,
        calc_2_24_17,
        calc_2_35_18,
        calc_2_37_1,
        calc_3_8_54,
        calc_3_15_12
    ]
    test_multiple_files(plane_creator, './datasets/Feynman_with_units/processed_datasets', filenames, calc_funcs)