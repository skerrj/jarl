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
        #self.childChannels = {}
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
        stackless.schedule()

class ViewView:
    def __init__(self, 
                 sceneGraph, 
                 renderChannel, 
                 zect):
        self.sceneGraph = sceneGraph
        self.eventChannel = None
        self.renderChannel = renderChannel
        self.childChannels = {}
        self.running = True
        self.id = zect.id
        self.pos = zect.pos
        self.dims = zect.dims
        self.lastx, self.lasty = (0, 0)
        self.initView()
        #self.task = stackless.tasklet(self.runTask)()
        self.task = None
        
    def initView(self):
        v = pygrend.Zect(id = self.id,  pos=self.pos,  dims=self.dims)
        self.sceneGraph.graph.append(v)
        self.renderChannel.send('render')
    
    def hitTest(self):
        x = self.lastx
        y = self.lasty
        x1 = self.pos[0]
        x2 = self.pos[0]+ self.dims[0]
        y1 = self.pos[1]
        y2 = self.pos[1]+ self.dims[1]
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
            print ( '%s MOUSEMOTION @ (%d, %d)' % (self.id,  event.pos[0],  event.pos[1]))
            #renderChannel.send('render')
        elif ( event.type == pygame.NOEVENT):
            pass
        self.renderChannel.send('render')
    

class SliderView(ViewView):
    def __init__(self, 
                 sceneGraph, 
                 renderChannel, 
                 zect):
        ViewView.__init__(self,  sceneGraph,  renderChannel,  zect)
        self.leftdown = False
    
    def process_events(self):
        event = self.eventChannel.receive()
        if event.type == pygame.MOUSEMOTION:
            self.lastx, self.lasty = event.pos
            #print ( 'slider MOUSEMOTION @ (%d, %d)' % (event.pos[0],  event.pos[1]))
            if (self.leftdown):
                print ( 'slider MOUSEMOTION @ (%d, %d)' % (event.pos[0],  event.pos[1]))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hitTest(): # left mouse down
                self.leftdown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # left mouse up
                self.leftdown = False
        elif ( event.type == pygame.NOEVENT):
            pass
        self.renderChannel.send('render')

