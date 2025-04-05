import json
from pathlib import Path


def json_to_file(f_name, sometext, dir="data"):
    json_object = json.dumps(sometext, indent=4)
    with open(f'{dir}/{f_name}.json', "w") as outfile:
        outfile.write(json_object)

def add_to_list(my_list, new_item):
    if new_item not in my_list:
        my_list.append(new_item)
    return my_list

def make_dir(path):
    directory_path = Path(path)

    try:
        directory_path.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass

def get_nested(data, path):
    if path and data:
        element  = path[0]
        if element:
            # value = data.get(element)
            value = data[element]
            return value if len(path) == 1 else get_nested(value, path[1:])
def test_echo():
    print('itwokr')

if __name__ == "__main__":
    print('wat')
    # get_nested("20250331")
    # print(f'gg')