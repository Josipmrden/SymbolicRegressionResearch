from matplotlib import pyplot as plt
import sys
from preffix_to_infix_converter import get_inffix_formula

def parse_file(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()

    data = []
    for i in range(0, len(lines), 2):
        fitnessSize = lines[i].split()
        fitness = float(fitnessSize[0])
        size = int(fitnessSize[1])
        representation = lines[i+1]
        index = 14 + len(str(size))
        representation = representation[index:]
        representation = representation[:-9]
        data.append([fitness, size, representation])

    data.sort(key=lambda x: x[1])
    for d in data:
        d[0] = str(d[0])
        d[1] = str(d[1])
        d[2] = get_inffix_formula(d[2])


    return data


def write_data(data, dest_filename):
    file = open(dest_filename, 'w')
    lines = [' '.join(x) for x in data]
    lines = '\n'.join(lines)
    file.write(lines)
    file.close()

if __name__ == '__main__':
    filename = sys.argv[1]
    dest_filename = sys.argv[2]

    data = parse_file(filename)
    write_data(data, dest_filename)

    sizes = [int(x[1]) for x in data]
    fitnesses = [float(x[0]) for x in data]

    legend = [" ".join(x) for x in data]
    legend = "\n".join(legend)
    fig = plt.figure()
    ax1 = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax1.set_xlabel('Size')
    ax1.set_ylabel('Fitness')
    ax1.set_title('Pareto front')
    plt.plot(sizes, fitnesses)
    plt.show()