from json import dumps, loads
import os

def serialPoster(data):
    if 'team_name' not in data:
        return

    return dumps(data)

def joiner(fileData, postData):
    if len(postData) and postData not in fileData:
        return fileData + [postData]
    return fileData

def read(fname):
    try:
        with open(fname) as f:
            text = f.read()
            data = loads(text)
            if type(data) == list:
                return data
            else:
                return [data]
    except:
        return []

def write(fname, data):
    if len(data) > 0:
        with open(fname, 'w') as f:
            f.write(dumps(data))
    pass
