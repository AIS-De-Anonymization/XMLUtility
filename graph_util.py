import networkx as nx
import matplotlib.pyplot as plt

def draw_relation(point_dict):
    G = nx.DiGraph()
    for x, y in point_dict.items():
        for t in y:
            G.add_edge(x, t)
    nx.draw(G, with_labels=True)
    plt.show()


if __name__ == '__main__':
    pass