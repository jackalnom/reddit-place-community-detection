import igraph as ig
from collections import defaultdict
import numpy as np
import os
import math
from pathlib import Path
from contextlib import redirect_stdout
import sys
import logging
import pickle
import leidenalg as la

def strip_dates(e):
    splits = e.split('-')

    if len(splits) > 1:
        return_str = splits[len(splits)-1]
    else:
        return_str = e

    #if len(return_str.split(',')) != 3:
    #    logging.error("Wrong number of fields: (" + e + ") split to: " + return_str)

    return return_str

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

logging.info("reading dict")
file = open("D:/canada.pickle",'rb')
links = pickle.load(file)
file.close()
logging.info("read dict")

logging.info("building graph")
g = ig.Graph.TupleList([(k, v) for k, vs in links.items() for v in vs])
logging.info("built graph")

g.vs["weight"] = 1
g.es["weight"] = 1

logging.info("partitioning")
#part = g.community_leiden(objective_function='CPM', resolution_parameter=0.0001)
part = la.find_partition(g, la.CPMVertexPartition, resolution_parameter = 0.000004, n_iterations=10) # try 3?
#part = la.find_partition(g, la.RBConfigurationVertexPartition, resolution_parameter = 0.05)
#part = la.find_partition(g, la.ModularityVertexPartition, n_iterations=50)

g = None

logging.info("partitioned")
# cluster_graph = part.cluster_graph(
#     combine_vertices={
#         "weight": "sum",
#     },
#     combine_edges={
#         "weight": "sum",
#     },
# )

# cluster_graph.write_picklez("D:/CPM_no_adjacency_0000065.pz")
# cluster_graph = None

# logging.info("wrote overall cluster graph")
directory = "D:/canada_communities_CPM"
os.makedirs(directory, exist_ok=True)
for i in range(100):
    if i >= len(part):
        break

    logging.info("parsing subgraph " + str(i))
    g1 = part.subgraph(i)

    logging.info("writing cluster - " + str(i))
    stripped_user_list = [ele for ele in g1.vs()["name"] if isinstance(ele, str)]
    np.savetxt(directory + "/cluster users " + str(i) + ".txt", stripped_user_list, fmt="%s")

    logging.info("wrote subgraph " + str(i))