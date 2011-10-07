#
#
#
import stackless
import pygame
from pygame.locals import *
import pygrend

def recvEventTestTask(eventChannel,  renderChannel,  id):
    while (True):
        event = eventChannel.receive()
        if event.type == pygame.MOUSEMOTION:
            print ( '%s recving MOUSEMOTION @ (%d, %d)' % (id,  event.pos[0],  event.pos[1]))
            #renderChannel.send('render')
        elif ( event.type == pygame.NOEVENT):
            pass
#
class TestViews:
    def __init__(self,  
                 scene_graph, 
                 renderChannel):
        self.scene_graph = scene_graph
        self.renderChannel = renderChannel
    
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
