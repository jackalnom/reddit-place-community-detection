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

def strip_dates(e):
    splits = e.split('-')
    if (splits[len] == 4):
        return splits[3]
    else:
        return e

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logging.info("reading dict")
file = open("D:/unioned_dict.pz",'rb')
links = pickle.load(file)
file.close()
logging.info("read dict")

logging.info("building graph")
g = ig.Graph.TupleList([(k, v) for k, vs in links.items() for v in vs])
logging.info("built graph")

g.vs["size"] = 1
g.es["size"] = 1

logging.info("partitioning")
part = g.community_leiden(objective_function='CPM', resolution_parameter=0.001)
logging.info("partitioned")
cluster_graph = part.cluster_graph(
    combine_vertices={
        "size": "sum",
    },
    combine_edges={
        "size": "sum",
    },
)

cluster_graph.write_picklez("D:/CPM_resolution_001.graphml")
logging.info("wrote overall cluster graph")
directory = "D:/communities_CPM"
os.makedirs(directory, exist_ok=True)
for i in range(100):
    if i >= len(part.subgraphs()):
        break

    logging.info("parsing subgraph " + str(i))
    g1 = part.subgraph(i)

    logging.info("writing cluster - " + str(i))
    stripped_pixel_list = [ele for ele in g1.vs()["name"] if "==" not in ele]
    stripped_pixel_list = list(map(lambda e: strip_dates(e), stripped_pixel_list))
    np.savetxt(directory + "/cluster pixels " + str(i) + ".txt", stripped_pixel_list, fmt="%s")
    logging.info("wrote subgraph " + str(i))