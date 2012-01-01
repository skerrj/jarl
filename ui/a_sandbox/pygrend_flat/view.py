#

import sys

import core

import pygame
from pygame.locals import *

from types import *

class RootView:
    def __init__(self, sceneGraph):
        self.sceneGraph = sceneGraph
        self.children = []
        
    def addChild(self,  view):
        self.children.append(view)
    
    def handleEvents(self,  events):
        for view in self.children:
            view.handleEvents(events)

class BaseView:
    def __init__(self, sceneGraph,zect):
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
    def __init__(self, sceneGraph, zect, views):
        BaseView.__init__(self,  sceneGraph, zect)
        self.leftDown = False
        self.leftView = views[0]
        self.rightView = views[1]
    
    def handleEvents(self,  events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                dX = event.pos[0] - self.lastx
                self.lastx, self.lasty = event.pos
                if (self.leftDown):
                    self.zect.pos = (self.zect.pos[0]+dX,  self.zect.pos[1])
                    self.leftView.zect.dims = (self.leftView.zect.dims[0]+dX, self.leftView.zect.dims[1])
                    self.rightView.zect.dims = (self.rightView.zect.dims[0]-dX, self.rightView.zect.dims[1])
                    self.rightView.zect.pos = (self.rightView.zect.pos[0]+dX, self.rightView.zect.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hitTest(): # left mouse down
                    self.leftDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left mouse up
                    self.leftDown = False
            elif ( event.type == pygame.NOEVENT):
                pass

class Button(BaseView):
    def __init__(self,  sceneGraph,  parentZect,  posDimsPair,  name ='button'):
        pos = posDimsPair[0]
        dims = posDimsPair[1]
        zect = core.Zect(id = parentZect.id + name, 
                                            pos = pos, 
                                            dims = dims)
        BaseView.__init__(self,  sceneGraph,  zect)
        self.leftDown = False
        self.leftClick = lambda: 1
    def handleEvents(self,  events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.lastx, self.lasty = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hitTest(): # left mouse down
                    self.leftDown = True
                    print self.zect.id, 'leftDown'
                    self.leftClick()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left mouse up
                    self.leftDown = False
            elif ( event.type == pygame.NOEVENT):
                pass

class BaseToolBar(BaseView):
    def __init__(self, sceneGraph, parentZect,  name = 'toolBar'):
            zect = core.Zect(
                                  id = parentZect.id + name,
                                  pos = lambda: (parentZect.pos[0]+2, parentZect.pos[1]+2), 
                                  dims = lambda: (parentZect.dims[0]-4,  12),  
                                  color=(0,0,0, 255))
            BaseView.__init__(self,  sceneGraph, zect)
            hPosDimsPair = (lambda: (parentZect.pos[0]+4, parentZect.pos[1]+3), (10, 10))
            self.splitHButton = Button(sceneGraph,  zect, hPosDimsPair,  name = 'splitHButton')
            self.addChild(self.splitHButton)
            vPosDimsPair = (lambda: (parentZect.pos[0]+4+12, parentZect.pos[1]+3), (10, 10))
            self.splitVButton = Button(sceneGraph,  zect, vPosDimsPair,  name = 'splitVButton')
            self.addChild(self.splitVButton)
            self.leftDown = False
    
    def handleEvents(self,  events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.lastx, self.lasty = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hitTest(): # left mouse down
                    self.leftDown = True
                    print self.zect.id, 'leftDown'
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left mouse up
                    self.leftDown = False
            elif ( event.type == pygame.NOEVENT):
                pass
        for view in self.children:
            view.handleEvents(events)

class ViewView(BaseView):
    def __init__(self, sceneGraph, zect,  rv,  sX,  b):
        BaseView.__init__(self,  sceneGraph, zect)
        self.toolBar = BaseToolBar(sceneGraph,  zect)
        self.toolBar.splitHButton.leftClick = lambda: self.splitViewH()
        self.addChild(self.toolBar)
        self.rootView = rv
        self.sX = sX
        self.b = b
    def splitViewH(self):
        z = self.zect
        posX,  posY = z.pos
        dimX, dimY = z.dims
        dimX = ((dimX+2*self.b)/2 - (self.sX/2) - (2*self.b))
        z.dims = (dimX,  dimY)
        nPosX = dimX + self.sX + 2*self.b + posX
        rv = ViewView(
                        self.sceneGraph, 
                        core.Zect(id='rv',  pos=(nPosX, posY), dims=z.dims), 
                        self.rootView,  self.sX,  self.b)
        self.rootView.addChild(rv)
