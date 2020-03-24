import sys

def cut(file_name, sample_size):
    file = open(file_name, 'r')

    lines = file.readlines()
    header = lines[0].split()
    if len(header) != 2:
        header = "{0} {1}".format(len(lines), len(lines[0].split()) - 1)
        lines.insert(0, header)
    else:
        sample_no = header[0]
        var_no = header[1]
        try:
            sample_no = int(sample_no)
        except IndexError:
            header = "{0} {1}".format(len(lines), len(lines[0].split()) - 1)
            lines.insert(0, header)

    lines = lines[:sample_size + 1]
    file.close()

    return lines[0], lines[1:]

def write_file(file_name, header, lines):
    file = open(file_name, 'w')

    file.write(header + "\n")

    for line in lines:
        file.write(line)

    file.close()

def get_new_header(sample_size, header):
    params = header.split()
    return "{0} {1}".format(sample_size, int(params[1]))

if __name__ == '__main__':
    src_file_name = sys.argv[1]
    dest_file_name = sys.argv[2]
    sample_size = int(sys.argv[3])

    header, cut_file = cut(src_file_name, sample_size)
    newHeader = get_new_header(sample_size, header)

    write_file(dest_file_name, newHeader, cut_file)


