#teaching is all about projects

from msilib import text
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UITextEntryLine, UILabel, UIHorizontalSlider
from threading import Thread
import sys
import colorsys
import math
pygame.init()

simSubsteps = 10
radius = 25
frames = 60
dt = 1/frames
timeStep = dt/simSubsteps
gravity = (0,981)
particleList = []
gravitationalMode = True
forceMode = True
colliderSubSteps = 8
xLength = 1000
yLength = 900
gridSpacingX = int(xLength/(radius*2))
gridSpacingY = int(yLength/(radius*2))
global nmbreParticules,displayOfRot

#clase particules
#rqjouter regex pr check init
class particle:
    def __init__(self,initPos,charge,initSpeed=[0,0],static=False,color = (255, 80, 80),colorHueSpeed = 1000,radiusOwn = radius,weight = 0.01):
        self.static = static
        self.initPos = initPos
        self.lastPos = substraction(initPos,initSpeed)
        self.charge = charge
        self.radius = radiusOwn
        self.pos = initPos
        self.initSpeed = initSpeed
        self.accVector = [0,0]
        particleList.append(self)
        self.color = color
        self.colorStep = 0
        self.colorHueSpeed = colorHueSpeed
        self.weight = weight
    def returnPos(self):
        return [self.initPosX,self.initPosY]
    def returnCharge(self):
        return self.charge
    def move(self,newPos):
        self.pos[0],self.pos[1] = newPos[0],newPos[1]
    def propCacheAdd(self,vector):
        self.accVector[0],self.accVector[1] = addition(self.accVector,scaling(vector,1/self.weight))
    def propCacheReturn(self):
        return self.accVector
    def updatePosition(self,dt):
        if not(self.static):
            self.speedVector = substraction(self.pos,self.lastPos)
            self.lastPos = self.pos
            self.pos = addition(addition(self.pos,self.speedVector),scaling(self.accVector,dt*dt))
            self.accVector[0],self.accVector[1] = 0,0
        else:
            self.pos = self.initPos.copy()
    def setCharge(self,newCharge):
        self.charge = newCharge
    def resetAcc(self):
        self.accVector[0],self.accVector[1] = 0,0
    def colorUp(self):
        num_steps = self.colorHueSpeed
        hue = self.colorStep
        step_val = 1.0 / num_steps
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        hue += step_val
        hue %= 1.0 # cap hue at 1.0
        r = round(rgb[0] * 255)
        g = round(rgb[1] * 255)
        b = round(rgb[2] * 255)
        rgb_ints = (r, g, b)
        self.colorStep = hue
        self.color = rgb_ints


#fonctions

# def refreshLabel():
#     global nmbreParticules,displayOfRot
#     while True:
#         if len(particleList)!=0:
#             nmbreParticules = len(particleList)
#         else :nmbreParticules = 0
#         displayOfRot.config(text = str(nmbreParticules)+" particules")


def normalise(vector):
    if vector[0] == vector[1] == 0:
        return [0,0]
    lenght = math.sqrt((vector[0]**2)+(vector[1]**2))
    return [vector[0]/lenght,vector[1]/lenght]
def substraction(vector1,vector2):
    return [vector1[0]-vector2[0],vector1[1]-vector2[1]]
def addition(vector1,vector2):
    return [vector1[0]+vector2[0],vector1[1]+vector2[1]]
def scaling(vector,scalar):
    return [vector[0]*scalar,vector[1]*scalar]

# def organise():
#     grid ={}
#     for i in range(gridSpacingX):
#         for j in range(gridSpacingY):
#             grid[(i,j)] = []
#     for particule in particleList:
#         for m in range(gridSpacingX):
#             if m*radius<=particule.pos[0]<radius*(m+1):
#                 xIndex = m
#                 break
#         for n in range(9):
#             if radius*n<=particule.pos[1]<radius*(n+1):
#                 yIndex = n
#                 break
#         grid[(m,n)].append(particule)
#     return grid
def organise():
    grid = {}
    for i in range(gridSpacingX):
        for j in range(gridSpacingY):
            grid[(i, j)] = []
    
    for particle in particleList:
        xIndex = int(particle.pos[0] // (radius * 2))
        yIndex = int(particle.pos[1] // (radius * 2))
        xIndex = min(max(xIndex, 0), gridSpacingX - 1)
        yIndex = min(max(yIndex, 0), gridSpacingY - 1)
        grid[(xIndex, yIndex)].append(particle)
    
    return grid

def checkCollision(objectA,objectB):
    distx = (objectA.pos[0]-objectB.pos[0])
    disty = (objectA.pos[1]-objectB.pos[1])
    dist = math.sqrt((distx**2)+(disty**2))
    if dist<(objectA.radius+objectB.radius):
        colVector = normalise((distx,disty))
        correctionDist = (objectA.radius+objectB.radius-dist)/2
        correctionVect = scaling(colVector,correctionDist)
        objectA.move((objectA.pos[0]+correctionVect[0],objectA.pos[1]+correctionVect[1]))
        objectB.move((objectB.pos[0]-correctionVect[0],objectB.pos[1]-correctionVect[1]))

def collider():
    grid = organise()
    for lurkin in range(colliderSubSteps):
        for i in range(gridSpacingX):
            #if i == 0 or i == gridSpacingX-1:
            #    continue
            for j in range(gridSpacingY):
                #if j == 0 or j == gridSpacingY-1:
                #    continue
                if grid[(i,j)] != []:
                    for particle in grid[(i,j)]:
                        for other in grid[(i,j)]:
                            if other!=particle:
                                checkCollision(particle,other)
                        gridCircle = [(i+x, j+y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
                        for index in gridCircle:
                            if index in grid:
                                for other in grid[index]:
                                    checkCollision(particle,other)
        grid = organise()
    constraintEffect(grid)
                        
        
def forceEffect():
    cacheList = particleList.copy()
    for particle in cacheList:
        cacheList.remove(particle)
        for other in cacheList:
            distx = (other.pos[0]-particle.pos[0])
            disty = (other.pos[1]-particle.pos[1])
            if distx == disty == 0:
                dist = 0.0001
            else:
                dist = math.sqrt((distx**2)+(disty**2))
            propVector = normalise((distx,disty))
            propVector = (other.returnCharge()*particle.returnCharge()*propVector[0]/(dist),other.returnCharge()*particle.returnCharge()*propVector[1]/(dist))
            if gravitationalMode:
                particle.propCacheAdd(propVector)
                other.propCacheAdd((-propVector[0],-propVector[1]))
            else:
                other.propCacheAdd(propVector)
                particle.propCacheAdd((-propVector[0],-propVector[1]))

def gravityEffect():
    for particle in particleList:
        particle.propCacheAdd(gravity)
                
def constraintEffect(grid):
    topBottom = [(x,y) for x in range(gridSpacingX) for y in [0,gridSpacingY-1]]
    leftRight = [(x,y) for x in [0,gridSpacingX-1] for y in range(gridSpacingY)]
    for indice in leftRight:
        if grid[indice]!=[]:
            for particle in grid[indice]:
                if particle.pos[0]+particle.radius > xLength:
                    particle.move((xLength-particle.radius,particle.pos[1]))
                if particle.pos[0]-particle.radius < 0:
                    particle.move((0+particle.radius,particle.pos[1]))
    for indice in topBottom:
        if grid[indice]!=[]:
            for particle in grid[indice]:
                if particle.pos[1]+particle.radius > yLength:
                    particle.move((particle.pos[0],yLength-particle.radius))
                if particle.pos[1]-particle.radius < 0:
                    particle.move((particle.pos[0],particle.radius))



#init
screen = pygame.display.set_mode((xLength,yLength))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((xLength, yLength))

####### #     BOUTONS
particleAdd = UIButton(
	relative_rect=pygame.Rect(900, 000, 100, 30),
	text='add particle',
	manager=manager
)


######### SLIDERS
sliderCharge = UIHorizontalSlider(
    pygame.Rect((750,
    30),(240, 25)), 400, (0, 96000),
    manager = manager
)

########## infos
# displayOfRot = UILabel(
# 	    relative_rect=pygame.Rect(750, 620, 250, 100),
# 	    text="0 particules",
# 	    manager=manager
#     )
# Thread(target=refreshLabel).start()

statParticle = particle([400,450],400,[0,0],True,(30,0,210),1)
#statParticle2 = particle((600,450),400,(0,0),True,(30,0,210))
#run
time = 0
while True:
    time_delta = clock.tick(frames)
    ######################    partie bouttons(réactions)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == particleAdd:
                particle([400,200],7,[2,0.5])
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == sliderCharge:
                statParticle.setCharge(event.value)
                #statParticle2.setCharge(event.value)
        manager.process_events(event)
    manager.update(time_delta/1)

       ######################    partie dessins et update des vars
    if forceMode:forceEffect()
    if gravitationalMode:gravityEffect()
    for gazou in range(simSubsteps):
        collider()
        for particule in particleList:
            particule.updatePosition(timeStep)
    time = time + dt
    #bck grnd
    pygame.draw.rect(screen, (125, 123, 15), pygame.Rect(0, 0, xLength, yLength))
    #affichage
    ####
    #particles
    for particule in particleList:
        pygame.draw.circle(screen,(particule.color),particule.pos,particule.radius)
        #particule.colorUp()
    
    ####

    ###############################  affichage 
    manager.draw_ui(screen)
    pygame.display.flip()