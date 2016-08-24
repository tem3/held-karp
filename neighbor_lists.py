import graph_tool.all as gt


"""
    Given a graph and a vertex in the graph, creates a list of 40 closest
    vertices in each quadrant, with the given vertex as origin. 
"""
class NeighborLists(object):
    
    NE = 0
    NW = 1
    SE = 2
    SW = 3
    
    def __init__(self, graph, vertex, distance_list, vertex_list):
        self.NW, self.NE, self.SW, self.SE, self.rest = [[],[], [], [], []]
        self.not_added = []
        self.all_neighbors = []
        self.quadrant_length = 7
        self.rest_length = 12

        self.graph = graph
        self.num_vertices = len(distance_list)
        
        self.vertex_pos = self.graph.vp.position[vertex]
        self.distance_list = distance_list
        self.vertex_list = vertex_list
        self.positions = self.graph.vp.position
        self.lengths = self.graph.ep.lengths
        self.neighborhood = graph.new_edge_property("boolean", val=False)
        self.fill_lists()

        num_missing = 40 - (len(self.NW) + len(self.NE) + len(self.SW) + len(self.SE) + len(self.rest))
        if num_missing > 0:
            self.all_neighbors += (self.not_added[:num_missing])
        for neighbor in self.all_neighbors:
            edge = self.graph.add_edge(vertex, neighbor)
            length = self.calc_length(neighbor)
            self.neighborhood[edge] = True
            self.lengths[edge] = length

        
    def fill_lists(self):
        index = 0
        pos = self.vertex_pos
        while self.lists_not_full() and index != self.num_vertices:
            other_vertex = self.vertex_list[index]
            other_pos = self.positions[other_vertex]
            direction = self.get_direction(pos[0], pos[1], other_pos[0], other_pos[1])
            self.update_list(other_vertex, direction)
            index+=1
           
    
    def quadrant_not_full(self, quadrant):
        return len(quadrant) < self.quadrant_length

    def rest_not_full(self):
        return len(self.rest) < self.rest_length
    
    def update_list(self, other_vertex, direction):
        quadrant = self.relevant_list(direction)
      
        if self.quadrant_not_full(quadrant):
            quadrant.append(other_vertex)
            self.all_neighbors.append(other_vertex)
        elif self.rest_not_full():
            self.rest.append(other_vertex)
            self.all_neighbors.append(other_vertex)
        else:
            if len(self.not_added) < 21:
                self.not_added.append(other_vertex)
           
        

    def relevant_list(self, direction):
        if direction==0:
            return self.NE
        if direction==1:
            return self.NW
        if direction==2:
            return self.SE
        if direction==3:
            return self.SW

        
    def lists_not_full(self):
        if len(self.NW) == len(self.NE) == len(self.SW) == len(self.SE) == self.quadrant_length:
            if len(self.rest) == self.rest_length:
                return False
        return True

    
    def get_direction(self, pointx, pointy, otherx, othery):
        if otherx < pointx and othery < pointy:
 
            return NeighborLists.SW
        elif otherx > pointx and othery > pointy:
            return NeighborLists.NE
        elif otherx < pointx and othery > pointy:
            return NeighborLists.NW
        else:
            return NeighborLists.SE


    def calc_length(self, other_vertex):
        x1, y1 = self.vertex_pos
        x2, y2 = self.positions[other_vertex]
        length = ( (x1-x2)**2 + (y1-y2)**2 )**(1/2.0)
       
        return length
    
