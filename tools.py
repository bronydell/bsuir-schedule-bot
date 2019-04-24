import json


def read_json_file(filename):
    """ Read file's content and convert json to dictionary """
    with open(file=filename, encoding="UTF-8") as file:
        return json.load(file)
