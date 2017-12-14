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


def data_loader(file_path) -> (list, list):
    data = []
    file_names = []
    with open(file_path, 'r') as file:
        file.readline()
        for single_line in file.readlines():
            single_list = single_line.split(' ')
            file_names.append(single_list[0])
            data.append([int(x) for x in single_list[1:]])
    return data, file_names


if __name__ == '__main__':
    directoryPath = config.ML_DIRECTORY_PATH
    dataDirectoryPath = config.ML_DATA_PATH
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
    sortedNodeName = sorted(nodeNames.items(), key=lambda t: (-t[1], t[0]))

    with open(os.path.join(dataDirectoryPath, 'node.txt'),'w') as file:
        # write Node names
        line = ''
        for node_name, _ in sortedNodeName:
            line += node_name + ' '
        file.write(line[:-1] + '\n')
        # write each file
        fileList = os.listdir(directoryPath)
        fileList.sort(key=lambda t: int(t[t.rindex('_') + 1: -4]))
        for filename in fileList:
            filepath = os.path.join(directoryPath, filename)
            if filepath == ".DS_Store":
                continue
            root = minidom.parse(filepath).documentElement
            node_names = extract_node_name(root)
            line = filename + ' '
            for node_name, _ in sortedNodeName:
                line += ('1' if node_name in node_names else '0') + ' '
            file.write(line[:-1] + '\n')
