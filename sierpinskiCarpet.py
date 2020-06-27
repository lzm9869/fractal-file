import numpy as np
import graphClasses as gc
import copy

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

# building a level 1 carpet
# making 8 smaller copies of sc0
sC1 = gc.Graph()
scalingFactor = 1 / 3  # how much longer each graph connection is compared to its n+1 carpet counterpart
listOfFixedPoints = [np.array([0, 0]),  # q0
                     np.array([0.5, 0]),  # q1
                     np.array([1, 0]),  # q2
                     np.array([1, 0.5]),  # q3
                     np.array([1, 1]),  # q4
                     np.array([0.5, 1]),  # q5
                     np.array([0, 1]),  # q6
                     np.array([0, 0.5])]  # q7
for i in range(0, 8):
    copyOfSC0 = copy.deepcopy(sC0)
    for j in range(len(copyOfSC0.vertices)):
        copyOfSC0.vertices[j].name = copyOfSC0.vertices[j].name + str(i)
    copyOfSC0.contract_graph(scalingFactor, listOfFixedPoints[i])
    sC1.add_graph(copyOfSC0)


sC1.remove_redundancies()
sC1.apply_harmonic_function()
for v in sC1.vertices:
    print(v.name)
sC1.print_graph()
print(sC1.energy_of_graph())
