from functions import *
from ellipse_plane import MultiDimEllipseCreator, MultiDimEllipse
from linear_plane import MultiLinearBasicPlaneCreator, MultiLinearBasicPlane, \
    MultiLinearCovariatePlaneCreator, MultiLinearCovariatePlane

def evaluate_function_error(points, func, verbose=False, name=None):
    total_offset = 0.0
    for i in range(len(points)):
        p = points[i]
        evaluation = func(p)
        if verbose:
            print(f"{i+1}: {evaluation}")
        total_offset += math.fabs(evaluation)
    if name is None:
        name = ""
    print(f"Total offset ({name}): {total_offset}")

def evaluate_correct_solutions_on_training_set(plane_creator, dir_name, ext, filenames, calc_funcs):
    for filename, formula in zip(filenames, calc_funcs):
        path = dir_name + filename + ext
        ellipses = plane_creator.import_processed_dataset(path)
        dataset = [x.center for x in ellipses]
        evaluate_function_error(dataset, formula, name=filename)

if __name__ == '__main__':
    dir_name = './datasets/Feynman_with_units/processed_datasets/'
    ext = "-cut-10000-100-150"
    plane_creator = MultiDimEllipseCreator()
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

    evaluate_correct_solutions_on_training_set(plane_creator, dir_name, ext, filenames, calc_funcs)