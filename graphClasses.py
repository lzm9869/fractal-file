class Vertex:
    # an object with a name, a list of neighbors, and a list of weights
    # name is a string that the vertex is refered to
    # neighbors is a list of Vertex objects that corresponds to all the vertices this vertex shares an edge with
    # weights is a list of floats that corresponds to the weight of the edge connecting this vertex and the neighbor at the same index
    # position is a list of 2 values, [x-coordinate, y-coordinate]
    # example: name = 'A'; neighbors = ('B','C'); weights = (4,10)
    # the above means that vertex A shares an edge of weight 4 with vertex B and an edge of weight 10 with vertex C
    def __init__(self, n):
        self.name = n
        self.neighbors = list()
        self.weights = list()
        self.position = list()
    
    # if there are optimization problems, might be able to change this so that the neighbor lists are lists of strings, not Vertex objects
    def add_neighbor(self, v, w):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.weights.append(w)

class Graph:
    # an object that is simply a list of vertices
    def __init__(self):
        self.vertices = []

    def add_vertex(self, vertex):
    # allows you to add vertices to a graph
    # checks that the input was a vertex and that the vertex is not already in the graph
        if isinstance(vertex, Vertex) and vertex not in self.vertices:
            self.vertices.append(vertex)
            return True
        else:
            return False
    
    def add_edge(self, u, v, w):
    # allows you to add edges to vertices in a graph
    # checks that both vertices (u, v) are in the graph, then makes them neighbors of each other with the desired weight (w)
        if u in self.vertices and v in self.vertices:
            u.add_neighbor(v, w)
            v.add_neighbor(u, w)
            return True
        else:
            return False
    
    def contract_graph(self, scale, fixedPoint):
        for v in self.vertices:
            v.weight = [x.weight / scale for x in v.weight]
            v.position[0] = scale * (v.position[0] - fixedPoint[0]) + fixedPoint[0]
            v.position[1] = scale * (v.position[1] - fixedPoint[1]) + fixedPoint[1]

    def combine_vertices(self, u, v):
    # little sloppy but should work for our purposes
        u.neighbors.append(n for n in v.neighbors)
        u.neighbors.append(w for w in v.weights)
        self.vertices.remove(v)

    def add_graph(self, g):
    # copies all the Vertex objects from a graph to another graph
        for v in g.vertices:
            self.add_vertex(v)
    
    def remove_redundencies(self):
    # combines any points with the same position
        repeatedPoints = set()
        seenPoints = set()
        for v in self.vertices:
            if v.position not in seenPoints:
                seenPoints.add(v.position)
            else:
                repeatedPoints.add(v)
        for p in repeatedPoints:
            # work on this some other time
            pass


    def print_graph(self):
        for i in range(len(self.vertices)):
            print(self.vertices[i].name + " has neighbors and weights as follows:")
            for j in range(len(self.vertices[i].neighbors)):
                print(self.vertices[i].neighbors[j].name + " " + str(self.vertices[i].weights[j]))

# test code
'''
g = Graph()
f = Graph()
a = Vertex("a")
b = Vertex("b")
c = Vertex("c")
d = Vertex("d")
g.add_vertex(a)
g.add_vertex(b)
g.add_vertex(c)
f.add_vertex(d)
f.add_graph(g)
g.add_edge(a, b, 3)
g.add_edge(a, c, 2)
g.print_graph()
f.print_graph()
'''