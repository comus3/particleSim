#teaching is all about projects

from msilib import text
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UITextEntryLine, UILabel, UIHorizontalSlider
from threading import Thread
import sys
import math
pygame.init()

radius = 25
frames = 30
dt = 1/frames
gravity = (0,981)
particleList = []
gravitationalMode = True
colliderSubSteps = 8
xLength = 1000
yLength = 900
gridSpacingX = int(xLength/(radius*4))
gridSpacingY = int(yLength/(radius*3))
global nmbreParticules,displayOfRot

#clase particules
#rqjouter regex pr check init
class particle:
    def __init__(self,initPos,charge,initSpeed,static=False,color = (255, 80, 80),radiusOwn = radius):
        self.static = static
        self.initPos = initPos
        self.lastPos = substraction(initPos,initSpeed)
        self.charge = charge
        self.radius = radiusOwn
        self.pos = initPos
        self.initSpeed = initSpeed
        self.accVector = (0,0)
        particleList.append(self)
        self.color = color
    def returnPos(self):
        return (self.initPosX,self.initPosY)
    def returnCharge(self):
        return self.charge
    def move(self,newPos):
        self.pos = (newPos[0],newPos[1])
    def propCacheAdd(self,vector):
        self.accVector = addition(self.accVector,vector)
    def propCacheReturn(self):
        return self.accVector
    def updatePosition(self):
        if not(self.static):
            self.speedVector = substraction(self.pos,self.lastPos)
            self.lastPos = self.pos
            self.pos = addition(addition(self.pos,self.speedVector),scaling(self.accVector,dt*dt))
            self.accVector = (0,0)
        else:
            self.pos = self.lastPos
    def setCharge(self,newCharge):
        self.charge = newCharge
    def resetAcc(self):
        self.accVector = (0,0)


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
        return (0,0)
    lenght = math.sqrt((vector[0]**2)+(vector[1]**2))
    return (vector[0]/lenght,vector[1]/lenght)
def substraction(vector1,vector2):
    return (vector1[0]-vector2[0],vector1[1]-vector2[1])
def addition(vector1,vector2):
    return (vector1[0]+vector2[0],vector1[1]+vector2[1])
def scaling(vector,scalar):
    return (vector[0]*scalar,vector[1]*scalar)

def organise():
    grid ={}
    for i in range(gridSpacingX):
        for j in range(gridSpacingY):
            grid[(i,j)] = []
    for particule in particleList:
        for m in range(gridSpacingX):
            if m*radius<=particule.pos[0]<radius*(m+1):
                xIndex = m
                break
        for n in range(9):
            if radius*n<=particule.pos[1]<radius*(n+1):
                yIndex = n
                break
        grid[(m,n)].append(particule)
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
    
    for steps in range(colliderSubSteps):
        grid = organise()
        for i in range(gridSpacingX):
            if i == 0 or i == gridSpacingX-1:
                continue
            for j in range(gridSpacingY):
                if j == 0 or j == gridSpacingY-1:
                    continue
                if grid[(i,j)] != []:
                    for particle in grid[(i,j)]:
                        for other in grid[(i,j)]:
                            if other!=particle:
                                checkCollision(particle,other)
                        gridCircle = [(i+1,j),(i-1,j),(i,j+1),(i,j-1),(i-1,j-1),(i+1,j-1),(i+1,j+1),(i-1,j+1)]
                        for index in gridCircle:
                            for other in grid[(index)]:
                                checkCollision(particle,other)
                        
        
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
                
def constraintEffect():
    for particle in particleList:
        if particle.pos[0]+particle.radius > xLength:
            particle.move((xLength-particle.radius,particle.pos[1]))
        if particle.pos[0]-particle.radius < 0:
            particle.move((0+particle.radius,particle.pos[1]))
        if particle.pos[1]+particle.radius > yLength:
            particle.move((particle.pos[0],yLength-particle.radius))
        if particle.pos[1]-particle.radius < 0:
            particle.move((particle.pos[0],particle.radius))



#init
screen = pygame.display.set_mode((xLength,yLength))
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
    30),(240, 25)), 400, (2, 13000),
    manager = manager
)

########## infos
# displayOfRot = UILabel(
# 	    relative_rect=pygame.Rect(750, 620, 250, 100),
# 	    text="0 particules",
# 	    manager=manager
#     )
# Thread(target=refreshLabel).start()

statParticle = particle((400,450),400,(0,0),True,(30,0,210),25)
#run

while True:
    time_delta = dt
    ######################    partie bouttons(réactions)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == particleAdd:
                particle((400,200),70,(10,0))
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == sliderCharge:
                statParticle.setCharge(event.value)
        manager.process_events(event)
    manager.update(time_delta/1)

       ######################    partie dessins et update des vars
    forceEffect()
    #gravityEffect()
    constraintEffect()
    for particule in particleList:
        particule.updatePosition()
    collider()
    
    #bck grnd
    pygame.draw.rect(screen, (125, 123, 15), pygame.Rect(0, 0, xLength, yLength))
    #affichage
    ####
    #particles
    for particule in particleList:
        pygame.draw.circle(screen,(particule.color),particule.pos,particule.radius)
    
    ####

    ###############################  affichage 
    manager.draw_ui(screen)
    pygame.display.flip()
    

#0,1, 2, 3, 4, 5, 6, 7, 8
#9,10,11,12,13,14,15,16,17
#18,19,20,21,22,23,24,25,26
#27,28,29,30,31,32,33,34,35
#36,37,38,39,40,41,42,43,44
#45,46,47,48,49,50,51,52,53
#54,55,56,57,58,59,60,61,62
#63,64,65,66,67,68,69,70,71
#72,73,74,75,76,77,78,79,80
#81,82,83,84,85,86,87,88,89
# 
# #
#
#
#
#
#
#