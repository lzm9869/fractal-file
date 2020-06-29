import numpy as np
import graphClasses as gc
import copy

#  INPUT HERE what level precarpet would you like?
precarpet_level = 2

# building the level 0 cross carpet
sC0 = gc.Graph()
a = gc.Vertex("a")
b = gc.Vertex("b")
c = gc.Vertex("c")
d = gc.Vertex("d")
e = gc.Vertex("e")
a.position = np.array([0, 0.5])
b.position = np.array([0.5, 1])
c.position = np.array([1, .5])
d.position = np.array([0.5, 0])
e.position = np.array([0.5, 0.5])
sC0.add_vertex(a)
sC0.add_vertex(b)
sC0.add_vertex(c)
sC0.add_vertex(d)
sC0.add_vertex(e)
sC0.add_edge(a, e)
sC0.add_edge(b, e)
sC0.add_edge(c, e)
sC0.add_edge(d, e)

sCn = copy.deepcopy(sC0)
sCn_plus_one = gc.Graph()
scalingFactor = 1 / 3  # how much longer each graph connection is compared to its n+1 carpet counterpart
listOfFixedPoints = [np.array([0, 0]),  # q0
                     np.array([0.5, 0]),  # q1
                     np.array([1, 0]),  # q2
                     np.array([1, 0.5]),  # q3
                     np.array([1, 1]),  # q4
                     np.array([0.5, 1]),  # q5
                     np.array([0, 1]),  # q6
                     np.array([0, 0.5])]  # q7

for k in range(precarpet_level):
    sCn_plus_one = gc.Graph()
    for i in range(0, 8):
        copyOfSCn = copy.deepcopy(sCn)
        for j in range(len(copyOfSCn.vertices)):
            copyOfSCn.vertices[j].name = copyOfSCn.vertices[j].name + str(i)
        copyOfSCn.contract_graph(scalingFactor, listOfFixedPoints[i])
        sCn_plus_one.add_graph(copyOfSCn)
    sCn_plus_one.remove_redundancies()
    sCn = copy.deepcopy(sCn_plus_one)

sCn_plus_one.apply_harmonic_function()
for v in sCn_plus_one.vertices:
    print(v.name)
sCn_plus_one.print_graph()
sCn_plus_one.print_vertices_x_y_f()
print("Resistance of the graph is", sCn_plus_one.resistance_of_graph())
