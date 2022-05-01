import json


class ServerRequest():
    def __init__(self, actions=[], msg_id=1, session=""):
        self.head = {}
        self.head['msgId'] = msg_id
        self.head['session'] = session
        self.head['source'] = 'testclient'
        self.head['target'] = 'server'
        self.head['version'] = '1.0'
        self.data = None
        self.actions = actions

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class NodeRequest():
    def __init__(self, fingerprint, authentification, actions=[], uptime=1, logcounter=0, errorcounter=0):
        self.header = {}
        self.header['source'] = 'Test node'
        self.header['version'] = '1.0.0'
        self.header['target'] = "roseguarden.fabba.space"
        self.header['fingerprint'] = fingerprint
        self.header['authentification'] = authentification
        self.header['logcounter'] = logcounter
        self.header['errorcounter'] = errorcounter
        self.header['uptime'] = uptime
        self.data = None
        self.actions = actions

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
