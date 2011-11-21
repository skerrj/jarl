#

import sys
import stackless
import channels.broadcast

import pygrend

#debug
import pygame
from pygame.locals import *

class RootView:
    def __init__(self, 
                 sceneGraph,  
                 eventChannel):
        self.eventChannel = eventChannel
        self.sceneGraph = sceneGraph
        self.childChannel = channels.broadcast.BroadcastChannel()
        self.running = True
        self.task = stackless.tasklet(self.runTask)()
        
    def addChild(self,  view):
        view.eventChannel = self.childChannel
    
    def runTask(self):
        while( self.running ):
            self.route_events()
    
    def route_events(self):
        event = self.eventChannel.receive()
        self.childChannel.send(event)

class BaseView:
    def __init__(self, 
                 sceneGraph, 
                 renderChannel, 
                 zect):
        self.sceneGraph = sceneGraph
        self.eventChannel = None
        self.renderChannel = renderChannel
        self.childChannel = None
        self.running = True
        self.zect = zect
#        self.id = zect.id
#        self.pos = zect.pos
#        self.dims = zect.dims
        self.lastx, self.lasty = (0, 0)
        self.initView()
        #self.task = stackless.tasklet(self.runTask)()
        self.task = None
        
    def initView(self):
        #v = pygrend.Zect(id = self.id,  pos=self.pos,  dims=self.dims)
        self.sceneGraph.graph.append(self.zect)
        self.renderChannel.send('render')
    
    def hitTest(self):
        x = self.lastx
        y = self.lasty
        x1 = self.zect.pos[0]
        x2 = self.zect.pos[0]+ self.zect.dims[0]
        y1 = self.zect.pos[1]
        y2 = self.zect.pos[1]+ self.zect.dims[1]
        if x >= x1 and x <= x2 and \
           y >= y1 and y <= y2:
            return True
        else:
            return False
    
    def scheduleTask(self):
        self.task = stackless.tasklet(self.runTask)()
    
    def setEventChannel(self,  channel):
        self.eventChannel = channel
    
    def addChild(self,  id):
        self.childChannels[id] = stackless.channel()
    
    def runTask(self):
        while( self.running ):
            self.process_events()
    
    def process_events(self):
        event = self.eventChannel.receive()
        if event.type == pygame.MOUSEMOTION:
            self.lastx, self.lasty = event.pos
            #print ( '%s MOUSEMOTION @ (%d, %d)' % (self.zect.id,  event.pos[0],  event.pos[1]))
            #renderChannel.send('render')
        elif ( event.type == pygame.NOEVENT):
            pass
        self.renderChannel.send('render')
    

class XSliderView(BaseView):
    def __init__(self, 
                 sceneGraph, 
                 renderChannel, 
                 zect):
        BaseView.__init__(self,  sceneGraph,  renderChannel,  zect)
        self.leftdown = False
        self.announce = channels.broadcast.BroadcastChannel()
    
    def process_events(self):
        event = self.eventChannel.receive()
        if event.type == pygame.MOUSEMOTION:
            dX = event.pos[0] - self.lastx
            self.lastx, self.lasty = event.pos
            if (self.leftdown):
                self.zect.pos = (self.zect.pos[0]+dX,  self.zect.pos[1])
                self.announce.send((self.zect.id,  dX))
#                self.leftView.zect.dims = (self.leftView.zect.dims[0]+dX, self.leftView.zect.dims[1])
#                self.rightView.zect.dims = (self.rightView.zect.dims[0]-dX, self.rightView.zect.dims[1])
#                self.rightView.zect.pos = (self.rightView.zect.pos[0]+dX, self.rightView.zect.pos[1])
#                self.leftView.updateToolBar()
#                self.rightView.updateToolBar()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hitTest(): # left mouse down
                self.leftdown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # left mouse up
                self.leftdown = False
        elif ( event.type == pygame.NOEVENT):
            pass
        self.renderChannel.send('render')

class ViewView(BaseView):
    def __init__(self, 
                 sceneGraph, 
                 renderChannel, 
                 zect, 
                 announce, 
                 tag):
            BaseView.__init__(self,  sceneGraph,  renderChannel,  zect)
            self.toolBarZect = None
            self.announce = announce
            self.tag = tag
            self.aTask = None
            self.initToolBar()
    def scheduleTask(self):
        BaseView.scheduleTask(self)
        self.aTask = stackless.tasklet(self.announceTask)()
    def announceTask(self):
        while( self.running ):
            self.process_annoucements()
    def process_annoucements(self):
        cmd = self.announce.receive()
        if cmd[0] == 'slider':
            dX = cmd[1]
            if self.tag == 'left':
                self.zect.dims = (self.zect.dims[0]+dX, self.zect.dims[1])
            else:
                self.zect.dims = (self.zect.dims[0]-dX, self.zect.dims[1])
                self.zect.pos = (self.zect.pos[0]+dX, self.zect.pos[1])
            self.updateToolBar() # calls render
    def initToolBar(self):
        x, y = self.zect.pos
        w, h = self.zect.dims
        self.toolbarZect = pygrend.Zect(
                                  id = self.zect.id + 'toolbar',
                                  pos = (x+2, y+2), 
                                  dims = (w-4, 12))
        self.sceneGraph.graph.append(self.toolbarZect)
        self.renderChannel.send('render')
    def updateToolBar(self):
        x, y = self.zect.pos
        w, h = self.zect.dims
        self.toolbarZect.pos = (x+2, y+2)
        self.toolbarZect.dims = (w-4, 12)
        self.renderChannel.send('render')
