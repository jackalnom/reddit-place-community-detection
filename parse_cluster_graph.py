import pickle
import igraph as ig

file = "D:/cluster_graphs-from-links-CPM.pz"
g1 = ig.Graph.Read_Picklez(file)
#g1 = ig.Graph.Read_GraphMLz(file)
print(g1.vs[0])
