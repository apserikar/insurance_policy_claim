import json

def read_json(file_name):

    with open(file_name, "r") as json_file:
        data = json.load(json_file)
        return data


