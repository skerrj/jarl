#

import sys
import stackless
import pygame
from pygame.locals import *

import pygrend

class FirstContoller:
    def __init__(self,  
                 scene_graph, 
                 eventChannel, 
                 renderChannel):
        self.scene_graph = scene_graph
        self.eventChannel = eventChannel
        self.renderChannel = renderChannel
        self.running = True
        self.focusedViewIndex = 0
    
    def hit_test(self):
        views = self.scene_graph
        for i in range(len(views)):
            r = views[i]
            x = self.lastx
            y = self.lasty
            x1 = r.x
            x2 = r.x + r.width
            y1 = r.y
            y2 = r.y + r.height
            if x >= x1 and x <= x2 and \
               y >= y1 and y <= y2:
                #print "hit: ", i
                return i
        return -1
    
    
    def runTask(self):
        while( self.running ):
            self.process_events()
    
    def process_events(self):
        event = self.eventChannel.receive()
        if event.type == pygame.MOUSEMOTION:
            self.on_mouse_move(event)
            #log.debug( 'recving MOUSEMOTION @ (%d, %d)' % event.pos)
        elif event.type == pygame.KEYUP:
            self.on_key_up(event)
        elif event.type == pygame.KEYDOWN:
            self.on_key_down(event)
        elif event.type == pygame.QUIT:
            self.running = False
        else:
            pass
    
    def on_mouse_move(self, event):
        lastview = self.scene_graph[self.focusedViewIndex]
        lastview.color = (255,255,255, 255*0.2)
        self.lastx, self.lasty = event.pos
        self.focusedViewIndex = self.hit_test()
        if ( self.focusedViewIndex >= 0):
            #print 'hit: ',  self.focusedViewIndex
            v = self.scene_graph[self.focusedViewIndex]
            v.color = (255,255,255, 255*0.4)
            self.renderChannel.send('render')
    
    def on_key_down(self, event):
        pass
    def on_key_up(self, event):
        pass
