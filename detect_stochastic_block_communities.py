from graph_tool.all import Graph, GraphView, minimize_nested_blockmodel_dl
import logging
import pickle

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

logging.info("reading dict")
file = open("D:/user_mapping_filtered_with_keys.pickle",'rb')
links = pickle.load(file)
file.close()
logging.info("read dict")

# Create a Graph object
g = Graph(directed=False)

# Create a property map for the vertex labels
v_label = g.new_vertex_property("int")

# Add the vertices to the graph
for node in links.keys():
    v = g.add_vertex()
    v_label[v] = node

# Add the edges to the graph
for node, edges in links.items():
    for edge in edges:
        g.add_edge(g.vertex(node), g.vertex(edge))

logging.info("built graph")

# Perform community detection
state = minimize_nested_blockmodel_dl(g, state_args=dict(overlap=True))

# Extract the communities
blocks = state.get_levels()[0].get_blocks()

# Create a list of communities, where each community is a list of nodes
communities = [[] for _ in range(int(blocks.a.max()) + 1)]
for v in g.iter_vertices():
    communities[int(blocks[v])].append(int(v))

# Sort the communities by size (largest first)
communities.sort(key=len, reverse=True)

# Write out the nodes in the top 10 communities to separate files
for i, community in enumerate(communities[:10]):
    with open(f'D:/stochastic/community_{i+1}.txt', 'w') as f:
        for node in community:
            f.write(f'{node}\n')

# Write out the community structure
with open('D:/stochastic/community_structure.txt', 'w') as f:
    for i, community in enumerate(communities):
        f.write(f'Community {i+1}: {community}\n')