
#!/usr/bin/env python

from random import random
import controller.opc as opc
import time
from datetime import datetime
import keyboard 
import math

#a light on the led strip
class Light:
    def __init__(self, r,g,b, fadeTime = 5):
         self.r = r
         self.g = g
         self.b = b
         self.fadeTime = fadeTime
         if self.fadeTime == False:
             self.fadeTime = 3
         self.startColor = (r,g,b)

    def __add__(self, o): 
        self.r += o.r
        self.g += o.g
        self.b += o.b
        return self


    #updates the lights brightness to fade out over the specified time
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




#handles a wave running through the mirror
class Wave:
    def __init__(self, position,speed,width,fadeRadius,color, fadeTime = 3):
         self.position = position
         self.speed = speed
         self.width = width
         self.fadeRadius = fadeRadius
         self.color = color
         self.fadeTime = fadeTime
         self.startTime = fadeTime

    
def clear():
    global pointLights
    global waveLights
    pointLights = [Light(0,0,0,0)] * (LIGHTS * STRANDS)
    waveLights = [Light(0,0,0,0)] * (LIGHTS * STRANDS)
    waves.clear()



#an array containing the current wave objects
waves = []

#updates the waves position depending over time. called every frame 
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

         
     
            
    
        #fade out lights over given time
         fadeFactor = elapsedTime/wave.fadeTime

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


            

        


    


   
#updates the Lights brightness
def PointLightUpdate(elapsedTime):
    for i in range(len(pointLights)):
        pointLights[i].update(elapsedTime)



#--------------------------USER CALLED FUNCTIONS------
#these functions can be called to add lights or waves to the mirror
def PointLight(position,r,g,b,fadeTime):
        pointLights[position] = Light(r,g,b,fadeTime)

def CreateWave(position,speed,width,fadeRadius,color):
    waves.append(Wave(position,speed,width,fadeRadius,color))
#-----------------------------------------------------


#globals
deltaTime = 0.0
timestamp = datetime.now()

# constants
STRANDS = 4
LIGHTS = 35
MAIN_SPEED = 0.1
MAX_LIGHT = 400

#GLOBAL LISTS FOR LAYERING
pointLights = [Light(0,0,0,0)] * (LIGHTS * STRANDS)
waveLights = [Light(0,0,0,0)] * (LIGHTS * STRANDS)


client = opc.Client('localhost:7890') #opc is always on this address

rainbows = []


#initializes the mirror, then infinitely loops over and over to add all the colors at current position together
def initializeMirror():
    frequency = 0.3



    #INITIALZIE MIRROR--------
    #for future use, creates an array of rainbow colors
    for i in range (0,32):
        red   = math.sin(frequency*i + 0) * 127 + 128
        green = math.sin(frequency*i + 2) * 127 + 128
        blue  = math.sin(frequency*i + 4) * 127 + 128

        rainbows.append((red,green,blue))




    timestamp = datetime.now()
  


    #initialize lights list
    for i in range(len(pointLights)):    
        pointLights[i] = Light(0,0,0,0)

   
 
    #-----------------------------


    #MIRROR UPDATE LOOP
    while True:

        

        # calculate elapsed time
        newTime = datetime.now()
        elapsedTime = newTime - timestamp
        timestamp = newTime
        elapsedTime = elapsedTime.microseconds / 1000000

        #Update all lights this frame
        WaveUpdate(elapsedTime)
        PointLightUpdate(elapsedTime)

     


        #FINAL CONVERSION - adds all light layers on top of each other
        finalColors = [(0, 0, 0)] * LIGHTS * STRANDS  #this array will hold the final layered colors
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


        #convert to pixels for opc lbrary. opc library takes lights at position 0-64*8. 8 channels and 64 lights on each channel. we must convert depending on our setup
        pixels = [(0, 0, 0)] * 512  
        strand = -1
        for i in range(len(finalColors)):
           
            if i % LIGHTS == 0:
                strand += 1

            #offsets needed because our fadecandy channels were broken. we used channels 1,2,4,5 out of 0-7
            if strand == 0:
                offset = 64 + i #((64 - LIGHTS) * strand) + (64) #extra lights passed because strand was less than channel max, plus 64
            elif strand == 1:
                 offset = 128 + (i - (LIGHTS * strand)) #extra lights passed because strand was less than channel max, plus 64
            elif strand == 2:
                 offset = (64 * 4) + (i - (LIGHTS * strand)) #extra lights passed because strand was less than channel max, plus 64
            elif strand == 3: 
                 offset = (64 * 5) + (i - (LIGHTS * strand)) #extra lights passed because strand was less than channel max, plus 64

            colorNeeded = finalColors[i]
           
            pixels[offset] = (colorNeeded[0],colorNeeded[1],colorNeeded[2])
     

            
         

      

        #send light data to lights
        client.put_pixels(pixels)

        time.sleep(MAIN_SPEED)
