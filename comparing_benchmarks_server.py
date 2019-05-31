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
    our_keyword = folder[len("ref_arch_complete_") + 1:]
    benchmark_keywords.add(our_keyword)
    comparison_critical_path_filepath = benchmarks + "ref_arch_complete_" + our_keyword + "/tmp.out.critical_path.out"
    comparison_net_filepath = benchmarks + "ref_arch_complete_" + our_keyword + "/" + our_keyword + ".net"
    comparison_place_filepath = benchmarks + "ref_arch_complete_" + our_keyword + "/" + our_keyword + ".place"
    parser_server.blob_parser("ref_" + our_keyword + ".results", comparison_net_filepath, comparison_place_filepath)
results = "/home/ramanath/results/"
for filename in os.listdir(results):
    our_keyword = ''
    for keyword in benchmark_keywords:
        if filename.find(keyword) != -1:
            our_keyword = keyword
            break



