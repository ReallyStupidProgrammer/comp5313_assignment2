import urllib
import urllib.request
import networkx as nx
import numpy as np

def test_graph():
    g = nx.DiGraph()
    nodes = [
        "a",
        "b",
        "c",
        "d"
    ]
    edges = [
        ("a", "b", np.float64(1)),
        ("c", "d", np.float64(1)),
        ("a", "c", np.float64(1)),
        ("d", "b", np.float64(1)),
        ("d", "a", np.float64(1)),
        # # ("b", "c", np.float64(1)),
        # ("a", "a", np.float64(1)),
        # ("b", "b", np.float64(1)),
        # ("c", "c", np.float64(1)),
        # ("d", "d", np.float64(1)),
    ]
    g.add_nodes_from(nodes)
    g.add_weighted_edges_from(edges)
    return g

def amazon():
    # Read file from the dataset
    filename = "D:\\USYD\\Year2021Sem1\\INFO5313\\assignment2\\data\\amazon-meta.txt\\amazon-meta.txt"
    info = []
    with open(filename, "r") as my_file:
        count = -1
        for line in my_file.readlines():
            if line.startswith("Id"):
                info.append({})
                count += 1
            elif line.startswith("ASIN"):
                info[count]["ASIN"] = line.strip().split(" ")[1]
            elif line.startswith("  title"):
                info[count]["name"] = line.strip().split(": ")[1]
            elif line.startswith("  similar"):
                info[count]["similar"] = line.strip().split(": ")[1].split("  ")
            else:
                continue
    
    #create a transfer dictionary and create nodes
    asin_to_name = {}
    for product in info:
        if not "name" in product:
            continue
        asin_to_name[product["ASIN"]] = product["name"]

    #build the graph
    g = nx.DiGraph()
    g.add_nodes_from(list(asin_to_name.values()))

    for product in info:
        if not "similar" in product or not "ASIN" in product:
            continue
        current = product["ASIN"]
        for asin in product["similar"]:
            if not asin in asin_to_name:
                continue
            g.add_edge(asin_to_name[current], asin_to_name[asin], weight=1)
    
    g.to_directed()
    return g

def read_file_same_format(filename):
    g = nx.DiGraph()
    with open(filename, "r") as my_file:
        for _ in range(4):
            my_file.readline()
        temp = my_file.readline()
        while temp:
            x, y = temp.strip().split("\t")
            g.add_edge(x, y, weight=1)
            temp = my_file.readline()

    return g

def friendster():
    filename = "D:\\USYD\\Year2021Sem1\\INFO5313\\assignment2\\data\\com-friendster.ungraph.txt\\com-friendster.ungraph.txt"
    with open(filename, "r") as my_file:
        for _ in range(4):
            print(my_file.readline())

def youtube():
    filename = "D:\\USYD\\Year2021Sem1\\INFO5313\\assignment2\\data\\com-youtube.ungraph.txt\\com-youtube.ungraph.txt"
    return read_file_same_format(filename)

def wiki():
    filename = "D:\\USYD\\Year2021Sem1\\INFO5313\\assignment2\\data\\\wiki-Vote.txt\\\wiki-Vote.txt"
    return read_file_same_format(filename)

def import_graph(dataset):
    if dataset == "amazon":
        g = amazon()
    elif dataset == "friendster":
        g = friendster()
    elif dataset == "youtube":
        g = youtube()
    elif dataset == "wiki":
        g = wiki()
    elif dataset == "test":
        g = test_graph()
    else:
        g = None

    return g