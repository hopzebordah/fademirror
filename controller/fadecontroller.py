from controller.MirrorMirror import *

class FadeCandyController: 

    def __init__(self):
        print('init!')

    def thumb_control(self, thumbControlCommand):
        print('side: ' + thumbControlCommand.side)
        print('position: ' + int(thumbControlCommand.position))
        print('mode: ' + thumbControlCommand.mode)
        print('ttl: ' + int(thumbControlCommand.ttl))
        print('rgb: ' + int(thumbControlCommand.rgb))