from json import dumps, loads
import os
import uuid
import sys
import csv

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

def writeToDir(dirName, data):
    if not os.path.isdir(dirName):
        os.makedirs(dirName)

    fname = str(uuid.uuid1()) + '.json'
    fullPath = os.path.join(dirName, fname)
    write(fullPath, data)

def mapValues(data):
    o = {}
    for k,vlist in data.items():
        v = vlist[0]
        try:
            v2 = v
            if v2.strip().endswith('%'):
                v2 = v2.strip().rpartition('%')[0]
            if v2.strip().endswith('days'):
                v2 = v2.strip().rpartition('days')[0]
            v = float(v2)
        except ValueError:
            pass
        except:
            print "Error!! processing value " + v + ' - ' + sys.exec_info()[0].__str__()

        o[k] = v
    return o


def readDirAsJson(dirName):
    o = []
    for fname in os.listdir(dirName):
        with open(os.path.join(dirName, fname)) as f:
            o.append(loads(f.read()))
    return o

def toCsv(to, data):
    headers = set()
    for d in data:
        headers = headers.union(d.keys())

    key_headers = ['sprint', 'plmt', 'team_name']
    orderedHeaders = [h for h in headers.difference(set(key_headers))]
    for h in key_headers:
        if h in headers:
            orderedHeaders = [h] + orderedHeaders

    w = csv.DictWriter(to, orderedHeaders, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(data)

