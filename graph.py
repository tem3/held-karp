import graph_tool.all as gt
import numpy as np
from numpy.random import randint

# Wrapper for the graph-tool graph class
class Graph(object):
    
    def __init__(self):
        self.graph = gt.load_graph("dsj1000.gt")
        self.size = self.graph.num_vertices()
        self.position = self.graph.vp["position"]
        self.e_weights = self.graph.ep["lengths"]
        self.not_zero_prop, self.not_zero_graph = self.not_zero()
        self.neighborhoods = gt.ungroup_vector_property(self.graph.ep.neighborhoods, np.arange(self.size))

   
    def draw(self, g, pos=None, v_prop=None, e_prop=None):
        gt.graph_draw(g, pos=pos)

    def get_graph(self):
        return self.graph
    
    def get_position(self):
        return self.position
    
    def get_edge_weights(self):
        return self.e_weights
    
    def get_neighborhoods(self):
        return self.neighborhoods

    def get_not_zero_prop(self):
        return self.not_zero_prop
    
    def get_not_zero_graph(self):
        return self.not_zero_graph

    """
    returns a new instance of the graph-tool class that does not contain
    thezeroth vertex
    """
    def not_zero(self):
        v0 = self.graph.vertex(0)
        not_zero_prop = self.graph.new_vertex_property("boolean", val = True)
        not_zero_prop[v0] = False
        not_zero_graph = gt.GraphView(self.graph, vfilt=not_zero_prop)
        return not_zero_prop, not_zero_graph
        
   
    def edge_index(self, edge):
        return self.graph.edge_index[edge]

    def vertex_index(self, vertex):
        return self.graph.vertex_index[vertex]

    
    
