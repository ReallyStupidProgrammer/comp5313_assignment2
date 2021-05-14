import sys
import networkx as nx

from src.import_graph import import_graph

if __name__ == "__main__":
    dataset = sys.argv[1]
    g = import_graph(dataset)
