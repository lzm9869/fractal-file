import graphClasses as gc
import copy

# building the level 0 carpet
sC0 = gc.Graph()
a = gc.Vertex("a")
b = gc.Vertex("b")
c = gc.Vertex("c")
d = gc.Vertex("d")
e = gc.Vertex("e")
sC0.add_vertex(a)
sC0.add_vertex(b)
sC0.add_vertex(c)
sC0.add_vertex(d)
sC0.add_vertex(e)
sC0.add_edge(a, e, 1)
sC0.add_edge(b, e, 1)
sC0.add_edge(c, e, 1)
sC0.add_edge(d, e, 1)

# building a level 1 carpet
# making 8 smaller copies of sc0
sC1 = gc.Graph()
scalingFactor = 3 #how much longer each graph connection is compared to its n+1 carpet counterpart
for i in range(0, 8):
    copyOfSC0 = copy.deepcopy(sC0)
    for j in range(len(copyOfSC0.vertices)):
        copyOfSC0.vertices[j].weights[:] = [x / scalingFactor for x in copyOfSC0.vertices[j].weights]
        copyOfSC0.vertices[j].name = copyOfSC0.vertices[j].name + str(i)
    sC1.add_graph(copyOfSC0)

sC1.print_graph()
# adding them all to sC1


