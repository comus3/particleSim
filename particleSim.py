#teaching is all about projects

from msilib import text
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UITextEntryLine, UILabel, UIHorizontalSlider
import sys
import math
pygame.init()

radius = 20
frames = 60
dt = 1/frames
gravity = (0,981)
particleList = []
gravitationalMode = True
colliderSubSteps = 6
xLength = 1000
yLength = 900
gridSpacingX = xLength/radius
gridSpacingY = yLength/radius
circlePos = [0,-1,1,-9,9,10,-10,8,-8]
topPos = [0,-1,1,9,8,10]
botPos = [0,-1,1,-9,-8,-10]
leftPos = [0,1,9,10,-9,-8]
rightPos = [0,-1,9,-9,8,-10]

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
        


#fonctions
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
    grid =[]
    for i in range(90):
        grid.append([])
    for particule in particleList:
        for n in range(10):
            if 100*n<=particule.pos[0]<100*(n+1):
                xIndex = n
                break
        for m in range(9):
            if 100*m<=particule.pos[1]<100*(m+1):
                yIndex = m
                break
        j,k = str(n),str(m)
        grid[int(k+j)].append(particle)
    return grid

def checkCollision(objectA,objectB):
    distx = (objectA.pos[0]-objectB.pos[0])
    disty = (objectA.pos[1]-objectB.pos[1])
    dist = math.sqrt((distx**2)+(disty**2))
    if dist<(objectA.radius+objectB.radius):
        colVector = normalise((distx,disty))
        correctionDist = (dist-(objectA.radius+objectB.radius))/2
        correctionVect = scaling(colVector,correctionDist)
        objectA.move((objectA[0]-correctionVect[0],objectA[1]-correctionVect[1]))
        objectB.move((objectB[0]+correctionVect[0],objectB[1]+correctionVect[1]))

def collider():
    def check(indexes):
        for particle in grid[i]:
            for index in indexes:
                if grid[i+index] != []:
                    for other in grid[i+index]:
                        if other != particle:
                            checkCollision(particle,other)
    grid = organise()
    for steps in range(colliderSubSteps):
        for i in range(90):
            if grid[i] != []:
                if 0<i<9:
                    check(topPos)
                elif i%9==0:
                    check(rightPos)
                elif i%10 == 0:
                    check(leftPos)
                elif 81<i<89:
                    check(botPos)
                elif i == 0:
                    check([0,1,9])
                elif i == 8:
                    check([0,-1,9])
                elif i == 81:
                    check([0,1,-9])
                elif i == 89:
                    check([0,-1,-9])
                else:
                    check(circlePos)

                





        
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
    30),(240, 25)), 400, (2, 13000),
    manager = manager
)

########## infos


displayOfRot = UILabel(
	    relative_rect=pygame.Rect(750, 620, 250, 100),
	    text=str("Couleurs"),
	    manager=manager
    )

statParticle = particle((400,450),400,(0,0),True,(30,0,210),20)
#run
while True:
    time_delta = clock.tick(frames)
    
    ######################    partie bouttons(réactions)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == particleAdd:
                particle((300,200),0,(3,0))
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == sliderCharge:
                statParticle.setCharge(event.value)
        manager.process_events(event)
    manager.update(time_delta/1)

       ######################    partie dessins et update des vars
    forceEffect()
    gravityEffect()
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