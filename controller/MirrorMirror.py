
#!/usr/bin/env python


import opc as opc
import time
from datetime import datetime
import keyboard 
import math


class Light:
    def __init__(self, r,g,b, fadeTime):
         self.r = r
         self.g = g
         self.b = b
         self.fadeTime = fadeTime
         self.startColor = (r,g,b)

    def __add__(self, o): 
        self.r += o.r
        self.g += o.g
        self.b += o.b
        return self

    def update(self,elapsedTime):

        #we can set fade time to be less than 0 so we skip the update
        if self.fadeTime <= 0:
            return
        #fade out lights over given time
        fadeFactor = elapsedTime/self.fadeTime
        if self.r > 0:
            self.r -= (self.startColor[0] * fadeFactor)
        else:
            self.r = 0
        if self.g > 0:
            self.g -= (self.startColor[1] * fadeFactor)
        else:
            self.g = 0
        if self.b > 0:
            self.b -= (self.startColor[2] * fadeFactor)
        else: 
            self.b = 0
    
    def normalize(self):
        if self.r < 0:
            self.r = 0
        elif self.r > MAX_LIGHT:
            self.r = MAX_LIGHT
        if self.g < 0:
            self.g = 0
        elif self.g > MAX_LIGHT:
            self.g = MAX_LIGHT
        if self.b < 0:
            self.b = 0
        elif self.b > MAX_LIGHT:
            self.b = MAX_LIGHT
        

    def addLight(self,r,g,b,fadeTime): #add light to the current light. if r is -1 ignore it and use current
         if r != -1:
             self.r = r 
         if g != -1:
             self.g = g 
         if b != -1:
             self.b = b 
         self.startColor[0] = self.r
         self.startColor[1] = self.g
         self.startColor[2] = self.b
         self.fadeTime = fadeTime


#UPDATE FUNCTIONS
wavePositions = [64,128]
waveSpeeds = [1,-3]
waveWidths = [10,5]
waveFadeRadius = [4,1]
waveColors = [(0,0,400),(400,0,0)]


class Wave:
    def __init__(self, position,speed,width,fadeRadius,color):
         self.position = position
         self.speed = speed
         self.width = width
         self.fadeRadius = fadeRadius
         self.color = color

    
        

waves = []
def WaveUpdate(elapsedTime):

    #reset
     for i in range(len(waveLights)):    
        waveLights[i] = Light(0,0,0,0)

     #update each wave position
     for i in range(len(waves)):
        waves[i].position += (waves[i].speed * elapsedTime)

     for i in range(len(waves)):
         wave = waves[i]
         wavePosition = wave.position

        #loop for now, get rid of and make it actulaly loop
         if wavePosition < 0:
            waves[i].position = LIGHTS * STRANDS
         if wavePosition > LIGHTS * STRANDS:
            waves[i].position = 64
        
         #print("index: " + str(i))
         waveColor = wave.color
         radius = wave.width/2
         fadeRadius = wave.fadeRadius
         start = wavePosition - radius #get start of wave
         end = wavePosition + radius # get end of wave
         fadeStart = start + fadeRadius
         fadeEnd = end - fadeRadius
         for x in range(math.ceil(start),math.floor(end) + 1):
            brightPercentage = 1
            if x < fadeStart: #this will not be full blown color but only half filled 
           
                brightPercentage = 1 - ((fadeStart - x)/fadeRadius)
            elif x > fadeEnd:
                brightPercentage = (end - x)/fadeRadius
            #print(x)
            if x >= STRANDS * LIGHTS:
                continue
            if x < 0:
                continue
            #apply the new color
            waveLights[x].r += waveColor[0] * brightPercentage
            waveLights[x].g += waveColor[1] * brightPercentage
            waveLights[x].b += waveColor[2] * brightPercentage
            #print(brightPercentage)


            

        


    


   

def PointLightUpdate(elapsedTime):
    for i in range(len(pointLights)):
        pointLights[i].update(elapsedTime)



#ALEX will call these functions
def PointLight(position,r,g,b,fadeTime):
        pointLights[position] = Light(r,g,b,fadeTime)

def CreateWave(position,speed,width,fadeRadius,color):
    waves.append(Wave(position,speed,width,fadeRadius,color))

#globals
deltaTime = 0.0
timestamp = datetime.now()

# constants
STRANDS = 3
LIGHTS = 35
MAIN_SPEED = 0.1
MAX_LIGHT = 400

#GLOBAL LISTS FOR LAYERING
pointLights = [Light(0,0,0,0)] * (LIGHTS * STRANDS)
waveLights = [Light(0,0,0,0)] * (LIGHTS * STRANDS)


client = opc.Client('localhost:7890')

if __name__ == "__main__":

  
 #def CreateWave(position,speed,width,fadeRadius,color):
    CreateWave(3,1,10,2,(0,250,0))
    CreateWave(3,5,5,2,(300,0,0))
    CreateWave(60,-3,12,2,(0,0,250))
    CreateWave(80,5,5,2,(200,0,400))

#initialize lights list
    for i in range(len(pointLights)):    
        pointLights[i] = Light(0,0,0,0)

   

    while True:
        # calculate elapsed time
        newTime = datetime.now()
        elapsedTime = newTime - timestamp
        timestamp = newTime
        elapsedTime = elapsedTime.microseconds / 1000000

        #call all update functions
        WaveUpdate(elapsedTime)
        PointLightUpdate(elapsedTime)

     


        #FINAL CONVERSION AND UPDATES
        finalColors = [(0, 0, 0)] * LIGHTS * STRANDS  
        for i in range(len(finalColors)):
            

            #merge all of the layers
            addR = 0
            addG = 0
            addB = 0

            #point light layer
            pointLight = pointLights[i]
            addR += pointLight.r
            addG += pointLight.g
            addB += pointLight.b

            #wave light layer
            waveLight = waveLights[i]
            addR += waveLight.r
            addG += waveLight.g
            addB += waveLight.b


            #add to final pixels
            if addR < 0:
                addR = 0
            elif addR > MAX_LIGHT:
                addR = MAX_LIGHT
            if addG < 0:
                addG = 0
            elif addG > MAX_LIGHT:
                addG= MAX_LIGHT
            if addB < 0:
                addB = 0
            if addB > MAX_LIGHT:
                addB = MAX_LIGHT

            finalColors [i] = (addR,addG,addB)


        #convert to pixels
        pixels = [(0, 0, 0)] * 512  
        strand = -1
        for i in range(len(finalColors)):
           
            if i % LIGHTS == 0:
                strand += 1

            if strand == 0:
                offset = 64 + i #((64 - LIGHTS) * strand) + (64) #extra lights passed because strand was less than channel max, plus 64
            elif strand == 1:
                 offset = 128 + (i - (LIGHTS * strand)) #extra lights passed because strand was less than channel max, plus 64
            elif strand == 2:
                 offset = (64 * 4) + (i - (LIGHTS * strand)) #extra lights passed because strand was less than channel max, plus 64
            elif strand == 3: 
                 offset = (64 * 5) + (i - (LIGHTS * strand)) #extra lights passed because strand was less than channel max, plus 64
            #merge all of the layers      
          #convert to pixel tuples
            colorNeeded = finalColors[i]
            print("strand: " + str(strand) + "final color index: " + str(i) + "made to be: " + str(i + offset))
            pixels[offset] = (colorNeeded[0],colorNeeded[1],colorNeeded[2])
     

            
         

      


        client.put_pixels(pixels)

        time.sleep(MAIN_SPEED)
