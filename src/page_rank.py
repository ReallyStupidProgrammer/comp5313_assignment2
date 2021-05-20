import networkx as nx
import numpy as np
import time

#Implement by myself using matrix multiplication
#Use CSR format 
def cal_matrix(g, node_trans):
    for i in g.nodes():
        if (g.out_degree(i) == 0.0):
            g.add_edge(i, i, weight=np.float64(1))

    g = nx.stochastic_graph(g, weight="weight")
    n = g.number_of_nodes()
    m = g.number_of_edges()
    data = np.zeros(m, dtype=np.float64)
    row = np.zeros(m, dtype=np.int32)
    col = np.zeros(m, dtype=np.int32)
    count = 0
    node_idx = 0
    for i in g.nodes():
        for _, j, w in g.edges(i, data="weight"):
            data[count] = np.float64(w)
            col[count] = np.int32(node_trans[j])
            row[count] = np.int32(node_trans[i])
            count += 1
    # print(data)
    # print(row)
    # print(col)
    return data, row, col

def node_transfer(g):
    d = {}
    count = 0;
    node_list = []
    for i in g.nodes():
        d[i] = count
        count += 1
        node_list.append(i)
    return d, node_list

def my_page_rank(g, alpha, err):
    start = time.time()
    node_trans, node_list = node_transfer(g)
    node_list_time = time.time() - start

    start = time.time()
    w = cal_matrix(g, node_trans)
    cal_matrix_time = time.time() - start

    n = g.number_of_nodes()
    pagerank = np.zeros(n, dtype=np.float64)
    ans_pagerank = pagerank.copy()
    pre = np.array([np.float64(1 / n)] * n)
    p = np.array([np.float64(1 / n)] * n)
    alpha = np.float64(alpha)
    # dangling = [node_trans[i] for i in g.nodes() if g.out_degree(i) == 0.0]
    # pre_sum = np.float64(len(dangling) / n)
    while True:
        row_idx = 0
        for i in range(len(w[0])):            
            pagerank[w[2][i]] += pre[w[1][i]] * w[0][i]

        pagerank = pagerank * alpha + p * np.float64(1 - alpha)
        if sum(map(lambda x: abs(x[0] - x[1]), zip(pre, pagerank))) < err:
            break
        ans_pagerank += pagerank
        pre = pagerank.copy()
        print(pagerank)
        pagerank = np.zeros(n, dtype=np.float64)
        # for i in dangling:
        #     pagerank[i] = pre[i]

    
    ans = {}
    for i in range(n):
        ans[node_list[i]] = ans_pagerank[i]

    return ans, node_list_time, cal_matrix_time

def my_page_rank_1(g, alpha, err):
    start = time.time()
    node_trans, node_list = node_transfer(g)
    node_list_time = time.time() - start

    start = time.time()
    w = cal_matrix(g, node_trans)
    cal_matrix_time = time.time() - start
    n = g.number_of_nodes()
    pagerank = np.zeros(n)
    pre = np.array([np.float64(1.0 / n)] * n)
    ans = pre.copy()
    k = 100
    for _ in range(k):
        for i in range(len(w[0])):
            pagerank[w[2][i]] += pre[w[1][i]] * w[0][i]
            # print(pagerank)
        pagerank *= alpha
        ans += pagerank
        # print(pagerank)
        # print("test")
        # print(ans)
        diff = sum(map(lambda x: abs(x[0] - x[1]), zip(pre, pagerank)))
        if diff <= err:
            break
        
        pre = pagerank.copy()
        pagerank = np.zeros(n)
        # print(pagerank)
        # print(ans)

    ans_pagerank = ans * (1 - alpha)
    ans = {}
    for i in range(n):
        ans[node_list[i]] = ans_pagerank[i]
    return ans, node_list_time, cal_matrix_time

def my_page_rank_2(g, alpha):
    n = g.number_of_nodes()

        

#use the pagerank function in networkX
def networkx_page_rank(g, alpha=0.4):
    return nx.pagerank(g, alpha=alpha)

def igraph_page_rank(g):
    pass