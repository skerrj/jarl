#
#
#
import stackless
#import pygame
#from pygame.locals import *

import core

class Renderer:
    def __init__(self):
        self.pg = core.PyGame()
        self.sg = core.SceneGraph()
        self.channel = stackless.channel()
        self.task = stackless.tasklet(self.renderTask)()
    
    def renderView(self,  v):
        self.pg.drawView(v.text, v.x,  v.y, v.width,  v.height,  v.color)
    
    def renderTask(self):
        while (True):
            cmd = self.channel.receive()
            if cmd == 'render':
                self.pg.clearScreen()
                self.pg.clockTick()
                map(self.renderView,  self.sg.getSceneGraph())
                #self.pg.drawView(str(self.pg.clockTick()), 10, 10, w=32)
                #self.pg.drawView('1234567890', 42, 10)
                self.pg.updateScreen()
    
