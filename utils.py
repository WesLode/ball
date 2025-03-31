import json


def json_to_file(f_name, sometext):
    json_object = json.dumps(sometext, indent=4)
    with open(f'data/{f_name}.json', "w") as outfile:
        outfile.write(json_object)