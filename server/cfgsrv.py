import json

def serialize(data, loc):
    with file(loc, 'w') as f:
        json.dump(data, f)

def deserialize(loc):
    try:
        with file(loc) as f:
            return json.load(f)
    except IOError:
        return {}

def dewrapper(loc):
    def f():
        return deserialize(loc)
    return f

def sewrapper(loc):
    def f(data):
        return serialize(data, loc)
    return f

def dict_wrapping(loc):
    return SerializedDict(dewrapper(loc), sewrapper(loc))

class SerializedDict(object):
    def __init__(self, loader, saver):
        self.loader = loader
        self.saver = saver
        self.rep = self.loader()

    def __setitem__(self, key, value):
        self.rep[key] = value
    
    def __getitem__(self, key):
        return self.rep[key]

    def load(self):
        self.rep = self.loader()
         
    def save(self):
        self.saver(self.rep)
