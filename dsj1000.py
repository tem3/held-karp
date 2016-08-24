import graph_tool.all as gt
import numpy as np
from scipy import spatial
import neighbor_lists as nl


"""
Creates new graph-tool graph instance from the graph from TSPLIB:
http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
"""

num_quadrant = 7
num_other_vertices = 12
min_x= min_y= max_x= max_y = None


lines = []

g = gt.Graph(directed = True)
g.properties[("v", "position")] = g.new_vertex_property("vector<double>")
g.properties[("e", "lengths")] = g.new_edge_property("double")


count = 0
with open("dsj1000.txt", "r") as raw:
    for line in raw:
        if line != 'EOF' and line != '':
            print line
            if count > 5:
                split = line.strip().split(' ')
                if split != []:
                    split = [int(split[1]), int(split[2])]
                    v = g.add_vertex()
                    g.vp.position[v] = split
                    lines.append(split)
            else:
                count+=1
                
lines = np.array(lines)
num_vertices = len(lines)
tree = spatial.KDTree(lines)
distances, hoods_arr = tree.query(lines, num_vertices)

distances = [dist[1:] for dist in distances]
hoods_arr = [nbhd[1:] for nbhd in hoods_arr]

g.properties[("e", "neighborhoods")] = g.new_edge_property("boolean")

neighborhoods_array = [
    nl.NeighborLists(g, vertex, distances[index], hoods_arr[index]).neighborhood \
    for index, vertex in enumerate(g.vertices())] 


           
gt.graph_draw(g, pos=g.vp.position)    
property_map = gt.group_vector_property(neighborhoods_array)
g.properties[("e", "neighborhoods")] = property_map

g.save("dsj1000.gt")
