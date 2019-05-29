# Recursively go to each folder in /home/ramanath/all_files, and for each filename, use "." as delimiter to get the first word (say, X). Then,
# work on X.net and X.place, if they exist. Save the result in the same folder with the name X_result.txt
import os
import sys
import blob_parser

all_files = "/home/ramanath/all_files/"
write_file = "/home/ramanath/Desktop/varun/write_file.txt"
open_file = open(write_file, "w+")
done = dict()
fname = []
for root,d_names,f_names in os.walk(all_files):
    for f in f_names:
        sys.stdout = sys.__stdout__
        fname.append(os.path.join(root,f))
        print(fname[-1])
        # open_file.writelines(fname[-1] + " is in " + os.path.dirname(fname[-1]))
        # open_file.writelines("\n")
        filename = os.path.basename(fname[-1])
        if filename.find(".") != -1:
            filename_array = filename.split(".")
            print(filename_array)
            net_filename = filename_array[0]+".net"
            complete_net_filename = os.path.join(os.path.dirname(fname[-1]),net_filename)
            place_filename = filename_array[0]+".place"
            complete_place_filename = os.path.join(os.path.dirname(fname[-1]),place_filename)
            net_exists = os.path.exists(os.path.join(os.path.dirname(fname[-1]),net_filename))
            place_exists = os.path.exists(os.path.join(os.path.dirname(fname[-1]),place_filename))
            print(net_filename)
            print(net_exists)
            print(place_filename)
            print(place_exists)
            if filename_array[0] in done:
                if done[filename_array[0]] > 100:
                    continue
                done[filename_array[0]] = done[filename_array[0]]+1
            else:
                done[filename_array[0]] = 1
            if net_exists and place_exists:
                print("Yay",file=sys.__stdout__)
                result_file = open(os.path.join(os.path.dirname(fname[-1]),filename_array[0]+".results"),"w+")
                sys.stdout = result_file
                blob_parser.blob_parser(complete_net_filename,complete_place_filename)
                result_file.close()
    # f.writelines("\n")
    # f.writelines(d_names)
    # f.writelines("\n")
    # f.writelines(f_names)
    # f.writelines("\n")
open_file.close()
