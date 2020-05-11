from os import walk, path
import random
from ellipse_plane import MultiDimEllipse, MultiDimEllipseCreator
from linear_plane import MultiLinearCovariatePlane, MultiLinearCovariatePlaneCreator, \
    MultiLinearBasicPlane, MultiLinearBasicPlaneCreator
import numpy as np

class DataSetStats:
    def __init__(self, no_samples, no_vars, mins, maxs, avgs, stdevs):
        self.no_samples = no_samples
        self.no_vars = no_vars
        self.mins = mins
        self.maxs = maxs
        self.stdevs = stdevs
        self.avgs = avgs

    def __repr__(self):
        s1 = "#Samples: {}".format(self.no_samples)
        s2 = "#Vars: {}".format(self.no_vars)
        s3 = "Mins: {}".format(str(self.mins))
        s4 = "Maxs: {}".format(str(self.maxs))
        s5 = "Avgs: {}".format(str(self.avgs))
        s6 = "Stds: {}".format(str(self.stdevs))

        return "\n".join([s1, s2, s3, s4, s5, s6])

class DataSet:
    def __init__(self, data=None):
        self.data = data
        self.initialized = False

    def initialize(self):
        no_samples = len(self.data)
        no_vars = len(self.data[0])
        mins = []
        maxs = []
        avgs = []
        stdevs = []

        for i in range(no_vars):
            var_values = [x[i] for x in self.data]
            mins.append(min(var_values))
            maxs.append(max(var_values))
            avgs.append(np.average(var_values))
            stdevs.append(np.std(var_values))

        self.stats = DataSetStats(no_samples, no_vars, mins, maxs, avgs, stdevs)

    def get_no_samples(self):
        return len(self.data)

    def get_no_vars(self):
        return len(self.data[0])

    def get_stats(self):
        if not self.initialized:
            self.initialize()
        return self.stats

    def write_dataset(self, filename, no_points=None):
        if no_points is None:
            cut_dataset = self.data
        else:
            cut_dataset = self.data[:no_points]

        with open(filename, 'w') as f:
            for point in cut_dataset:
                point_line = " ".join([str(x) for x in point])
                f.write(point_line + "\n")

    @staticmethod
    def import_dataset(filename):
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()

        sample_size = len(lines)
        data = []
        for i in range(sample_size):
            sample_str = lines[i]
            data.append([float(x) for x in sample_str.split()])

        return DataSet(data)

    @staticmethod
    def cut_dataset(src, dest, no_samples):
        dataset = DataSet.import_dataset(src)
        random.shuffle(dataset.data)
        dataset.write_dataset(dest, no_samples)

    @staticmethod
    def cut_multiple_datasets(dir_name, dest_dir_name, no_samples):
        for (dirpath, dirnames, filenames) in walk(dir_name):
            for i, file in enumerate(filenames):
                src_filename = dir_name + "/" + file
                cut_filename = dest_dir_name + "/" + file + "-cut-{}".format(no_samples)
                cut_filename = cut_filename.replace("-cut", "")

                if path.exists(cut_filename):
                    print("Path exists: {}".format(cut_filename))
                else:
                    DataSet.cut_dataset(src_filename, cut_filename, no_samples)
                    print("{}/{} Written dataset: {}".format(i+1, len(filenames), cut_filename))

class DataPreprocessor:
    @staticmethod
    def get_planes_for_dataset(plane_creator, dataset, low, high):
        points = dataset.data
        _, planes = plane_creator.create_planes_for_dataset(points=points, low_no_neighbors=low, high_no_neighbors=high, verbose=False)

        return planes

    @staticmethod
    def preprocess_dataset(plane_creator, src_path, low, high, dest_path):
        dataset = DataSet.import_dataset(src_path)
        _, planes = plane_creator.create_planes_for_dataset(dataset.data, low, high)
        plane_creator.write_plane(planes, dest_path)

    @staticmethod
    def preprocess_datasets_in_directory(plane_creator, src_path, low, high, dest_path):
        for (dirpath, dirnames, filenames) in walk(src_path):
            for i, file in enumerate(filenames):
                src_filename = dirpath + "/" + file
                dest_filename = "{}/{}-{}-{}".format(dest_path, file, low, high)
                DataPreprocessor.preprocess_dataset(plane_creator, src_filename, low, high, dest_filename)
                print("Preprocessed {}/{}: {}".format(i+1, len(filenames), dest_filename))