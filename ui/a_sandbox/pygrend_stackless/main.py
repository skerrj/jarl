#import display 
#
#if __name__ == "__main__" :
#    d = display.Display()
#    d.run()

import stackless
import pygame
from pygame.locals import *
import channels.broadcast
import events
import renderer

import view_view

#import a_control_node
import testing
#import view_manager
#import first_controller

#renderCh=stackless.channel()
eventCh = channels.broadcast.BroadcastChannel()

#render = renderer.Renderer(renderCh)
render = renderer.Renderer()
#task0=stackless.tasklet(render.renderTask)()

v1 = view_view.ViewView(
                        render.sg, 
                        eventCh,  render.channel, 
                        id='v1',  pos=(2, 2), 
                        dims=(390, 596))

v2 = view_view.ViewView(
                        render.sg, 
                        eventCh,  render.channel, 
                        id='v2',  pos=(394, 2), 
                        dims=(12, 596))

v3 = view_view.ViewView(
                        render.sg, 
                        eventCh,  render.channel, 
                        id='v3',  pos=(408, 2), 
                        dims=(390, 596))

#testing.testA1(render.sg.getSceneGraph(),   render.channel)
# test getViews
#render.sg.printViewIds()
#print render.sg.getViews(['2',  '4',  '8',  '11'])

task1=stackless.tasklet(events.sendEventTask)(eventCh)
task2=stackless.tasklet(testing.recvEventTestTask)(eventCh,  render.channel)

#fc=first_controller.FirstContoller(render.sg.getSceneGraph(), eventCh,  render.channel)
#task3=stackless.tasklet(fc.runTask)()

stackless.run()

#while ( True):
#    pass
