#
#
#
import core
import pygame
from pygame.locals import *
from types import *

class Renderer:
    def __init__(self,  sceneGraph,  rootView):
        self.pg = core.PyGame()
        self.sg = sceneGraph
        self.rootView = rootView
        self.running = True
        
    def renderView(self,  z):
        pos = z.pos() if isinstance(z.pos,  FunctionType) else z.pos
        dims = z.dims() if isinstance(z.dims,  FunctionType) else z.dims
        #print 'renderView:',  z.id,  pos,  dims
        self.pg.drawView(z.text, pos[0],  pos[1], dims[0],  dims[1],  z.color)
    
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
