import os
from xml.dom import minidom
import config


def extract_node_name(node) -> set:
    node_set = set()
    node_set.add(node.nodeName)
    if node.childNodes:
        for child_node in node.childNodes:
            if child_node.nodeType != child_node.TEXT_NODE:
                node_set |= extract_node_name(child_node)
    return node_set


if __name__ == '__main__':
    directoryPath = config.ML_DIRECTORY_PATH
    nodeNames = {}
    fileCount = 0
    for filename in os.listdir(directoryPath):
        filepath = os.path.join(directoryPath, filename)
        if filepath == ".DS_Store":
            continue
        root = minidom.parse(filepath).documentElement
        for node_name in extract_node_name(root):
            nodeNames[node_name] = nodeNames.get(node_name, 0) + 1
        fileCount += 1
    for key in list(nodeNames):
        if nodeNames[key] == fileCount:
            del(nodeNames[key])

    print(len(sorted(nodeNames.items(), key=lambda t: t[1])))
