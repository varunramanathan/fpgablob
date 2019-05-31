import os
import shutil

list_of_files = open("/home/ramanath/all_files/all_files_list","r")
home_dir = "/home/ramanath/all_files/all_files_copy/"
current_dir = "/home/ramanath/all_files/all_files_copy/"
os.chdir(home_dir)
while True:
    new_line = list_of_files.readline()
    if len(new_line)<=0:
        break
    new_line = new_line.rstrip("\n")
    new_line_array = new_line.split("/")
    for i in range(4,8):
        if os.path.exists("./"+new_line_array[i]):
            os.chdir("./"+new_line_array[i])
        else:
            os.mkdir("./"+new_line_array[i])
            os.chdir("./"+new_line_array[i])
    shutil.copy(new_line,os.curdir)
    os.chdir(home_dir)