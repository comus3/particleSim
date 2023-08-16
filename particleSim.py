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
gravity = (0,9.81)
particleList = []


#clase particules
#rqjouter regex pr check init
radius = 20
class particle:
    def __init__(self,initPos,charge,initSpeed,color = (255, 80, 80)):
        self.initPos = initPos
        self.lastPos = substraction(initPos,initSpeed)
        self.charge = charge
        self.radius = radius
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
        self.speedVector = substraction(self.pos,self.lastPos)
        self.lastPos = self.pos
        self.pos = addition(addition(self.pos,self.speedVector),scaling(self.accVector,dt*dt))
        self.accVector = (0,0)
        


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
            propVector = (other.returnCharge()*particle.returnCharge()*propVector[0]/(dist**2),other.returnCharge()*particle.returnCharge()*propVector[1]/(dist**2))
            particle.propCacheAdd(propVector)
            other.propCacheAdd((-propVector[0],-propVector[1]))

def gravityEffect():
    for particle in particleList:
        particle.propCacheAdd(gravity)
                
def constraintEffect():
    for particle in particleList:
        if particle.pos[0]-radius > 1000:
            particle.move((1000,particle.pos[1]))
        elif particle.pos[0]+radius < 0:
            particle.move((0,particle.pos[1]))
        elif particle.pos[1]-radius > 900:
            particle.move((particle.pos[0],900))
        elif particle.pos[1]+radius < 0:
            particle.move((particle.pos[0],0))

                    






#init
screen = pygame.display.set_mode((1000,900))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((1000, 900))

####### #     BOUTONS
random_Bouton = UIButton(
	relative_rect=pygame.Rect(900, 000, 100, 30),
	text='Random\nrotation',
	manager=manager
)


######### SLIDERS
sliderMaxD = UIHorizontalSlider(
    pygame.Rect((750,
    30),(240, 25)), 400, (2, 1000),
    manager = manager
)

########## infos


displayOfRot = UILabel(
	    relative_rect=pygame.Rect(750, 620, 250, 100),
	    text=str("Couleurs"),
	    manager=manager
    )

for i in range(10):
    particule = particle((300+2*i,300-i),7,(0,0))
#run
while True:
    time_delta = clock.tick(frames)
    
    ######################    partie bouttons(réactions)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == random_Bouton:
                if randomRotVar:randomRotVar = False
                else:randomRotVar = True
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == sliderMaxD:
                maxDiameterVar = event.value
                tres = True
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
        pygame.draw.circle(screen,(particule.color),particule.pos,radius)
    
    ####

    ###############################  affichage 
    manager.draw_ui(screen)
    pygame.display.flip()
    

