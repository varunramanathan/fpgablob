import os

all_files = "/home/ramanath/all_files/"
write_file = "/home/ramanath/parameters.txt"
open_write_file = open(write_file, "w+")
done = dict()
fname = []
for root,d_names,f_names in os.walk(all_files):
    for f in f_names:
        fname.append(os.path.join(root,f))
        filename = os.path.basename(fname[-1])
        if filename.find(".") != -1:
            filename_array = filename.split(".")
            # print(filename_array)
            net_filename = filename_array[0]+".net"
            complete_net_filename = os.path.join(os.path.dirname(fname[-1]),net_filename)
            place_filename = filename_array[0]+".place"
            complete_place_filename = os.path.join(os.path.dirname(fname[-1]),place_filename)
            net_exists = os.path.exists(os.path.join(os.path.dirname(fname[-1]),net_filename))
            place_exists = os.path.exists(os.path.join(os.path.dirname(fname[-1]),place_filename))
            # print(net_filename)
            # print(net_exists)
            # print(place_filename)
            # print(place_exists)
            complete_net_filename_array = complete_net_filename.split("/")
            if net_exists and place_exists:
                open_write_file.write(complete_net_filename_array[6]+"_"+complete_net_filename_array[7]+"_"+complete_net_filename_array[8].split(".")[0]+".results "+str(complete_net_filename)+" "+str(complete_place_filename)+"\n")
    # f.writelines("\n")
    # f.writelines(d_names)
    # f.writelines("\n")
    # f.writelines(f_names)
    # f.writelines("\n")
open_write_file.close()
