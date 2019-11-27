from controller.MirrorMirror import *
from threading import Thread

class FadeCandyController: 

    def __init__(self):
        print('init!')
        timestamp = datetime.now()
        thread = Thread(target = initializeMirror)
        thread.start()

    def mapRange(self,value, low1, high1, low2, high2) :
        return low2 + (high2 - low2) * (value - low1) / (high1 - low1)

    def getSide(self,input):
        if "top" == input:
            return 1
        if "right" == input:
            return 2
        if "left" == input:
            return 0

    def clear(self): 
        print('from fadecontroller: clear the mirror!')

#CreateWave(3,1,10,2,(0,250,0))
#def PointLight(position,r,g,b,fadeTime):
    def thumb_control(self, thumbControlCommand):
        
        h = thumbControlCommand.rgb.strip('#')
        rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        
        #print(rgb)

        light = self.mapRange(thumbControlCommand.position , 1, 100, 0, LIGHTS)
        if thumbControlCommand.side == "right":
            light = LIGHTS - light
        side = self.getSide(thumbControlCommand.side)
        print("light: " + str(light) + " side: " + str(side) + " lights: " + str(LIGHTS))
        multiplier = 400.0/255.0
        mode = thumbControlCommand.mode
        index = int(light + (side * LIGHTS))
        r = rgb[0] * multiplier
        g = rgb[1] * multiplier
        b = rgb[2] * multiplier
        if mode == "dot":
            PointLight(index, r,g,b,thumbControlCommand.ttl)
        elif mode == "burst":
            CreateWave(index,4,5,2,(r,g,b))
        elif mode == "pulse":
            CreateWave(index,15,2,2,(r,g,b))
            CreateWave(index,-15,2,2,(r,g,b))

        print('side: ' + thumbControlCommand.side)
        print('position: ' + str(thumbControlCommand.position))
        #print('mode: ' + thumbControlCommand.mode)
        #print('ttl: ' + str(thumbControlCommand.ttl))
        #print('rgb: ' + thumbControlCommand.rgb)