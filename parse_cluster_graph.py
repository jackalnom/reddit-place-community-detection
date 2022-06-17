import pickle
import igraph as ig

file = "D:/CPM_no_adjacency_0000065.pz"
g1 = ig.Graph.Read_Picklez(file)
to_delete_ids = [v.index for v in g1.vs if v.index >= 30]
g1.delete_vertices(to_delete_ids)
g1.write_graphml("D:/CPM_no_adjacency_0000065_truncated.graphml")
#g1 = ig.Graph.Read_GraphMLz(file)
print(g1.vs[0])
