#teaching is all about projects

from msilib import text
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UITextEntryLine, UILabel, UIHorizontalSlider
import sys
import math
pygame.init()
frames = 60
dt = 1/frames
gravity = (0,981)
particleList = []
gravitationalMode = True


#clase particules
#rqjouter regex pr check init
radius = 5
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
        return 0

def collider():
    return 0
        
def forceEffect():
    cacheList = particleList.copy()
    for particle in cacheList:
        cacheList.remove(particle)
        for other in cacheList:
            distx = (other.pos[0]-particle.pos[0])
            disty = (other.pos[1]-particle.pos[1])
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
        if particle.pos[0]+particle.radius > 1000:
            particle.move((1000-particle.radius,particle.pos[1]))
        if particle.pos[0]-particle.radius < 0:
            particle.move((0+particle.radius,particle.pos[1]))
        if particle.pos[1]+particle.radius > 900:
            particle.move((particle.pos[0],900-particle.radius))
        if particle.pos[1]-particle.radius < 0:
            particle.move((particle.pos[0],particle.radius))



#init
screen = pygame.display.set_mode((1000,900))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((1000, 900))

####### #     BOUTONS
particleAdd = UIButton(
	relative_rect=pygame.Rect(900, 000, 100, 30),
	text='add particle',
	manager=manager
)


######### SLIDERS
sliderCharge = UIHorizontalSlider(
    pygame.Rect((750,
    30),(240, 25)), 400, (2, 10000),
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
                particle((300,200),70,(3,0))
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
    #bck grnd
    pygame.draw.rect(screen, (125, 123, 15), pygame.Rect(0, 0, 1000, 900))
    #affichage
    ####
    #particles
    for particule in particleList:
        pygame.draw.circle(screen,(particule.color),particule.pos,particule.radius)
    
    ####

    ###############################  affichage 
    manager.draw_ui(screen)
    pygame.display.flip()
    

