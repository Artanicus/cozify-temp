import json, os

from . import config

# init XDG path to store in
dump_file = config._initXDG('cozify-temp') + 'cache.json'

# dump provided sensor cache data to a file
def dump(sensors):
    global dump_file
    if len(sensors) > 0:
        with open(dump_file, 'w') as fh:
            json.dump(sensors, fh)
            return True
    else:
        return False

def read():
    global dump_file
    if exists():
        with open(dump_file, 'r') as fh:
            return json.load(fh)
    else:
        return None

def clear():
    global dump_file
    if exists():
        os.unlink(dump_file)
        return True
    else:
        return False

def flush():
    out = read()
    clear()
    return out

def exists():
    global dump_file
    return os.path.isfile(dump_file)