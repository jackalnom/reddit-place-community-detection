import leidenalg
import igraph as ig
from collections import defaultdict
import numpy as np
import os
import math
from pathlib import Path
from contextlib import redirect_stdout
import sys
import logging

date = 'Test_Cluster'
dir = "D:/to_union/"
uniong = None

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

files = Path(dir).glob('*.pz')
for full_file in files:
    logging.info("reading " + str(full_file))
    g1 = ig.Graph.Read_Picklez(str(full_file))
    logging.info("read " + str(full_file))

    if uniong is None:
        uniong = g1
    else:
        logging.info("beginning union")
        f = open("logfile.txt", 'w')
        with redirect_stdout(f):
            uniong = ig.union([uniong, g1], byname=True)
        logging.info("done unioning")

    g1 = None

    if len(uniong.edge_attributes()) > 1:
        logging.info("rebuilding weight")
        for e in uniong.es():
            weight1 = (e["weight_1"] or 0)
            weight2 = (e["weight_2"] or 0)
            e["weight"] = weight1 + weight2
            #print("w1 " + str(weight1) + " w2 " + str(weight2) + " wt " + str(e["weight"]))
        logging.info("deleting extraneous weights")
        del uniong.es()["weight_1"]
        del uniong.es()["weight_2"]

    logging.info("merged " + str(full_file))

logging.info("writing to disk")
uniong.write_picklez("D:/for 02 and 03.pz")
logging.info("finished writing")
#
# uniong.vs["users"] = 1
# print("partitioning")
# part = uniong.community_leiden(objective_function='modularity', weights="weight")
# print("partitioned")
# cluster_graph = part.cluster_graph(
#     combine_vertices={
#         "users": "sum",
#     },
#     combine_edges={
#         "weight": "sum",
#     },
# )
#
# to_delete_ids = [v.index for v in cluster_graph.vs if v.index >= 25]
# cluster_graph.delete_vertices(to_delete_ids)
#
# cluster_graph.write_graphml("D:/user_cluster_graph.graphml")
#
# directory = "D:/communities"
# os.makedirs(directory, exist_ok=True)
# for i in range(25):
#     if i >= len(part.subgraphs()):
#         break
#
#     g1 = part.subgraphs()[i]
#
#     print("writing cluster - " + str(i))
#     stripped_list = g1.vs()["name"]
#     np.savetxt(directory + "/cluster " + str(i) + ".txt", stripped_list, fmt="%s")