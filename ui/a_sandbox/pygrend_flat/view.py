#

import sys

import core

import pygame
from pygame.locals import *

from types import *

class RootView:
    def __init__(self, 
                 sceneGraph):
        self.sceneGraph = sceneGraph
        self.children = []
        
    def addChild(self,  view):
        self.children.append(view)
    
    def handleEvents(self,  events):
        for view in self.children:
            view.handleEvents(events)

class BaseView:
    def __init__(self, 
                 sceneGraph,
                 zect):
        self.sceneGraph = sceneGraph
        self.zect = zect
        self.lastx, self.lasty = (0, 0)
        self.children = []
        self.initView()
        
    def initView(self):
        self.sceneGraph.graph.append(self.zect)
    
    def addChild(self,  view):
        self.children.append(view)
    
    def hitTest(self):
        x = self.lastx
        y = self.lasty
        pos =self.zect.pos() if isinstance(self.zect.pos,  FunctionType) else self.zect.pos
        dims =self.zect.dims() if isinstance(self.zect.dims,  FunctionType) else self.zect.dims
        x1 = pos[0]
        x2 = pos[0]+ dims[0]
        y1 = pos[1]
        y2 = pos[1]+ dims[1]
        if x >= x1 and x <= x2 and \
           y >= y1 and y <= y2:
            return True
        else:
            return False
    
    def handleEvents(self,  events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.lastx, self.lasty = event.pos
            elif ( event.type == pygame.NOEVENT):
                pass
        for view in self.children:
            view.handleEvents(events)

class XSliderView(BaseView):
    def __init__(self, 
                 sceneGraph,
                 zect, 
                 views):
        BaseView.__init__(self,  sceneGraph, zect)
        self.leftdown = False
        self.leftView = views[0]
        self.rightView = views[1]
    
    def handleEvents(self,  events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                dX = event.pos[0] - self.lastx
                self.lastx, self.lasty = event.pos
                if (self.leftdown):
                    self.zect.pos = (self.zect.pos[0]+dX,  self.zect.pos[1])
                    self.leftView.zect.dims = (self.leftView.zect.dims[0]+dX, self.leftView.zect.dims[1])
                    self.rightView.zect.dims = (self.rightView.zect.dims[0]-dX, self.rightView.zect.dims[1])
                    self.rightView.zect.pos = (self.rightView.zect.pos[0]+dX, self.rightView.zect.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hitTest(): # left mouse down
                    self.leftdown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left mouse up
                    self.leftdown = False
            elif ( event.type == pygame.NOEVENT):
                pass

class ToolBar(BaseView):
    def __init__(self, 
                 sceneGraph, 
                 parentViewZect):
            zect = self.initToolBarZect(parentViewZect)
            BaseView.__init__(self,  sceneGraph, zect)
            self.leftdown = False
    
    def initToolBarZect(self,  parentViewZect):
        toolbarZect = core.Zect(
                                  id = parentViewZect.id + 'toolbar',
                                  pos = lambda: (parentViewZect.pos[0]+2, parentViewZect.pos[1]+2), 
                                  dims = lambda: (parentViewZect.dims[0]-4,  12),  
                                  color=(0,0,0, 255))
        return toolbarZect
    
    def handleEvents(self,  events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.lastx, self.lasty = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hitTest(): # left mouse down
                    self.leftdown = True
                    print 'toolBar leftdown'
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left mouse up
                    self.leftdown = False
            elif ( event.type == pygame.NOEVENT):
                pass

class ViewView(BaseView):
    def __init__(self, 
                 sceneGraph, 
                 zect):
            BaseView.__init__(self,  sceneGraph, zect)
            self.toolBar = ToolBar(sceneGraph,  zect)
            self.addChild(self.toolBar)
    
    def updateToolBar(self):
        self.toolBar.updateToolBar(self.zect)
