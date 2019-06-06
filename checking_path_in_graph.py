import sys

import networkx as nx

def main(graph, path_list):
    print(str(nx.is_simple_path(graph,path_list)))

if __name__=="__main__":
    main(sys.argv[1],sys.argv[2])