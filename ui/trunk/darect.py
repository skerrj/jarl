#
# core view
#
#~ import pygame
#~ from pygame.locals import *
from types import *
#~ from scenegraph import *

class DaRect:
    def __init__(self):
        self.pos=(0, 0)
        self.dims=(32, 32)
    def GetPos(self):
        return self.pos() if isinstance(self.pos,  FunctionType) else self.pos
    def GetDims(self):
        return self.dims() if isinstance(self.dims,  FunctionType) else self.dims
    def HitTest(self,  mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        pos = self.GetPos()
        dims =self.GetDims()
        x1 = pos[0]
        x2 = pos[0]+ dims[0]
        y1 = pos[1]
        y2 = pos[1]+ dims[1]
        if x >= x1 and x <= x2 and \
           y >= y1 and y <= y2:
            return True
        else:
            return False
#~ class View(object):
    #~ def __init__(self, name='aView'):
        #~ self.name = name
        #~ self.rect = None
        #~ self.text = ''
        #~ self.color=(255,255,255, 255*0.2)
        #~ self.boarder=2
        #~ self.boarder_color=(0,0,0,255)
        #~ self.children = []
    #~ def processEvents(self,  events):
        #~ return
    #~ def addChild(self, view):
        #~ global SCENEGRAPH
        #~ self.children.append(view.name)
        #~ SCENEGRAPH.add(view)
