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

log = logging.getLogger('ATreeControlNode')
log.info("-- ATreeControlNode --")

import pygame
from pygame.locals import *

import pygrend

class ATreeControlNode:
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
        self.tree_model = []
        
        self.xo = self.yo = 32
        self.x = self.y = 0
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
    def test_tree_model(self):
        self.tree_model = \
        [('1-dkfjdfkdj',  \
            [('1.1-ruereiu', []), \
              ('1.2-nmmncv', [])]), \
          ('2-wqewew', []), \
          ('3-dkfddfjdfkdj',  \
            [('3.1-rurrrereiu', []), \
              ('3.2-nmmnnnncv', [])]),
          ('4-47384739erer', [])]
    def update_tree(self,  tree_model):
        view_list = []
        for n in tree_model:
            view_list.append(pygrend.Zect(x=self.x,y=self.y,  text='+'))
            view_list.append(pygrend.Zect(x=(self.x+self.xo),y=self.y,  text=n[0]))
            self.y += self.yo
            if (n[1] != []):
                self.x += self.xo
                self.update_tree(n[1])
                self.x -= self.xo
        cmd = pygrend.SceneGraphSyncMessage(self.node_id, 'add', view_list=view_list)
        self.scene_graph_command_pipe.append(cmd) 
    def test_commands(self):
        self.x,  self.y = (300,  100)
        self.test_tree_model()
        self.update_tree(self.tree_model)
        self.sync_scene_graphs()
    def run(self):
        while( self.running ):
            self.get_events()
            self.sync_scene_graphs()
        self.clean_up()
    def sync_scene_graphs(self):
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
    theATreeControlNode = ATreeControlNode('at1')
    #testing
    theATreeControlNode.test_commands()
    theATreeControlNode.run()
