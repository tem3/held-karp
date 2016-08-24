import graph
import graph_tool.all as gt
import numpy as np
import sys, os, os.path

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

"""
    Runs the Held Karp algorithm.
    Takes in a Graph object (wrapper for graph-tool graph class)
    and runs the algorithm to determine a lower bound.
"""
class HeldKarp(object):
    
    def __init__(self, graph_class, seq_length):
        self.graph_class = graph_class
        self.graph = graph_class.graph
        self.neighborhoods = self.graph_class.get_neighborhoods()
        self.e_weights = self.graph_class.get_edge_weights()
        self.not_zero_prop, self.not_zero_graph = self.graph_class.not_zero()
        self.v_weights = self.create_vertex_weights()
        self.seq_length = seq_length

        self.best_tree = None
        self.current_tree = None
        
        self.bound = self.initialize_bound()
        self.costs = self.initialize_costs()
        self.degree = self.initialize_degree()
        self.t_init = self.initialize_step()
        self.prev_degree = self.degree
        self.step = 0

        self.loop()

    
    def create_vertex_weights(self):
        v_weights = self.graph.new_vertex_property("double", val=0.0)
        return v_weights

    def initialize_bound(self):
        bound = 0.0
        return bound

    def initialize_costs(self):
        costs = self.graph.new_edge_property("double", val=float('Inf'))
        return costs

    def initialize_degree(self):
        tree_prop = gt.min_spanning_tree(self.graph, self.e_weights)
        tree = gt.GraphView(self.graph, efilt=tree_prop)
        degree = tree.degree_property_map("total")
        return degree
    
    def update_edge_weights(self):
  
        for v in self.graph.vertices():
            v_ind = self.graph.vertex_index[v]
            
            subgraph = gt.GraphView(self.graph, efilt=self.neighborhoods[v_ind])
            
            for e in subgraph.edges():
                v2 = e.target()
                self.costs[e] = self.e_weights[e] + self.v_weights[v] + self.v_weights[v2]
     
        tree_prop = gt.min_spanning_tree(self.not_zero_graph, weights=self.costs)
        (s1, t1), (s2, t2) = self.least_edges()
        e1 = self.graph.edge(s1,t1)
        e2 = self.graph.edge(s2,t2)

        tree_prop[e1] = True
        tree_prop[e2] = True
        return tree_prop

    # returns the two edges with the smallest weights    
    def least_edges(self):
        v0 = self.graph.vertex(0)
        subgraph = gt.GraphView(self.graph, efilt=self.neighborhoods[0])
        sorted_edges = sorted(subgraph.edges(), key=lambda e: self.costs[e])
        e1 = sorted_edges[0]
        e2 = sorted_edges[1]
        s1 = e1.source()
        s2 = e2.source()
        t1 = e1.target()
        t2 = e2.target()
        return (s1,t1),(s2,t2)

    # performs the iterations of the Held Karp algorithm
    def loop(self):
        
        for m in range(1, self.seq_length+1):
            print ("begin step: ", m)
            tree_prop = self.update_edge_weights()
            tree_cost = self.cost_of_tree(tree_prop)
            self.current_tree = gt.GraphView(self.graph, efilt=tree_prop)

            # draw the best spanning tree yet found every 125 iterations
            if m % 125 == 0:
                position = self.graph_class.position
                self.graph_class.draw(self.best_tree, position)
                
            self.prev_degree = self.degree.copy()
            self.degree = self.current_tree.degree_property_map("total")
            vertex_sum = self.sum_of_vertex_weights()
            bound = tree_cost - 2*vertex_sum
            print("current best bound: ", self.bound)

            
            if m != self.seq_length:
                print( "new bound: ", bound)
                if bound > self.bound:
                    self.bound = bound
                    self.best_tree = self.current_tree
                self.step = self.next_step(m)
                self.update_vertex_weights()
            else:
                print self.bound
                gt.graph_draw(gt.GraphView(self.graph, efilt=tree_prop), self.graph_class.position)
            
            
    def cost_of_tree(self, tree_prop):
      
        tree = gt.GraphView(self.graph, efilt=tree_prop)
        tree_cost = 0
        for e in tree.edges():
            tree_cost += self.costs[e]
        return tree_cost
    
    def sum_of_vertex_weights(self):
        v_sum = 0
        for v in self.graph.vertices():
            v_sum += self.v_weights[v]
        print v_sum
        return v_sum

    # determines the initial step length
    def initialize_step(self):
        tree_prop = gt.min_spanning_tree(self.graph, weights = self.e_weights)
        tree = gt.GraphView(self.graph, efilt=tree_prop)
        gt.graph_draw(tree, self.graph_class.position)
        self.best_tree = tree
        tree_cost = 0
        
        for e in tree.edges():
            tree_cost += self.e_weights[e]
            
        t = (1/(2.0*self.graph_class.size)) * tree_cost
        return t

    # updates the step length for each new iteration
    def next_step(self, m):
        bigM = 1.0*self.seq_length
        step = self.t_init *( (m-1)*((2*bigM - 5)/(2*(bigM-1))) - (m-2) + (1/2.0)*( (m**2-3*m+2)/(bigM**2-3*bigM+2)))
        return step

    def update_vertex_weights(self):
        
        for v in self.graph.vertices():
            d_curr = self.degree[v]
            d_prev = self.prev_degree[v]
            if d_curr !=2:
                self.v_weights[v] = self.v_weights[v] + 0.6*self.step * (d_curr-2) + 0.4*self.step*(d_prev-2)

