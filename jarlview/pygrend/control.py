#
#   Connects SUB socket to 
#    tcp://localhost:5556
#    ipc://pygame1.ipc
#

import sys
import logging
import zmq
import pickle

import utils.colored_logging

log = logging.getLogger('control')
log.info("-- Control --")

import pygame
from pygame.locals import *

import pygrend

class Control:
    def __init__(self):
        #  Socket to talk to server
        self.context = zmq.Context()
        self.event_sock = self.context.socket(zmq.SUB)
        self.render_sock = self.context.socket(zmq.PUB)
        self.render_sock.bind("tcp://*:5557")
        self.render_sock.bind("ipc://pygrend_rend.ipc")
        #event_sock.connect ("tcp://localhost:5556")
        self.event_sock.connect ("ipc://pygrend_zvent.ipc")
        # Subscribe to all messages
        filter = sys.argv[1] if len(sys.argv) > 1 else ""
        self.event_sock.setsockopt(zmq.SUBSCRIBE, filter)

        self.running = True
        self.lastx = 0
        self.lasty = 0
        self.scene_graph = []
        self.dragging_rect = -1
    
    def hit_test(self):
        for i in range(len(self.scene_graph)):
            r = self.scene_graph[i]
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
                
    
    
    def send_message(self,  mes):
        ms = pickle.dumps(mes)
        self.render_sock.send(ms)
    def test_commands(self):
        r = pygrend.Zect(x=100,y=100)
        self.scene_graph.append(r)
        r = pygrend.Zect(x=150,y=100)
        self.scene_graph.append(r)
        r = pygrend.Zect(x=200,y=200)
        self.scene_graph.append(r)
        r = pygrend.Zect(x=250,y=200)
        self.scene_graph.append(r)
        self.pub_render_messages()
    def run(self):
        while( self.running ):
            self.get_events()
            self.pub_render_messages()
        self.clean_up()
    def pub_render_messages(self):
        self.send_message(pygrend.RenderMessage(cmd='clr'))
        for v in self.scene_graph:
            #print "pub_render_messages: ",  v.x, v.y
            self.send_message(pygrend.RenderMessage(cmd='rec', view=v))
        self.send_message(pygrend.RenderMessage(cmd='pau'))
    def get_events(self):
        string = self.event_sock.recv()
        event = pickle.loads(string)
        if event.type == pygame.MOUSEMOTION:
            self.on_mouse_move(event)
            #print "mouse at (%d, %d)" % event.pos
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

    def clean_up(self):
        pygame.quit()

    def on_mouse_move(self, event):
        #print "in mm, hit_index: ", self.dragging_rect
        self.lastx, self.lasty = event.pos
        if (self.dragging_rect > -1):
            v = self.scene_graph[self.dragging_rect]
            v.x, v.y = event.pos
            self.scene_graph[self.dragging_rect] = v
    def on_key_down(self, event):
        pass
    def on_key_up(self, event):
        pass
    def on_lbutton_down(self, event):
        self.dragging_rect = self.hit_test()
        pass
    def on_mbutton_down(self, event):
        pass
    def on_rbutton_down(self, event):
        pass
    def on_lbutton_up(self, event):
        self.dragging_rect = -1
    def on_mbutton_up(self, event):
        pass
    def on_rbutton_up(self, event):
        pass


if __name__ == "__main__" :
    theControl = Control()
    #testing
    theControl.test_commands()
    theControl.run()
