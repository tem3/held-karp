# held-karp
Python implementation of the Held-Karp algorithm

Requires graph-tool and numpy packages.

held_karp.py
Runs the Held-Karp algorithm on an instance of the Graph class. Find the Held-Karp lower bound for the traveling salesman tour after a pre-determined number of iterations.

graph.py
A wrapper class for the graph-tool graph class.

neighbor_lists.py
Creates a list of the closest neighbors of a vertex, ensuring a mix of vertices in multiple quadrants if possible.

dsj1000.py
Creates a graph-tool Graph instance from an example graph from the TSPLIB (http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)
