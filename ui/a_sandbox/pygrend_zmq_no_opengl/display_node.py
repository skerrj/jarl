import os
import sys
import logging
import time
import math
import ConfigParser
import pickle
import itertools

import utils.colored_logging

log = logging.getLogger('displaynode')
log.info("-- DisplayNode --")

import pygame
from pygame.locals import *

import utils.utils
from utils.utils import *

import zmq

import pygrend
 
SCREEN_SIZE = (800, 600)
#SCREEN_SIZE = (0, 0)

class DisplayNode:
    def __init__(self):
        self.render_cnt = 0
        self.render_window = 100
        self.pull_sg_window = 100
        self.running = True
        self.screen = None
        self.size = self.weight, self.height = None, None
        self.scene_graph = {}
        self.backgroundcolor = (0, 0, 0)
        self.fonts = {}
        self.width = None
        self.height = None
        self.flags = None
        self.clock = None
        self.clock = pygame.time.Clock()
        self.rt = 0
        self.pt = 0
        
        self.context = zmq.Context(2)
        self.event_sock = self.context.socket(zmq.PUB)
        self.scene_graph_sock = self.context.socket(zmq.PULL)
        #self.event_sock.bind("tcp://*:5556")
        self.event_sock.bind("ipc://pygrend_zvent.ipc")
        self.scene_graph_sock.bind ("ipc://pygrend_sg.ipc")
    def init(self):
        pygame.init()
        pygame.font.init()
        self.font = self.get_font(28)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        pygame.display.set_caption('DisplayNode')
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(
            [QUIT, KEYUP, KEYDOWN, \
             VIDEORESIZE, VIDEOEXPOSE, MOUSEMOTION, \
             MOUSEBUTTONUP, MOUSEBUTTONDOWN])
        self.running = True
 
    def send_event(self, event):
        #log.debug ('ENTER send_event()')
        zv = pygrend.Zvent()
        if event.type == pygame.MOUSEMOTION:
            zv.__dict__ = {'type':event.type,
                           'pos':event.pos,
                           'rel':event.rel,
                           'button':event.buttons}
            #log.debug( 'sending MOUSEMOTION @ (%d, %d)' % event.pos)
        elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            zv.__dict__ = {'type':event.type,
                           'pos':event.pos,
                           'button':event.button}
        elif event.type == pygame.KEYUP:
            zv.__dict__ = {'type':event.type, 
                           'key':event.key, 
                           'mod':event.mod}
            if event.key == K_ESCAPE or event.key == K_q:
                zv.__dict__ = {'type':pygame.QUIT}
                self.running = False
        elif event.type == pygame.KEYDOWN:
            zv.__dict__ = {'type':event.type,
                           'unicode':event.unicode,
                           'key':event.key, 
                           'mod':event.mod}
            if event.key == K_f:
                if self.flags & FULLSCREEN == FULLSCREEN:
                    self.flags = self.flags ^ FULLSCREEN
                else:
                    self.flags = self.flags | FULLSCREEN
                self.screen = pygame.display.set_mode((0,0), self.flags)
                self.projection_setup()
        elif event.type == pygame.QUIT:
            zv.__dict__ = {'type':event.type}
            self.running = False 
        else:
            zv.__dict__ = {'type':event.type}
        pzv = pickle.dumps(zv)
        self.event_sock.send(pzv)
    def pull_sg_updates(self):
        try:
            s = self.scene_graph_sock.recv(zmq.NOBLOCK)
            cmd = pickle.loads(s)
            #for i in range(self.pull_sg_window):
            cnt = 0
            #while (cmd.command != 'brk'):
            while (cnt<self.pull_sg_window):
                log.debug('pull_sg_updates[%s][%s][%d]' % (cmd.node_id, cmd.command,  cnt))
                if (cmd.command == 'add'):
                    if (not self.scene_graph.has_key(cmd.node_id)):
                        self.scene_graph[cmd.node_id] = cmd.view_list
                    else:
                        self.scene_graph[cmd.node_id] += cmd.view_list
                elif (cmd.command == 'del'):
                    node_sg = self.scene_graph[cmd.node_id]
                    for i in cmd.index_list:
                        del node_sg[i]
                elif (cmd.command == 'upd'):
                    for i in range(len(cmd.view_list)):
                        self.scene_graph[cmd.node_id][cmd.index_list[i]] = cmd.view_list[i]
                else:
                    pass
                #s = self.scene_graph_sock.recv()
                s = self.scene_graph_sock.recv(zmq.NOBLOCK)
                cmd = pickle.loads(s)
                cnt += 1
        except zmq.ZMQError:
            pass
        pygame.display.flip()
    def render(self):
        self.screen.fill(self.backgroundcolor)
        for id, node_sg in self.scene_graph.iteritems():
            for v in node_sg:
                self.draw_face(v.text, v.x,  v.y)
        self.draw_face(str(self.rt), 10, 10)
        self.draw_face(str(self.pt), 42, 10)
        pygame.display.update()
    def cleanup(self):
        pygame.quit()
    
    def run(self):
        if self.init() == False:
            self.running = False
        while( self.running ):
            for _ in itertools.repeat(None,  self.render_window):
                self.clock.tick()
                self.pull_sg_updates()
                self.pt = self.clock.tick()
                self.render() 
                self.rt = self.clock.tick()
                for event in pygame.event.get():
                    self.send_event(event)
            log.debug('waiting')
            self.send_event(pygame.event.wait())
        self.cleanup()
    def get_font(self, size, bold = False):
        key = (size, bold)
        if not key in self.fonts:
            if bold:
                font_name = 'fonts/bitstream_bold.ttf'
            else:
                font_name = 'fonts/bitstream.ttf'
            self.fonts[key] = pygame.font.Font(font_name, size)
        return self.fonts[key]
    def draw_face(self,  text,  x,  y):
        theFont = self.get_font(12)
        surface = theFont.render(text, True, (255, 255, 255))
        rounded_surface = rounded_border_surface(surface)
        self.screen.blit(rounded_surface, (x, self.height - y))

if __name__ == "__main__" :
    theDisplayNode = DisplayNode()
    theDisplayNode.run()
