def parse_value(value):
    if all(character.isdigit() for character in value):
        return int(value)
    return value


def parse_object(object_string):
    obj = {}
    for pair in object_string.split(","):
        key, value = pair.split(":")
        obj[key.strip()] = parse_value(value.strip())
    return obj


def parse_map(file_content):
    state = "START"
    data = {}
    current_key = None

    for line in file_content:
        line = line.strip()
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


def from_file(path):
    with open(path) as file:
        return parse_map(file)