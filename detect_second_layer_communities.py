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
import json
from collections import defaultdict

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
file = open("D:/CPM_no_adjacency_0000065.pz",'rb')
g = ig.Graph.Read_Picklez(file)
file.close()
logging.info("read dict")

g.vs()[0]["label"] = "France"
g.vs()[1]["label"] = "Latin America"
g.vs()[2]["label"] = "Turkey"
g.vs()[3]["label"] = "xQc Streamer"
g.vs()[4]["label"] = "Russian Streamers"
g.vs()[5]["label"] = "USA"
g.vs()[6]["label"] = "Germany"
g.vs()[7]["label"] = "LGBTQ+"
g.vs()[8]["label"] = "osu!"
g.vs()[9]["label"] = "Twitch Streamer"
g.vs()[10]["label"] = "Canada"
g.vs()[11]["label"] = "Poland"
g.vs()[12]["label"] = "Netherlands"
g.vs()[13]["label"] = "Gamestop"
g.vs()[14]["label"] = "India"
g.vs()[15]["label"] = "UK"
g.vs()[16]["label"] = "Italy"
g.vs()[17]["label"] = "Destiny Streamer"
g.vs()[18]["label"] = "Palestine/Israel"
g.vs()[19]["label"] = "Romania/Hungary"
g.vs()[20]["label"] = "One Piece"
g.vs()[21]["label"] = "Argentina"
g.vs()[22]["label"] = "Runescape"
g.vs()[23]["label"] = "Ludwig Streamer"
g.vs()[24]["label"] = "My Little Pony"
g.vs()[25]["label"] = "Rappers"
g.vs()[26]["label"] = "Twitch Streamers"
g.vs()[27]["label"] = "Hollow Knight/Elden Ring"
g.vs()[28]["label"] = "Portugal"
g.vs()[29]["label"] = "Columbia"
g.vs()[30]["label"] = "Fuck Cars"
g.vs()[31]["label"] = "Blue Square"
g.vs()[32]["label"] = "Ukraine"
g.vs()[33]["label"] = "Quebec"
g.vs()[34]["label"] = "Star Wars"
g.vs()[35]["label"] = "Minecraft Streamers"
g.vs()[36]["label"] = "Czechia/Slovakia"
g.vs()[37]["label"] = "Lithuania"
g.vs()[38]["label"] = "Sweden"
g.vs()[39]["label"] = "Serbia"
g.vs()[40]["label"] = "Belgium"
g.vs()[41]["label"] = "Hong Kong"
g.vs()[42]["label"] = "Spain"
g.vs()[43]["label"] = "Brazil"
g.vs()[44]["label"] = "Grand Theft Auto"
g.vs()[45]["label"] = "Chile"
g.vs()[46]["label"] = "Denmark"
g.vs()[47]["label"] = "Furry/NATO"
g.vs()[48]["label"] = "Twitch Streamer"
g.vs()[49]["label"] = "Formula 1"

logging.info("partitioning")
to_delete_ids = [v.index for v in g.vs if v.index >= 200]
g.delete_vertices(to_delete_ids)


part = g.community_multilevel(weights="weight", return_levels=True)

nodes = {}
index = 0

communities = defaultdict(list)
for index, community in enumerate(part[0].membership):
    n = g.vs()[index]
    leaf = {"name": n["label"], "value": n["weight"]}
    communities[community].append(leaf)

second_level_community_indexes = defaultdict(set)
for index, community in enumerate(part[1].membership):
    second_level_community_indexes[community].add(part[0].membership[index])

second_level_communities = []
for community in second_level_community_indexes.values():
    community_list = []
    for ind_community in community:
        community_list.append({"name": "", "children": communities[ind_community]})
    second_level_communities.append({"name": "", "children": community_list})
#
root_node = {"name": "", "children": second_level_communities}

# for dendrogram to json
# for merge in part.merges:
#     merge_node_1 = nodes[merge[0]]
#     merge_node_2 = nodes[merge[1]]
#
#     new_node = {"name": "", "children": [merge_node_1, merge_node_2]}
#     nodes.append(new_node)

with open('D:/json_data_2.json', 'w') as outfile:
    json.dump(root_node, outfile)
