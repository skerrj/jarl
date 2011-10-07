#

import sys
import stackless
import pygame
from pygame.locals import *

import pygrend

class AControlNode:
    def __init__(self,  
                 node_id,  
                 scene_graph, 
                 eventChannel, 
                 renderChannel):
        self.node_id = node_id
        self.lastx = 0
        self.lasty = 0
        self.scene_graph = scene_graph
        self.eventChannel = eventChannel
        self.renderChannel = renderChannel
        self.dragging_rect = -1
        #self.scene_graph[self.node_id] = []
        self.running = True
    
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
    
    def test_commands(self,  n,  m,  xi,  yi):
        view_list = []
        x = xi
        y = yi
        for i in range(n):
            yo = (i*32)
            for j in range(m):
                xo = (j*32)
                view_list.append(pygrend.Zect(x=x+xo,y=y+yo,  text='+'))
        self.scene_graph += view_list
        self.renderChannel.send('render')
    
    def runTask(self):
        while( self.running ):
            self.process_events()
    
    def process_events(self):
        event = self.eventChannel.receive()
        if event.type == pygame.MOUSEMOTION:
            self.on_mouse_move(event)
            #log.debug( 'recving MOUSEMOTION @ (%d, %d)' % event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.on_lbutton_up(event)
                #print "left mouse up"
            elif event.button == 2:
                self.on_mbutton_up(event)
            elif event.button == 3:
                self.on_rbutton_up(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #print "left mouse down"
                self.on_lbutton_down(event)
            elif event.button == 2:
                self.on_mbutton_down(event)
            elif event.button == 3:
                self.on_rbutton_down(event)
        elif event.type == pygame.KEYUP:
            self.on_key_up(event)
        elif event.type == pygame.KEYDOWN:
            self.on_key_down(event)
        elif event.type == pygame.QUIT:
            self.running = False
        else:
            pass
    
    def on_mouse_move(self, event):
        self.lastx, self.lasty = event.pos
        if (self.dragging_rect > -1):
            v = self.scene_graph[self.dragging_rect]
            v.x, v.y = event.pos
            #self.scene_graph[self.node_id][self.dragging_rect] =  v
            self.renderChannel.send('render')
    
    def on_key_down(self, event):
        pass
    def on_key_up(self, event):
        pass
    def on_lbutton_down(self, event):
        self.dragging_rect = self.hit_test()
    def on_mbutton_down(self, event):
        pass
    def on_rbutton_down(self, event):
        pass
    def on_lbutton_up(self, event):
        self.dragging_rect = -1
        #self.renderChannel.send('render')
    def on_mbutton_up(self, event):
        pass
    def on_rbutton_up(self, event):
        pass


#if __name__ == "__main__" :
#    theAControlNode = AControlNode('a1')
#    #testing
#    theAControlNode.test_commands(5, 20, 10, 42)
#    theAControlNode.run()
