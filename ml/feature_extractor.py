import os, re
from xml.dom import minidom
import config


def save_title_match(directory, target_directory, target_filename):
    # regexes specifically for IndustryType="Information Technology Sector"
    regexes = [r'Phishing', r'Malicious', r'Theme', r'Rat', r'\d{6}.\d{2}', r'IIR.+?\d.+?\d{3}.+?\d{4}.+?\d{2}', r'CRF.+?\d{5}.+?\d{3}', r'.*?FO\d\d']
    with open(os.path.join(target_directory, target_filename), 'w') as file:
        line = ''
        for regex in regexes:
            line += 'r\'' + regex + '\' '
        file.write(line[:-1] + '\n')
    file_list = os.listdir(directory)
    file_list.sort(key=lambda t: (int(t[t.index('_') + 1: t.rindex('_')]), int(t[t.rindex('_') + 1: -4])))
    for filename in file_list:
        filepath = os.path.join(directory, filename)
        if filepath == ".DS_Store":
            continue
        with open(filepath, 'r', encoding="utf-8") as file:
            search = re.search(r'<stix:Title>([^<]*?)</stix:Title>',file.read())
            title = search.group(1) if search else None
            if title and re.search(r'to.*?activity',title, flags=re.IGNORECASE):
                print(filename + ': '+ title)
        with open(os.path.join(target_directory, target_filename), 'a') as file:
            line = filename + ' '
            for regex in regexes:
                line += ('1' if title and re.search(regex, title, flags=re.IGNORECASE) else '0') + ' '
            file.write(line[:-1] + '\n')


def extract_node_name(node) -> set:
    node_names = set()
    node_names.add(node.nodeName)
    if node.childNodes:
        for child_node in node.childNodes:
            if child_node.nodeType != child_node.TEXT_NODE:
                node_names |= extract_node_name(child_node)
    return node_names


def save_node_name(directory, target_directory, target_filename):
    node_names = {}
    file_count = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filepath == ".DS_Store":
            continue
        root = minidom.parse(filepath).documentElement
        for node_name in extract_node_name(root):
            node_names[node_name] = node_names.get(node_name, 0) + 1
        file_count += 1
    for key in list(node_names):
        if node_names[key] == file_count:
            del (node_names[key])
    sorted_node_name = sorted(node_names.items(), key=lambda t: t[0])
    with open(os.path.join(target_directory, target_filename), 'w') as file:
        # write node names
        line = ''
        for node_name, _ in sorted_node_name:
            line += node_name + ' '
        file.write(line[:-1] + '\n')
        # write each file
        file_list = os.listdir(directory)
        file_list.sort(key=lambda t: (int(t[t.index('_') + 1: t.rindex('_')]), int(t[t.rindex('_') + 1: -4])))
        for filename in file_list:
            filepath = os.path.join(directory, filename)
            if filepath == ".DS_Store":
                continue
            root = minidom.parse(filepath).documentElement
            single_node_names = extract_node_name(root)
            line = filename + ' '
            for node_name, _ in sorted_node_name:
                line += ('1' if node_name in single_node_names else '0') + ' '
            file.write(line[:-1] + '\n')


def feature_file_loader(file_path) -> (list, list, list):
    data = []
    labels = []
    file_names = []
    with open(file_path, 'r') as file:
        label_line = file.readline()[:-1]
        for label in label_line.split(' '):
            labels.append(label)
        for single_line in file.readlines():
            single_list = single_line.split(' ')
            file_names.append(single_list[0])
            data.append([int(x) for x in single_list[1:]])
    return data, labels, file_names


if __name__ == '__main__':
    #save_node_name(config.ML_DIRECTORY_PATH, config.ML_DATA_PATH, 'node_1.txt')
    save_title_match(config.ML_DIRECTORY_PATH, config.ML_DATA_PATH, 'title.txt')
