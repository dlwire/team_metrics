from json import dumps

def serialPoster(data):
    if 'team_name' not in data:
        return

    return dumps(data)

def joiner(fileData, postData):
    if len(postData) and postData not in fileData:
        return fileData + [postData]
    return fileData
