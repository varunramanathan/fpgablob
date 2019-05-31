import random

list_of_files = open("/home/ramanath/all_files/files_to_copy.txt","r")
new_list_of_files = open("/home/ramanath/all_files/all_files_list","w+")
parameters_dict = dict()
set_of_arcs = dict()
# count_of_benchmarks = dict()
arc_num = ''
seed_num = ''
# first collect the seed for each architecture
while True:
    line = list_of_files.readline().rstrip("\n")
    line_array = line.split("/")
    if len(line) <= 0:
        break
    if line_array[6] in set_of_arcs:
        set_of_arcs[line_array[6]].add(line_array[7])
    else:
        set_of_arcs[line_array[6]] = set()
        set_of_arcs[line_array[6]].add(line_array[7])
list_of_files.close()
list_of_files = open("/home/ramanath/all_files/files_to_copy.txt","r")
# now, select the seed for each architecture randomly
seed_for_arch = dict()
while True:
    line = list_of_files.readline().rstrip("\n")
    line_array = line.split("/")
    if len(line) <= 0:
        break
    if line_array[6] not in seed_for_arch:
        random.seed = 42
        seed_for_arch[line_array[6]] = random.choice(tuple(set_of_arcs[line_array[6]]))
list_of_files.close()
list_of_files = open("/home/ramanath/all_files/files_to_copy.txt","r")
benchmarks_for_arcs = dict()
while True:
    line = list_of_files.readline().rstrip("\n")
    line_array = line.split("/")
    except_extension = line.split(".")
    if len(line) <= 0:
        break
    if seed_for_arch[line_array[6]] == line_array[7]:
        if except_extension[0] not in parameters_dict:
            parameters_dict[except_extension[0]] = [line_array[6]+"_"+line_array[7]+"_"+line_array[8].split(".")[0]+".results", '', '']
        if except_extension[1] == "net":
            parameters_dict[except_extension[0]][1] = line
        else:
            parameters_dict[except_extension[0]][2] = line
        # new_list_of_files.write(line+"\n")
list_of_files.close()
for filename in parameters_dict:
    new_list_of_files.write(parameters_dict[filename][0]+" "+parameters_dict[filename][1]+" "+parameters_dict[filename][2]+"\n")
new_list_of_files.close()