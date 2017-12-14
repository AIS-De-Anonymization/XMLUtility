import networkx as nx
import matplotlib.pyplot as plt


def draw_relation(point_dict: dict):
    g = nx.DiGraph()
    for x, y in point_dict.items():
        for t in y:
            g.add_edge(x, t)
    nx.draw(g, with_labels=True)
    plt.show()


if __name__ == '__main__':
    pass
