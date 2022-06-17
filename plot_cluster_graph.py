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

g = ig.Graph.Read_Picklez("D:/CPM_no_adjacency_0000065.pz")

to_delete_ids = [v.index for v in g.vs if v.index >= 30]
g.delete_vertices(to_delete_ids)

min_edge = 10000
max_edge = 0

for e in g.es():
    e["edge_width"] = e["weight"] / (e.source_vertex["weight"] * e.target_vertex["weight"])
    min_edge = min(min_edge, e["edge_width"])
    max_edge = max(max_edge, e["edge_width"])

for e in g.es():
    e["edge_width"] = ((e["edge_width"] - min_edge) / (max_edge-min_edge))*7

to_delete_ids = [e.index for e in g.es if e["edge_width"] < 1]
g.delete_edges(to_delete_ids)

min_vertex = 100000000
max_vertex = 0

for v in g.vs():
    v["label"] = str(v.index)
    v["vertex_size"] = math.log(v["weight"])
    min_vertex = min(min_vertex, v["vertex_size"])
    max_vertex = max(max_vertex, v["vertex_size"])

for v in g.vs():
    v["vertex_size"] = ((v["vertex_size"] - min_vertex) / (max_vertex-min_vertex))*100
    logging.info(v["vertex_size"])

layout = g.layout_fruchterman_reingold(weights="weight")

g.vs[0]["label"] = "France"
visual_style = {}
visual_style["vertex_size"] = g.vs()["vertex_size"]
#visual_style["vertex_color"] = [color_dict[gender] for gender in g.vs["gender"]]
visual_style["edge_width"] = g.es()["edge_width"]
visual_style["layout"] = layout
visual_style["bbox"] = (2000, 2000)
visual_style["margin"] = 20
ig.plot(g, **visual_style)

#
# logging.info("partitioning")
# #part = g.community_leiden(objective_function='CPM', resolution_parameter=0.0001)
# part = la.find_partition(g, la.CPMVertexPartition, resolution_parameter = 0.0000065, n_iterations=50) # try 3?
# #part = la.find_partition(g, la.RBConfigurationVertexPartition, resolution_parameter = 0.05)
# #part = la.find_partition(g, la.ModularityVertexPartition, n_iterations=10)
#
# g = None
#
# logging.info("partitioned")
# cluster_graph = part.cluster_graph(
#     combine_vertices={
#         "weight": "sum",
#     },
#     combine_edges={
#         "weight": "sum",
#     },
# )
#
# cluster_graph.write_picklez("D:/CPM_no_adjacency_0000065.pz")
# cluster_graph = None
#
# logging.info("wrote overall cluster graph")
# directory = "D:/communities_CPM_no_adjacency_0000065"
# os.makedirs(directory, exist_ok=True)
# for i in range(100):
#     if i >= len(part):
#         break
#
#     logging.info("parsing subgraph " + str(i))
#     g1 = part.subgraph(i)
#
#     logging.info("writing cluster - " + str(i))
#     stripped_pixel_list = [ele for ele in g1.vs()["name"] if "==" not in ele]
#     stripped_pixel_list = list(map(lambda e: strip_dates(e), stripped_pixel_list))
#     np.savetxt(directory + "/cluster pixels " + str(i) + ".txt", stripped_pixel_list, fmt="%s")
#
#     stripped_user_list = [ele for ele in g1.vs()["name"] if "==" in ele]
#     np.savetxt(directory + "/cluster users " + str(i) + ".txt", stripped_user_list, fmt="%s")
#
#     logging.info("wrote subgraph " + str(i))