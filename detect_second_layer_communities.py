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
file = open("D:/CPM_no_adjacency_000007.pz",'rb')
g = ig.Graph.Read_Picklez(file)
file.close()
logging.info("read dict")

logging.info("partitioning")
#part = g.community_leiden(objective_function='CPM', resolution_parameter=0.0001)
part = la.find_partition(g, la.CPMVertexPartition, resolution_parameter = 0.06, n_iterations=2, weights="size") # try 3?
#part = la.find_partition(g, la.RBConfigurationVertexPartition, resolution_parameter = 0.05)
#part = la.find_partition(g, la.ModularityVertexPartition, n_iterations=10)

g = None

ig.plot(part)

# logging.info("partitioned")
# cluster_graph = part.cluster_graph(
#     combine_vertices={
#         "size": "sum",
#     },
#     combine_edges={
#         "size": "sum",
#     },
# )
#
# cluster_graph.write_picklez("D:/CPM_no_adjacency_000007_layer_up.pz")
# cluster_graph = None
#
# logging.info("wrote overall cluster graph")
# directory = "D:/communities_CPM_no_adjacency_00001"
