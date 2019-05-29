# whenever you encounter a .net file, search for file with same name in done_results.
# open that file.
# open the tmp.out.critical_path.out file in the same subdir as the .net file.
# search for number of occurences of ble.out
# write down both
import os

all_files = "/home/ramanath/all_files/ref_zips/"

write_file = "/home/ramanath/Desktop/varun/comparing_benchmarks.txt"
open_write_file = open(write_file, "w+")
fname = []
for root,d_names,f_names in os.walk(all_files):
    for f in f_names:
        fname.append(os.path.join(root,f))
        print(fname[-1])
        # open_file.writelines(fname[-1] + " is in " + os.path.dirname(fname[-1]))
        # open_file.writelines("\n")
        filename = os.path.basename(fname[-1])
        if filename.find(".") != -1:
            filename_array = filename.split(".")
            # print(filename_array)
            blif_filename = filename_array[0]+".blif"
            complete_blif_filename = os.path.join(os.path.dirname(fname[-1]),blif_filename)
            blif_exists = os.path.exists(os.path.join(os.path.dirname(fname[-1]),blif_filename))
            # print(net_filename)
            # print(net_exists)
            # print(place_filename)
            # print(place_exists)
            if blif_exists:
                print(str(blif_filename)+" EXISTS")
                while True: # going through all the files that were done
                    print("Loop 0")
                    print("Searching for "+str(filename_array[0]))
                    done_file = open("/home/ramanath/all_files/done_results.txt", "r")
                    new_line = done_file.readline()
                    got_same_file = new_line.find(str(filename_array[0]))
                    print(got_same_file)
                    if got_same_file>-1:
                        results_file = open(new_line.rstrip("\n"),"r")
                        critical_path_file = os.path.join(os.path.dirname(fname[-1]),"tmp.out.critical_path.out")
                        counting_ble_out_file = open(critical_path_file,"r")
                        ble_outs = 0
                        while True:
                            print("Loop 1")
                            new_line_ble = counting_ble_out_file.readline()
                            new_line_ble_array = new_line_ble.split()
                            if len(new_line_ble)<=0: break
                            elif new_line_ble!="\n" and new_line_ble_array[0] == "Pin:" and new_line_ble_array[1][:len("ble.out")] == "ble.out":
                                ble_outs += 1
                        while True:
                            print("Loop 2")
                            new_line_result = results_file.readline()
                            if len(new_line_result)<=0: break
                            if new_line_result.find("longest path has length") == 0:
                                open_write_file.writelines(new_line + " \n")
                                open_write_file.writelines(critical_path_file + " \n")
                                open_write_file.writelines("reference is " + str(ble_outs) + " \n")
                                open_write_file.writelines("we have " + str(new_line_result.split()[6]) + " \n")
                                open_write_file.writelines("######\n")
                        results_file.close()
                        counting_ble_out_file.close()

                    if len(new_line)<=0:
                        break
                done_file.close()
open_write_file.close()