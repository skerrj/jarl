#
#
#
import stackless
import pygame
from pygame.locals import *
import pygrend

def recvEventTestTask(eventChannel,  renderChannel):
    while (True):
        event = eventChannel.receive()
        if event.type == pygame.MOUSEMOTION:
            print ( 'MOUSEMOTION @ (%d, %d)' % (event.pos[0],  event.pos[1]))
            #renderChannel.send('render')
        elif ( event.type == pygame.NOEVENT):
            pass
#
    
def testA(scene_graph, renderChannel,  n,  m,  xi,  yi):
    view_list = []
    x = xi
    y = yi
    cnt = 0
    for i in range(n):
        yo = (i*32)
        for j in range(m):
            xo = (j*32)
            view_list.append(pygrend.Zect(id = str(cnt),  x=x+xo,y=y+yo,  text='+'))
            cnt += 1
    scene_graph += view_list
    renderChannel.send('render')

def testA1(scene_graph, renderChannel):
    testA(scene_graph, renderChannel, 5, 20, 0, 42+(12*32))
