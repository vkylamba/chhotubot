import json

graph = {}
with open('graph.json') as f:
    graph = json.load(f)


def get_path(source, destination, path=''):
    source = str(source)
    destination = str(destination)
    if source in graph:
        source_dict = graph.get(source)
        destination_path = source_dict.get(destination, [])
        if destination_path:
            for each_node in destination_path:
                if path:
                    path = path + ','
                if each_node in source_dict:
                    path = path + get_path(source, each_node, path)
                else:
                    path = path + each_node
    return path


if __name__ == '__main__':
    print(get_path("1,5", "1,1"))
