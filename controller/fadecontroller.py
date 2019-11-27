from controller.MirrorMirror import *

class FadeCandyController: 

    def __init__(self):
        print('init!')

    def thumb_control(self, thumbControlCommand):
        print('side: ' + thumbControlCommand.side)
        print('position: ' + str(thumbControlCommand.position))
        print('mode: ' + thumbControlCommand.mode)
        print('ttl: ' + str(thumbControlCommand.ttl))
        print('rgb: ' + thumbControlCommand.rgb)