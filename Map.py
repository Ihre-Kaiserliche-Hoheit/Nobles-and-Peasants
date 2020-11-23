import networkx as nx
import matplotlib.pyplot as plt

class Node():
    pass

G = nx.Graph() #Reminder to self, don't forget the goddamn brackets again
G.add_node(Node())


nx.draw_networkx(G)
nx.draw_random(G)
nx.draw_circular(G)
nx.draw_spectral(G)
plt.show()
