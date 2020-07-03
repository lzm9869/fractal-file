import numpy as np
import copy


class Graph:
    # an object that is simply a dictionary of vertices
    # the key is the name of the vertex and refers to a list
    # index 0 is a list of strings referring to the keys of the vertex's neighbors
    # index 1 is a numpy array of 2 values referring to the x and y coordinates of the vertex, respectively
    # index 2 is the harmonicValue of the point
    def __init__(self):
        self.vertices = {}

    def __deepcopy__(self, memodict={}):
        theCopy = Graph()
        for v in self.vertices:
            theCopy.vertices[v] = copy.deepcopy(self.vertices[v])
        return theCopy

    # noinspection PyUnusedLocal
    def add_vertex(self, name, xyCoordinates):
        # allows you to add vertices to a graph
        # adds a new key to the vertices dictionary that refers to the list corresponding to the vertex
        # the key is the string input for name, the position input should be a list and is transformed into an np.array
        # and 0 is put as a placeholder harmonic value
        self.vertices[name] = [[], np.array(xyCoordinates), 0]

    def add_edge(self, u, v):
        # allows you to add edges to vertices in a graph
        # input is 2 strings, function makes sure the strings are both keys in the vertices dictionary and then adds
        #   each string to each other's neighbor lists
        if u in self.vertices and v in self.vertices:
            self.vertices[v][0].append(u)
            self.vertices[u][0].append(v)

    def contract_graph(self, scale, fixedPoint):
        # contracts a graph by a scale towards a fixed point
        # since v[1] (the position) and fixedPoint are numpy arrays, the formula written works
        # NOTICE: will need to change this once the code is modified for affine graphs
        for v in self.vertices:
            self.vertices[v][1] = scale * (self.vertices[v][1] - fixedPoint) + fixedPoint

    def combine_vertices(self, u, v):
        for n in self.vertices[v][0]:
            self.vertices[u][0].append(n)
            for neigh in self.vertices[v][0]:
                self.vertices[neigh][0].remove(v)
                self.vertices[neigh][0].append(u)
        self.vertices.pop(v)

    def update_all_vertices_names(self, update):
        self.vertices = {key+update: value for key, value in self.vertices.items()}
        for v in self.vertices:
            self.vertices[v][0] = [n+update for n in self.vertices[v][0]]

    def add_graph(self, gr):
        # copies all the Vertex objects from a graph to another graph
        grCopy = copy.deepcopy(gr)
        self.vertices.update(grCopy.vertices)

    def remove_redundancies(self):
        # combines any points with the same position
        repeatedPoints = list()
        seenPoints = list()
        for v in self.vertices:
            neverSeen = True
            for q in seenPoints:
                if np.allclose(self.vertices[v][1], self.vertices[q][1]):
                    repeatedPoints.append(v)
                    neverSeen = False
                    break
            if neverSeen:
                seenPoints.append(v)
        for p in repeatedPoints:
            for u in seenPoints:
                if np.allclose(self.vertices[p][1], self.vertices[u][1]):
                    self.combine_vertices(p, u)
                    seenPoints.remove(u)
                    break

    def apply_harmonic_function(self):
        for v in self.vertices:
            self.vertices[v][2] = self.vertices[v][1][0]  # starts with the function f(x, y) = x
        greatestDifference = 1
        desiredAccuracy = .01
        while greatestDifference > desiredAccuracy:
            print(greatestDifference)
            greatestDifference = 0
            for u in self.vertices:
                if not (self.vertices[u][2] == 0 or self.vertices[u][2] == 1):
                    oldHarmonicValue = copy.deepcopy(self.vertices[u][2])
                    listOfHarmonicValues = []
                    for n in self.vertices[u][0]:
                        listOfHarmonicValues.append(self.vertices[n][2])
                    self.vertices[u][2] = np.mean(listOfHarmonicValues)
                    differenceBetweenHarmonicValues = abs(oldHarmonicValue - self.vertices[u][2])
                    if differenceBetweenHarmonicValues > greatestDifference:
                        greatestDifference = differenceBetweenHarmonicValues

    def resistance_of_graph(self):
        totalOfSquaredDifferences = 0
        for v in self.vertices:
            for n in self.vertices[v][0]:
                totalOfSquaredDifferences += (self.vertices[v][2] - self.vertices[n][2]) ** 2
        return 1 / (totalOfSquaredDifferences / 2)

    def print_graph(self):
        for v in self.vertices:
            print(v, "has neighbors:")
            for n in self.vertices[v][0]:
                print(n)
            print("and is in position:")
            print(self.vertices[v][1])
            print("and has a harmonic function value of:")
            print(self.vertices[v][2])
            print()

    def print_vertices_x_y_f(self):
        for v in self.vertices:
            print(v, self.vertices[v][1], self.vertices[v][2])


# test code
'''
g = Graph()
g.add_vertex("a", [0, 0])
g.add_vertex("b", [1, 0])
g.add_vertex("c", [1, 1])
g.add_vertex("d", [1, 0])
g.add_edge("a", "b")
g.add_edge("c", "d")
g.contract_graph(1/2, [.5, .5])
g.remove_redundancies()
g.print_graph()
g.print_vertices_x_y_f()'''