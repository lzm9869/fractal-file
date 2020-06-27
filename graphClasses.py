import numpy as np
import copy


class Vertex:
    # an object with a name, a list of neighbors, and a list of weights
    # name is a string that the vertex is referred to
    # neighbors is a list of Vertex objects that corresponds to all the vertices this vertex shares an edge with
    # weights is a list of floats that corresponds to the weight of the edge connecting this vertex
    #   and the neighbor at the same index
    # position is a list of 2 values, [x-coordinate, y-coordinate]
    # example: name = 'A'; neighbors = ('B','C'); weights = (4,10)
    # the above means that vertex A shares an edge of weight 4 with vertex B and an edge of weight 10 with vertex C
    def __init__(self, n):
        self.name = n
        self.neighbors = list()
        self.position = None
        self.harmonicValue = None

    # if there are optimization problems, might be able to change this so that the neighbor lists
    #   are lists of strings, not Vertex objects
    def add_neighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)


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

    def add_edge(self, u, v):
        # allows you to add edges to vertices in a graph
        # checks that both vertices (u, v) are in the graph, then makes them neighbors of each other
        if u in self.vertices and v in self.vertices:
            u.add_neighbor(v)
            v.add_neighbor(u)
            return True
        else:
            return False

    def contract_graph(self, scale, fixedPoint):
        # contracts a graph by a scale towards a fixed point
        # since v.position and fixedPoint are numpy arrays, the formula written works
        # NOTICE: will need to change this once the code is modified for affine graphs
        for v in self.vertices:
            v.position = scale * (v.position - fixedPoint) + fixedPoint

    def combine_vertices(self, u, v):
        # little sloppy but should work for our purposes
        pointsWithVAsNeighbor = list()
        for n in v.neighbors:
            pointsWithVAsNeighbor.append(n)
            u.neighbors.append(n)
        self.vertices.remove(v)
        for p in pointsWithVAsNeighbor:
            p.neighbors.remove(v)
            p.neighbors.append(u)

    def add_graph(self, g):
        # copies all the Vertex objects from a graph to another graph
        for v in g.vertices:
            self.add_vertex(v)

    def remove_redundancies(self):
        # combines any points with the same position
        # this seems to have a high complexity, which may cause problems
        repeatedPoints = list()
        seenPoints = list()
        for v in self.vertices:
            neverSeen = True
            for q in seenPoints:
                if np.allclose(v.position, q.position):
                    repeatedPoints.append(v)
                    neverSeen = False
                    break
            if neverSeen:
                seenPoints.append(v)
        for p in repeatedPoints:
            for u in seenPoints:
                if np.allclose(p.position, u.position):
                    self.combine_vertices(p, u)
                    break

    def apply_harmonic_function(self):
        for v in self.vertices:
            v.harmonicValue = v.position[0]  # starts with the function f(x, y) = x
        greatestDifference = 1
        desiredAccuracy = .00000001
        while greatestDifference > desiredAccuracy:
            greatestDifference = 0
            for u in self.vertices:
                if not (u.harmonicValue == 0 or u.harmonicValue == 1):
                    oldHarmonicValue = copy.deepcopy(u.harmonicValue)
                    listOfHarmonicValues = []
                    for n in u.neighbors:
                        listOfHarmonicValues.append(n.harmonicValue)
                    u.harmonicValue = sum(listOfHarmonicValues) / len(listOfHarmonicValues)
                    differenceBetweenHarmonicValues = abs(oldHarmonicValue - u.harmonicValue)
                    if differenceBetweenHarmonicValues > greatestDifference:
                        greatestDifference = differenceBetweenHarmonicValues

    def energy_of_graph(self):
        totalOfSquaredDifferences = 0
        for v in self.vertices:
            for n in v.neighbors:
                totalOfSquaredDifferences += (v.harmonicValue - n.harmonicValue)**2
        return totalOfSquaredDifferences / 2

    def print_graph(self):
        for i in range(len(self.vertices)):
            print(self.vertices[i].name + " has neighbors:")
            for n in self.vertices[i].neighbors:
                print(n.name)
            print("and is in position:")
            print(self.vertices[i].position)
            print("and has a harmonic function value of:")
            print(self.vertices[i].harmonicValue)
            print()


# test code
"""
g = Graph()
f = Graph()
a = Vertex("a1")
b = Vertex("b1")
c = Vertex("c1")
d = Vertex("d1")
a.position = np.array([0, 0])
b.position = np.array([1, 0])
c.position = np.array([0, 1])
d.position = np.array([0, 0])
# a and d should be combined
g.add_vertex(a)
g.add_vertex(b)
g.add_vertex(c)
g.add_vertex(d)
g.add_edge(a, b)
g.add_edge(c, d)
print("graph 1")
g.print_graph()
g.remove_redundancies()
print("graph 2")
g.print_graph()
"""
