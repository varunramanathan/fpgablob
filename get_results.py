import parser_server
import concurrent.futures


def run_parser(input_line):
    lines_array = input_line.split(" ")
    parser_server.blob_parser(lines_array[0].rstrip("\n"), lines_array[1].rstrip("\n"), lines_array[2].rstrip("\n"))


with concurrent.futures.ProcessPoolExecutor() as executor:
    filename = '/home/ramanath/parameters.txt'
    open_file = open(filename, "r")
    lines = list()
    while True:
        new_line = open_file.readline()
        if len(new_line) <= 0:
            break
        lines.append(new_line)
    open_file.close()
    for line,ret in zip(lines,executor.map(run_parser,lines)):
        pass