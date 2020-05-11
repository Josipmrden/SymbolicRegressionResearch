from functions import *
from os import walk
from ellipse_plane import *
from dataset_analyzer import DataSet, DataPreprocessor
from polynomial_plane import *

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
    print(f"Zero offset: {offset_from_zero_total}, Derivation error: {error}, #NO. Planes: {len(multi_ellipses)}")
    return error, offset_from_zero_total

def test_bench(plane_creator, filename, calculation_func, verbose=False):
    planes = plane_creator.import_processed_dataset(filename)
    error, offset_from_zero_total = test_derivations(planes, calculation_func, verbose=verbose)

def test_multiple_files(plane_creator, start_directory, dataset_filenames, calculation_functions):
    for (dirpath, dirnames, filenames) in walk(start_directory):
        for i, file in enumerate(filenames):
            src_filename = dirpath + "/" + file
            for dataset_file, calc_func in zip(dataset_filenames, calculation_functions):
                if dataset_file in src_filename:
                    test_bench(plane_creator, src_filename, calc_func)

if __name__ == '__main__':
    dataset_name = "I.6.2a"
    calc_func = calc_1_6_20_a
    no_samples = 1000
    lows = [10, 20, 30, 40, 50, 60, 100, 200, 300]
    highs = [20, 30, 40, 50, 60, 70, 150, 250, 350]
    plane_creator = MultiDimEllipseCreator()

    cut = True
    process = True
    calc_error = True
    verbose = False

    original_filename = f"./datasets/Feynman_with_units/original/{dataset_name}"
    cut_filename = f"./datasets/Feynman_with_units/cut/{dataset_name}-{no_samples}"

    if cut:
        DataSet.cut_dataset(original_filename, cut_filename, no_samples)
    for low, high in zip(lows, highs):
        processed_filename = f"./poc/{dataset_name}-{no_samples}-{low}-{high}"
        if process:
            DataPreprocessor.preprocess_dataset(plane_creator, cut_filename, low, high, processed_filename)
        if calc_error:
            test_bench(plane_creator, processed_filename, calc_func, verbose=verbose)