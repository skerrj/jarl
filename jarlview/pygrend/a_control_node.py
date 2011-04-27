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

import pygame
from pygame.locals import *

import pygrend

class AControlNode:
    def __init__(self,  node_id):
        self.node_id = node_id
        #  Socket to talk to server
        self.context = zmq.Context()
        self.event_sock = self.context.socket(zmq.SUB)
        self.scene_graph_sock = self.context.socket(zmq.PUSH)
        self.scene_graph_sock.connect("ipc://pygrend_sg.ipc")
        self.event_sock.connect ("ipc://pygrend_zvent.ipc")
        # Subscribe to all messages
        filter = sys.argv[1] if len(sys.argv) > 1 else ""
        self.event_sock.setsockopt(zmq.SUBSCRIBE, filter)

        self.running = True
        self.lastx = 0
        self.lasty = 0
        self.scene_graph = []
        self.scene_graph_command_pipe = []
        self.dragging_rect = -1
        
        self.log = logging.getLogger(('acontrolnode-%s'%self.node_id))
        self.log.info(("-- AControlNode [%s]"% self.node_id))
    
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
        self.scene_graph_sock.send(ms)
    def test_commands(self,  n,  m,  xi,  yi):
        view_list = []
        x = xi
        y = yi
        for i in range(n):
            yo = (i*32)
            for j in range(m):
                xo = (j*32)
                view_list.append(pygrend.Zect(x=x+xo,y=y+yo,  text='+'))
        cmd = pygrend.SceneGraphSyncMessage(self.node_id, 'add', view_list=view_list)
        self.scene_graph_command_pipe.append(cmd)
        self.sync_scene_graphs()
    def run(self):
        while( self.running ):
            self.get_events()
            self.sync_scene_graphs()
        self.clean_up()
    def sync_scene_graphs(self):
        sg_cmd_pipe_not_empty = len(self.scene_graph_command_pipe) != 0
        for i in range(len(self.scene_graph_command_pipe)):
            cmd = self.scene_graph_command_pipe.pop()
            #log.debug('sync_scene_graphs[%s]' % cmd.command)
            self.send_message(cmd)
            if (cmd.command == 'add'):
                self.scene_graph += cmd.view_list
            elif (cmd.command == 'del'):
                for i in cmd.index_list:
                    del self.scene_graph[i]
            elif (cmd.command == 'upd'):
                #log.debug('sync_scene_graphs:scene_graph: %s' % self.scene_graph)
                #log.debug('sync_scene_graphs %s' % str(cmd.index_list))
                for i in range(len(cmd.view_list)):
                    self.scene_graph[cmd.index_list[i]] = cmd.view_list[i]
            else:
                pass
        if (sg_cmd_pipe_not_empty):
            self.send_message(pygrend.SceneGraphSyncMessage(self.node_id,  'brk'))
    def get_events(self):
        string = self.event_sock.recv()
        event = pickle.loads(string)
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

    def clean_up(self):
        pygame.quit()

    def on_mouse_move(self, event):
        self.lastx, self.lasty = event.pos
        if (self.dragging_rect > -1):
            v = self.scene_graph[self.dragging_rect]
            v.x, v.y = event.pos
            cmd = pygrend.SceneGraphSyncMessage(self.node_id, 'upd', view_list=[v], index_list=[self.dragging_rect])
            self.scene_graph_command_pipe.append(cmd)
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
    theAControlNode = AControlNode('a1')
    #testing
    theAControlNode.test_commands(5, 20, 10, 42)
    theAControlNode.run()
