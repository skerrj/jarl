#
#
#
import stackless
import pygame
from pygame.locals import *

def sendEventTask(channel):
    while (True):
        events = pygame.event.get()
        if events != []:
            i = 0
            mouse_motion_events = []
            for event in events:
                if (event.type == pygame.MOUSEMOTION):
                    mouse_motion_events.append(event)
                elif ( event.type == pygame.QUIT):
                    print "Bye."
                    pygame.quit()
                else:
                    channel.send(event)
                i += 1
            if (mouse_motion_events != []):
                channel.send(mouse_motion_events[len(mouse_motion_events)-1])
        stackless.schedule()


#    while (True):
#        for event in pygame.event.get():
#        #event = pygame.event.poll()
#            if ( event.type == pygame.QUIT):
#                print "Bye."
#                pygame.quit()
#            channel.send(event)
#        stackless.schedule()
