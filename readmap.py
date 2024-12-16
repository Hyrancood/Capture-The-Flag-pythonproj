from multiprocessing.managers import Value
from typing import List, Tuple

import config
import gamemap as gmap


def parse_value(value: str):

    if not isinstance(value, str):
        raise TypeError(f"value should be a str, not '{type(value)}'")
    if value == "":
        raise ValueError("Empty value!")
    if all(character.isdigit() for character in value):
        return int(value)
    return value


def parse_object(object_string: str) -> dict:
    obj = {}
    if not isinstance(object_string, str):
        raise TypeError(f"value should be a str, not '{type(object_string)}'")
    if object_string == "":
        raise ValueError("Empty value!")
    for pair in object_string.split(","):
        if pair.count(":") != 1:
            raise ValueError(f"Invalid syntax: object '{pair}' hasn't (or has >1) separator ':'")
        key, value = pair.split(":")
        if obj.get(key.strip(), None) is not None:
            raise ValueError(f"Invalid syntax: repeated attribute '{key}'")
        obj[key.strip()] = parse_value(value.strip())
    return obj


def parse_file(file_content) -> dict:
    state = "START"
    data = {}
    current_key = None

    for line in file_content:
        line = line.strip()
        if line == "":
            continue
        if state == "READING":
            if line.startswith("-"):
                data[current_key].append(parse_object(line[1:].strip()))
            else:
                state = "START"
        if state == "START":
            if line.endswith(":"):
                current_key = line[:-1]
                data[current_key] = []
                state = "READING"
            else:
                raise ValueError("Invalid syntax: expected key ending with ':'")
    return data

def parse_map(file_content) -> gmap.Map:
    return gmap.Map(**parse_file(file_content))

def check_type_valid(parameter: str, value, t: type):
    if not isinstance(value, t):
        raise TypeError(f"Invalid value: '{parameter}' should be integer, not {type(value)}")


def is_name_valid(values: List[str]):
    if len(values) == 0:
        raise ValueError("Invalid structure: name section has no objects")
    parsed = [parse_object(val) for val in values]
    langs = {
        "ru": None,
        "en": None
    }
    for obj in parsed:
        for lang in obj:
            if lang != "ru" and lang != "en":
                raise ValueError(f"Invalid syntax: unexpected language: {lang}")
            langs[lang] = obj[lang]
    return True


def is_sizes_valid(values: List[str]):
    if len(values) == 0:
        raise ValueError("Invalid structure: sizes section has no objects")
    sizes = {
        'x': None,
        'y': None
    }
    parsed = [parse_object(val) for val in values]
    for obj in parsed:
        for size in obj:
            if size != 'x' and size != 'y':
                raise ValueError(f"Invalid syntax: unexpected size: '{size}'")
            if obj[size] == 0:
                raise ValueError(f"Invalid value: '{size}'-size should be >0")
            check_type_valid(size, obj[size], int)
            sizes[size] = obj[size]
    if not (isinstance(sizes["x"], int) and isinstance(sizes["y"], int)):
        if isinstance(sizes["x"], int):
            raise ValueError(f"Invalid structure: sizes should contains 'x' and 'y', has only 'x'")
        raise ValueError(f"Invalid structure: sizes should contains 'x' and 'y', has only 'y'")
    if sizes['x'] > 40 or sizes['x'] < 5:
        raise ValueError(f"Invalid value: 'x'-size should be between 5 and 40, 'x' = {sizes['x']}")
    if sizes['y'] > 22 or sizes['y'] < 3:
        raise ValueError(f"Invalid value: 'x'-size should be between 3 and 22, 'y' = {sizes['y']}")
    return True, sizes['x'], sizes['y']


def check_if_more_then_zero(parameter: str, value: int):
    if value < 1:
        raise ValueError(f"Invalid value: '{parameter}'-parameter should be >0")


def check_if_point_in_map(point: Tuple[int, int], map_size: Tuple[int, int]):
    if all(cord > 0 for cord in point):
        if point[0] <= map_size[0] and point[1] <= map_size[1]:
            return True
        else:
            raise ValueError(f"Invalid value: point {point} not fit in map sizes {map_size}")
    raise ValueError(f"Invalid value: point {point} should be between (1, 1) and {map_size}")


def is_platforms_valid(values: List[str], map_x_size: int, map_y_size: int, map: List[List[bool]]):
    parsed = [parse_object(val) for val in values]
    for platform in parsed:
        if 'x' not in platform:
            raise ValueError("Invalid syntax: every object in 'platforms' section should has 'x' parameter")
        if 'y' not in platform:
            raise ValueError("Invalid syntax: every object in 'platforms' section should has 'y' parameter")
        params = (('x', platform['x']), ('y', platform['y']),
                  ('w', platform.get('w', 1)), ('h', platform.get('h', 1)))
        for param in params:
            check_type_valid(*param, int)
            check_if_more_then_zero(*param)
        check_if_point_in_map((params[0][1], params[1][1]), (map_x_size, map_y_size))
        check_if_point_in_map((params[0][1] + params[2][1] - 1, params[1][1]), (map_x_size, map_y_size))
        check_if_point_in_map((params[0][1], params[1][1] + params[3][1] - 1), (map_x_size, map_y_size))
        check_if_point_in_map(
            (params[0][1] + params[2][1] - 1, params[1][1] + params[3][1] - 1),
            (map_x_size, map_y_size))
        for x in range(params[0][1]-1, params[0][1]-1+params[2][1]):
            for y in range(map_y_size - params[1][1] - params[3][1] + 1,
                           map_y_size - params[1][1] + 1):
                map[y][x] = True
    return True


def is_thorns_valid(values: List[str], map_x_size:int, map_y_size:int, map:List[List[bool]]):
    parsed = [parse_object(val) for val in values]
    for thorns in parsed:
        if 'x' not in thorns:
            raise ValueError("Invalid syntax: every object in 'thorns' section should has 'x' parameter")
        if 'y' not in thorns:
            raise ValueError("Invalid syntax: every object in 'thorns' section should has 'y' parameter")
        x = thorns['x']
        y = thorns['y']
        check_type_valid('x', x, int)
        check_type_valid('y', y, int)
        check_if_point_in_map((x, y), (map_x_size, map_y_size))
        if map[map_y_size-y][x-1]:
            raise ValueError(f"Invalid structure: object 'thorns{(x, y)}' overlaps platform")
        if map_y_size > map_y_size - y + 1 >= 0:
            if not map[map_y_size - y + 1][x-1]:
                raise ValueError(f"Invalid structure: object 'thorns{(x, y)}' float in air, should be placed on platform or on bottom border of map")
    return True


def is_flags_valid(values: List[str], map_x_size:int, map_y_size:int, map:List[List[bool]]):
    flags = {
        "red": False,
        "blue": False
    }
    parsed = [parse_object(val) for val in values]
    for flag in parsed:
        if 'x' not in flag:
            raise ValueError("Invalid syntax: every object in 'flag' section should has 'x' parameter")
        if 'y' not in flag:
            raise ValueError("Invalid syntax: every object in 'flag' section should has 'y' parameter")
        if 'color' not in flag:
            raise ValueError("Invalid syntax: every object in 'flag' section should has 'color' parameter")
        x = flag['x']
        y = flag['y']
        color = flag["color"]
        if color not in flags:
            raise ValueError(f"Invalid value: parameter 'color' for object 'flag' should be 'blue' or 'red', get {color}")
        if flags[color]:
            raise ValueError(f"Invalid structure: repeated object 'flag' with 'color'='{color}'")
        check_type_valid('x', x, int)
        check_type_valid('y', y, int)
        check_if_point_in_map((x, y), (map_x_size, map_y_size))
        if map[map_y_size - y][x-1]:
            raise ValueError(f"Invalid structure: object 'flag{(x, y)}' overlaps platform")
        if map_y_size > map_y_size - y + 1 >= 0:
            if not map[map_y_size - y + 1][x-1]:
                raise ValueError(f"Invalid structure: object 'flag{(x, y)}' float in air, should be placed on platform or on bottom border of map")
        flags[color] = True
    return flags['blue'] and flags['red']


def is_valid(file_content):
    state = "KEY"
    sections = {}
    key = None
    section = []
    for line in file_content:
        line = line.strip()
        if line == "":
            continue
        if state == "READING":
            if line.startswith("-"):
                section.append(line[1:].strip())
            else:
                sections[key] = section.copy()
                section = []
                state = "KEY"
        if state == "KEY":
            if line.endswith(":"):
                key = line[:-1]
                if key not in ("name", "sizes", "platforms", "thorns", "flags"):
                    raise ValueError(f"Invalid syntax: unexpected key: '{key}'")
                if key in sections:
                    raise ValueError(f"Invalid syntax: repeating key: '{key}'")
                state = "READING"
            else:
                raise ValueError("Invalid syntax: expected key ending with ':'")
    sections[key] = section.copy()

    if "name" not in sections:
        raise ValueError("Invalid structure: key 'name' wasn't found")
    if is_name_valid(sections["name"]):
        pass
    if "sizes" not in sections:
        raise ValueError("Invalid structure: key 'sizes' wasn't found")
    valid, x, y = is_sizes_valid(sections["sizes"])
    if valid:
        map = [[False for __ in range(x)] for _ in range(y)]
        if "platforms" in sections:
            valid = is_platforms_valid(sections["platforms"], x, y, map)
            if valid:
                pass
        if "thorns" in sections:
            if is_thorns_valid(sections['thorns'], x, y, map):
                pass
        if "flags" not in sections:
            raise ValueError("Invalid structure: key 'flags' wasn't found")
        if is_flags_valid(sections['flags'], x, y, map):
            pass
    return True


def from_file(path) -> gmap.Map:
    with open(path, encoding="UTF-8") as file:
        lines = list(file.readlines())
        if is_valid(lines):
            return parse_map(lines)


if __name__ == "__main__":
    mp = from_file(f"{config.INSTANCE.maps}/default.ctfmap")
    print(f"Name: {mp.name['ru']}")
    print(f"Sizes: {mp.sizes['x']}x{mp.sizes['y']}")
    print("Map:")
    mp.printmap()