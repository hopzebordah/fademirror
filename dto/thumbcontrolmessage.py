class ThumbControlMessage:

    side = ''
    position = 0
    mode = ''
    ttl = 0
    rgb = 0

    def ThumbControlMessage(self, json):
        self.side = json['side']
        self.position = int(json['position'])
        self.mode = json['mode']
        self.ttl = int(json['ttl'])
        self.rgb = int(json['rgb'])