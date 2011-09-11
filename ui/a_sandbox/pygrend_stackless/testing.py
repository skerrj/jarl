#
#
#
import stackless
import pygame
from pygame.locals import *

def recvEventTestTask(eventChannel,  renderChannel,  id):
    while (True):
        event = eventChannel.receive()
        if event.type == pygame.MOUSEMOTION:
            print ( '%s recving MOUSEMOTION @ (%d, %d)' % (id,  event.pos[0],  event.pos[1]))
            #renderChannel.send('render')
        elif ( event.type == pygame.NOEVENT):
            pass
