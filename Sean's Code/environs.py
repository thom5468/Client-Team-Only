#@PydevCodeAnalysisIgnore
import os
import sys
import pygame
from math import pi, cos, sin

ETcolors = { 'U' : (150,150,150), 'F' : (200, 0, 0), 'W' : (50, 150, 50)}
STARTANGLE = pi / 2
UNITANGLE = pi / 8
LINECOLOR = (0,200,0)

class Environ():
    def __init__ (self, center, iradius, oradius, number, type, size, race, resources, creature, politics):
        self.box = pygame.Rect(center[0]-oradius, center[1]-oradius, oradius-iradius, oradius)
        self.number = number
        self.type = type
        self.size = size
        self.race = race
        self.resources = resources
        self.creature = creature
        self.politics = politics
        self.startangle = STARTANGLE+(self.number)
        self.endangle = self.startangle + UNITANGLE
        self.iradius = iradius
        self.oradius = oradius
        self.averadius = (iradius+oradius)/2
        self.center = center
        #self.colliderect = pygame.Rect(,,,)
        self.getcolor(type)
        self.collidepoints = []
        self.updatepoints()
    def getcolor(self, type):
        self.fillcolor = ETcolors[type]
    def shiftdown1  (self):
        self.endangle = self.endangle + UNITANGLE
        self.startangle = self.startangle + UNITANGLE
        self.updatepoints()
    def shiftup1 (self):
        self.endangle = self.endangle - UNITANGLE
        self.startangle = self.startangle - UNITANGLE
        self.updatepoints()
    def expand1 (self):
        self.endangle = self.endangle + UNITANGLE
        self.updatepoints()
        return self.collidepoints[-2]
    def contract1 (self):
        self.endangle = self.endangle - UNITANGLE
        #self.updatepoints()
    def updatepoints (self):
        self.collidepoints = []
        angle = self.startangle
        while angle < self.endangle:
            angle = angle + UNITANGLE/2
            self.collidepoints.add(cos(angle)*(averadius+self.center),sin(angle)*(averadius-self.center))
            angle = angle + UNITANGLE
        self.stacks = len(self.collidepoints)
    def update (self, stacklist):
        self.total = 1
        for stack in stacklist:
            for point in self.collidepoints:
                if stack.rect.collidepoint(point):
                    self.total = self.total + 1
        for i in range(self.stacks-self.total):
            if i > 0:
                self.contract1();
        self.total = self.stacks - self.total
        self.updatepoints()
        for stack in stacklist:
            for point in self.collidepoints:
                if stack.rect.collidepoint(point):
                    stack.pos = point
                    stack.update()
        return self.total #amount of growth/shrinkage
    def draw (self, surface):
        self.startline = pygame.draw.line(surface, self.fillcolor, (self.center[0]+self.oradius*(cos(self.startangle)), self.center[1]-self.oradius*(sin(self.startangle))), (self.center[0]+self.iradius*(cos(self.startangle)), self.center[1]-self.iradius*(sin(self.startangle))), 2)
        self.endline = pygame.draw.line(surface, self.fillcolor, (self.center[0]+self.oradius*(cos(self.endangle)), self.center[1]-self.oradius*(sin(self.endangle))), (self.center[0]+self.iradius*(cos(self.endangle)), self.center[1]-self.iradius*(sin(self.endangle))), 4)
        self.oarc = pygame.draw.arc(surface, self.fillcolor, pygame.Rect(self.box.topleft, (2*self.oradius, 2*self.oradius)), self.startangle, self.endangle+pi/72, 3)
        self.iarc = pygame.draw.arc(surface, self.fillcolor, pygame.Rect(self.box.topleft[0]+(self.oradius-self.iradius), self.box.topleft[1]+(self.oradius-self.iradius), 2*self.iradius, 2*self.iradius), self.startangle, self.endangle + pi/72, 3)
        #for i in self.collidepoints:
            


                
class EnvironBox():
    def __init__(self, planetrect):
        #self.name = name
        self.planet = planetrect
        self.environlist = []
        self.envarc = pygame.Rect(planetrect.topleft[0] - 75, planetrect.topleft[1] - 75, planetrect.width + 150, planetrect.height + 150)
#        self.firstangle = 2*pi/3
#        self.lastangle = 2*pi/3
        
    def addEnviron(self, number, type, size, race, resources, creature, politics):
        self.environlist.append(Environ(self.planet.center, self.planet.width/2 + 50, self.planet.width/2 + 150, number, type, size, race, resources, creature, politics))

    def addstack (self, stack):
        for i in self.environlist:
            for j in i.collidepoints:
                if (stack.rect.collidepoint(j)):
                    stack.loc = i.expand1
                    for k in self.environlist[i.number:]:
                        k.shiftdown1
#        self.lastangle = self.lastangle + UNITANGLE
        
    def update(self, stacklist):
        #self.envarc.collidelist(stacklist)
        for i in self.environlist:
            i.center = self.planet.center
            ret = i.update(stacklist)
            if (ret != 0):
                for j in range(0, ret):
                    for k in self.environlist[i.number:]:
                        if (j<0):
                            k.shiftup1()
                        if (j>0):
                            k.shiftdown1()
#        self.outsideArc = [self.rect, ARCCOLOR, self.rect, self.firstangle, self.lastangle]
#        self.insideArc = [self.rect, ARCCOLOR, self.rect, self.firstangle, self.lastangle]
    
    def draw(self, surface):
        for i in self.environlist:
            i.draw(surface)
    #    pygame.draw.arc(self.outsideArc)
    #    pygame.draw.arc(self.insideArc)
        
