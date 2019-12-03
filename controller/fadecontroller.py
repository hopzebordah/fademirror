#from controller.MirrorMirror import *
import controller.MirrorMirror as lib
from threading import Thread

class FadeCandyController: 

    def __init__(self):
        print('init!')
        lib.timestamp = lib.datetime.now()
        thread = Thread(target = lib.initializeMirror)
        thread.start()


    def mapRange(self,value, low1, high1, low2, high2) :
        return low2 + (high2 - low2) * (value - low1) / (high1 - low1)

    #helps convert JSON side field to int index of light strand
    def getSide(self,input):
        if "top" == input:
            return 1
        if "right" == input:
            return 2
        if "left" == input:
            return 0
        if "bottom" == input:
            return 3

    def clear(self): 
        print('from fadecontroller: clear the mirror!')

    #web server calls this with command object
    def thumb_control(self, thumbControlCommand):
        
        h = thumbControlCommand.rgb.strip('#')
        rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        
        
        #convert server click position to light strand/index
        light = self.mapRange(thumbControlCommand.position , 1, 100, 0, lib.LIGHTS)
        if thumbControlCommand.side == "right" or thumbControlCommand.side == "bottom":
            light = lib.LIGHTS - light
        side = self.getSide(thumbControlCommand.side)
        multiplier = 400.0/255.0
        mode = thumbControlCommand.mode
        index = int(light + (side * lib.LIGHTS))


        #convert color (because leds take a max color)
        r = rgb[0] * multiplier
        g = rgb[1] * multiplier
        b = rgb[2] * multiplier

        #determin mode and call correct function on controller
        if mode == "dot":
            lib.PointLight(index, r,g,b,thumbControlCommand.ttl)
        elif mode == "burst":
            lib.CreateWave(index,4,5,2,(r,g,b))
        elif mode == "pulse":
            lib.CreateWave(index,15,2,2,(r,g,b))
            lib.CreateWave(index,-15,2,2,(r,g,b))
