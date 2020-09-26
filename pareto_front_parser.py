def parse_pareto_front(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    trees = []

    i = 0
    while i < len(lines):
        tree_params = tuple([float(x) for x in lines[i].split(sep=';')])
        trees.append(tree_params)
        i += 2

    return trees

def write_trees(trees, filename):
    f = open(filename, 'w')
    sizes = ','.join([f"{x[0]}" for x in trees])
    fitnesses = ','.join([f"{int(x[1])}" for x in trees])
    f.write("\n".join([sizes, fitnesses]))
    f.close()

if __name__ == '__main__':
    for i in range(5, 11):
        source_pareto_front = f'./logANAL2/{i}/IEUND/D_TESTELLIPSE_100_150/100_0.900000_TOUR/paretoFront.txt'
        dest_dataset_file = f'./graphs_r/GP_pareto_{i}'

        trees = parse_pareto_front(source_pareto_front)
        write_trees(trees, dest_dataset_file)