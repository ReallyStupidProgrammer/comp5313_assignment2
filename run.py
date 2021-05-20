import sys
import time
import numpy as np
import networkx as nx

from src.import_graph import import_graph
from src.page_rank import *

def stdv(pagerank):
    temp = np.array(list(pagerank), dtype=np.float64)
    return np.std(temp, ddof=1)

def output(g, filename=".\\output", alpha=0.85):
    with open(filename, "w") as my_file:
        my_file.write("Dataset Description: \n")
        my_file.write("Number of Nodes: " + str(g.number_of_nodes()) + "\n")
        my_file.write("Number of Edges: " + str(g.number_of_edges()) + "\n")
        my_file.write("\n\n\n")

        my_file.write("NetworkX: \n")
        start = time.time()
        ans = networkx_page_rank(g, alpha)
        # print(ans)
        my_file.write("Max Value: " + str(max(ans.values())) + "\n")
        my_file.write("Min Value: " + str(min(ans.values())) + "\n")
        my_file.write("Standard Deviation: " + str(stdv(ans.values())) + "\n\n")
        my_file.write("TotalTime: " + str(time.time() - start) + "\n")

        my_file.write("\n\n\n")
        my_file.write("Mine: \n")
        start = time.time()
        ans, time1, time2 = my_page_rank_1(g, alpha, 1.0e-6)
        total_time = time.time() - start
        # print(ans)
        my_file.write("Max Value: " + str(max(ans.values())) + "\n")
        my_file.write("Min Value: " + str(min(ans.values())) + "\n")
        my_file.write("Standard Deviation: " + str(stdv(ans.values())) + "\n\n")
        my_file.write("Total Time: " + str(total_time) + "\n")
        my_file.write("Node to Number Time: " + str(time1) + "\n")
        my_file.write("Matrix Calculation Time: " + str(time2) + "\n")
        my_file.write("PageRank Calculation Time: " + str(total_time - time1 - time2) + "\n")

if __name__ == "__main__":
    g = import_graph(sys.argv[1])
    print("test")
    output(g, sys.argv[2], np.float64(sys.argv[3]))  