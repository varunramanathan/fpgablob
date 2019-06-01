# whenever you encounter a .net file, search for file with same name in done_results.
# open that file.
# open the tmp.out.critical_path.out file in the same subdir as the .net file.
# search for number of occurences of ble.out
# write down both
import os

import parser_server

done_benchmark_analysis = dict()
benchmarks = "/home/ramanath/ref_zips/"
benchmark_keywords = set()
for folder in os.listdir(benchmarks):
    print("Current file/folder name: "+folder)
    if folder.find("zip") > -1 or folder.find("result")>-1 or folder.find("ref_arch_complete")==-1:
        print("proceeding to next")
        continue
    our_keyword = folder[len("ref_arch_complete_"):]
    print(our_keyword)
    benchmark_keywords.add(our_keyword)
    comparison_critical_path_filepath = benchmarks + "ref_arch_complete_" + our_keyword + "/tmp.out.critical_path.out"
    comparison_net_filepath = benchmarks + "ref_arch_complete_" + our_keyword + "/" + our_keyword + ".net"
    comparison_place_filepath = benchmarks + "ref_arch_complete_" + our_keyword + "/" + our_keyword + ".place"
    if not os.path.exists(benchmarks+"ref_" + our_keyword + ".results") and len(our_keyword)>0:
        parser_server.blob_parser(benchmarks+"ref_" + our_keyword + ".results", comparison_net_filepath, comparison_place_filepath)
# created all the reference results files
open_output_file = open(benchmarks+"output.txt","w+")
results = "/home/ramanath/results/"
for filename in os.listdir(results):
    our_keyword = ''
    for keyword in benchmark_keywords:
        if filename.find(keyword) != -1:
            our_keyword = keyword
            break
    ref_filename = benchmarks+"ref_"+our_keyword+".results"
    #read the result file
    current_result_file = open(results+filename,'r')
    current_ref_file = open(ref_filename,'r')
    ref_critical_path_file = open(benchmarks + "ref_arch_complete_" + our_keyword + "/tmp.out.critical_path.out",'r')
    # counting BLEs in critical path file:
    ble_outs = 0
    while True:
        # print("Loop 1")
        new_line_ble = ref_critical_path_file.readline()
        if len(new_line_ble) <= 0:
            break
        new_line_ble_array = new_line_ble.split()
        if new_line_ble != "\n" and new_line_ble_array[0] == "Pin:" and new_line_ble_array[1][:len("ble.out")] == "ble.out":
            ble_outs += 1
    ref_critical_path_file.close()
    longest_path_current = 0
    longest_path_ref_nodes = 0
    longest_path_current_nodes = 0
    longest_path_ref = 0

    while True:
        new_line_result = current_ref_file.readline()
        # print("Loop 2 =>       "+new_line_result)
        if len(new_line_result) <= 0:
            break
        if new_line_result.find("longest path has length") == 0:
            split_array = new_line_result.split()
            longest_path_ref = split_array[4]
            longest_path_ref_nodes = split_array[6]
            break
    while True:
        new_line_result = current_result_file.readline()
        # print("Loop 2 =>       "+new_line_result)
        if len(new_line_result) <= 0:
            break
        if new_line_result.find("longest path has length") == 0:
            split_array = new_line_result.split()
            longest_path_current = split_array[4]
            longest_path_current_nodes = split_array[6]
            break
    current_result_file.close()
    current_ref_file.close()
    open_output_file.write("------------------------------------------\n")
    open_output_file.write("Filename = "+filename+"\n")
    open_output_file.write("Longest path length = "+longest_path_current+"\n")
    open_output_file.write("Number of nodes on longest path = "+longest_path_current_nodes+"\n")
    open_output_file.write("Longest path in reference = "+longest_path_ref+"\n")
    open_output_file.write("Number of nodes in longest path in reference = "+longest_path_ref_nodes+"\n")
    open_output_file.write("ble.outs in reference critical path: "+str(ble_outs)+"\n")
    open_output_file.write("Node comparison: "+str(longest_path_current_nodes < longest_path_ref_nodes)+"\n")
    open_output_file.write("Length comparison: "+str(longest_path_current < longest_path_ref_nodes)+"\n")
open_output_file.close()