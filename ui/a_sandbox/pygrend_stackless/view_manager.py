#

import sys
import stackless
import pygame
from pygame.locals import *

import pygrend

class ViewManager:
    def __init__(self,  
                 node_id,  
                 scene_graph, 
                 eventChannel, 
                 renderChannel, 
                 screenSize=(800, 600)):
        self.node_id = node_id
        self.lastx = 0
        self.lasty = 0
        self.scene_graph = scene_graph
        self.eventChannel = eventChannel
        self.renderChannel = renderChannel
        self.dragging_rect = -1
        self.scene_graph[self.node_id] = []
        self.running = True
        self.screenSize = screenSize
        self.baseView()
    
    def hit_test(self):
        views = self.scene_graph[self.node_id]
        for i in range(len(views)):
            r = views[i]
            x = self.lastx
            y = self.lasty
            x1 = r.x
            x2 = r.x + r.width
            y1 = r.y
            y2 = r.y + r.height
            if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                print self.scene_graph[self.node_id][i].tag
                return i
        return -1
    
    def baseView(self):
        view_list = []
        width = self.screenSize[0]
        height = self.screenSize[1]
        view_list.append(
                         pygrend.Zect(x=10,y=42,  width = 250,  height = 250,  text='',  tag='slider1_l'))
        view_list.append(
                         pygrend.Zect(x=10+256,y=42,  width = 250,  height = 250,  text='',  tag='slider1_r'))
        view_list.append(
                         pygrend.Zect(x=10+251,y=42,  width = 4,  height = 250,  text='',  tag='slider1'))        
        self.scene_graph[self.node_id] = view_list
        self.renderChannel.send('render')
    
    def getView(self,  tag):
        returnVal = None
        for v in self.scene_graph[self.node_id]:
            if (v.tag == tag):
                returnVal = v
        return returnVal
    
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
    # xS
    # xL, wL, xR, wR
    # xLastLeft = xL + wL
    # xChangeL = xS - xLastLeft
    # wNewL = wL + xChangeL
    # xLastRight = xR
    # xChangeR = xLastRight - xS
    # xNewR = xR + xChangeR
    # wNewR = wR + (xR - xNewR)
    def on_mouse_move(self, event):
        self.lastx, self.lasty = event.pos
        if (self.dragging_rect != -1):
            v = self.scene_graph[self.node_id][self.dragging_rect]
            if (v.tag == 'slider1'):
                v_r = self.getView('slider1_r')
                v_l = self.getView('slider1_l')
                xS = v.x
                xL = v_l.x
                wL =v_l.width
                xR = v_r.x
                wR = v_r.width
                xLastLeft = xL + wL
                xChangeL = xS - xLastLeft
                v_l.width = wL + xChangeL
                xLastRight = xR
                xChangeR = xLastRight - xS
                v_r.x = xR + xChangeR
                v_r.width = wR + (xR - v_r.x)
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
