import networkx as nx
import matplotlib.pyplot as plt


def simplify_filename(filename):
    return filename[filename.rindex('_') - 3:-4]


def draw_relation(point_dict: dict):
    start_nodes = []
    end_nodes = []
    edges = []
    for k, l in point_dict.items():
        start_nodes.append(k)
        for v in l:
            end_nodes.append(v)
            edges.append((k,v))

    g = nx.DiGraph()
    g.add_nodes_from(start_nodes+end_nodes)
    g.add_edges_from(edges)
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g,pos,nodelist=start_nodes,node_color='red')
    nx.draw_networkx_nodes(g,pos,nodelist=end_nodes,node_color='blue')
    nx.draw_networkx_edges(g,pos,edgelist=edges)
    #nx.draw(g, with_labels=True)
    plt.show()


if __name__ == '__main__':
    g = nx.DiGraph()
    g.add_node('aa')
    g.add_node('bb')
    g.add_edge('aa','bb')

    nx.draw(g, with_labels=True,node_color=['blue','red'])
    plt.show()
