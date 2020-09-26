from os import walk
import lxml.etree
import numpy as np

results = {}

def parse_log_file(filename, destination):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    for line in reversed(lines):
        stripped_line = line.strip()
        if stripped_line.startswith("<FitnessMin"):
            fitness = lxml.etree.fromstring(stripped_line).xpath('@value')[0]
            filename_key = filename.replace("./", "").replace("/", "-").replace("-log_1.txt", "")
            dash_index = filename_key.rfind("-")
            filename_key = filename_key[:dash_index]
            if filename_key not in results:
                results[filename_key] = []
            results[filename_key].append(float(fitness))

def parse_results(source_dir, dest_dir):
    for (dirpath, dirnames, filenames) in walk(source_dir):
        for i, file in enumerate(filenames):
            if file == 'log_1.txt':
                parse_log_file(dirpath + "/" + file, dest_dir)

def write_trees(trees, filename):
    f = open(filename, 'w')
    sizes = ','.join([f"{x[0]}" for x in trees])
    fitnesses = ','.join([f"{int(x[1])}" for x in trees])
    f.write("\n".join([sizes, fitnesses]))
    f.close()

if __name__ == '__main__':
    source_dir = './logGEP20/GEP'
    dest_dir = './training_results_test.txt'

    parse_results(source_dir, dest_dir)
    pass
    #f = open(dest_dir, "w")
    #
    #for key in results:
    #    print(key)
    #    print(f"Average: {np.average(results[key])}, Std: {np.std(results[key])}")
    #    f.write(key + "\n")
    #    f.write(",".join(str(x) for x in results[key]) + "\n")
    #
    #f.close()