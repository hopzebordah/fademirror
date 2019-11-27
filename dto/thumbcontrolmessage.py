import json

class ThumbControlMessage:

    def __init__(self):
        self.side = ''
        self.position = 0
        self.mode = ''
        self.ttl = 0
        self.rgb = ''

    def setValues(self, json):
        self.side = json['side']
        self.position = json['position']
        self.mode = json['mode']
        self.ttl = json['ttl']
        self.rgb = json['rgb']