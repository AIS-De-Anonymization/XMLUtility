import os, re
import config, graph_util


if __name__ == '__main__':
    directoryPath = config.DIRECTORY_PATH
    id_file = {}
    id_relatedId = {}
    for filepath in os.listdir(directoryPath):
        if filepath == ".DS_Store":
            continue
        with open(os.path.join(directoryPath, filepath), 'r', encoding="utf-8") as file:
            for line in file:
                searches = re.search(r'id="[^"]*?([A-Z]{2}-\d{2}-\d{5}\w?)"', line)
                if searches:
                    search = searches.group(0 if not searches.lastindex else searches.lastindex)
                    id = search
                    id_file[id] = filepath
                searches = re.findall(r'[A-Z]{2}-\d{2}-\d{5}\w?', line)
                if searches:
                    for search in searches:
                        if id != search:
                            if id in id_relatedId:
                                if search not in id_relatedId[id]:
                                    id_relatedId[id].append(search)
                            else:
                                id_relatedId[id] = [search]

    relation = {}
    for _id, _related_id_list in id_relatedId.items():
        for _related_id in _related_id_list:
            if _related_id in id_file:
                print(_id + ' (' + id_file[_id] + ') -> ' + _related_id + ' (' + id_file[_related_id] + ')')
                if _id in relation:
                    relation[_id].append(_related_id)
                else:
                    relation[_id] = [_related_id]
    graph_util.draw_relation(relation)