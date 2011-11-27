#
#
#
import core
import pygame
from pygame.locals import *

class Renderer:
    def __init__(self,  sceneGraph,  rootView):
        self.pg = core.PyGame()
        self.sg = sceneGraph
        self.rootView = rootView
        self.running = True
        
    def renderView(self,  z):
        self.pg.drawView(z.text, z.pos[0],  z.pos[1], z.dims[0],  z.dims[1],  z.color)
    
    def render(self):
        self.pg.clearScreen()
        self.pg.clockTick()
        map(self.renderView,  self.sg.getSceneGraph())
        self.pg.updateScreen()
    
    def handleEvents(self):
        events = self.pg.getEvents()
        if pygame.QUIT in events:
            self.running = False
        else:
            self.rootView.handleEvents(events)
    
    def mainLoop(self):
        while (self.running):
            self.handleEvents()
            self.render()
