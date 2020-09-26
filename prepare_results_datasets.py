import os

def create_data(results):
    f = open(results, 'r')
    lines = f.readlines()
    f.close()

    data_list = []

    i = 0
    while i < len(lines):
        title = lines[i].replace("\n", "")
        data = lines[i+1]
        data_list.append((title, data))
        i += 2

    return data_list

if __name__ == '__main__':
    dir_name = "./data_r_test"
    results_filename = "./training_results_test.txt"

    data_list = create_data(results_filename)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    for data in data_list:
        data_title = data[0]
        data_results = data[1]
        filename = "/".join([dir_name, data_title])
        f = open(filename, 'w')
        f.write(data_results + "\n")
        f.close()