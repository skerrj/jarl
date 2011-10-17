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
import a_control_node
import testing
import renderer
import view_manager
import first_controller

renderCh=stackless.channel()
eventCh = channels.broadcast.BroadcastChannel()

render = renderer.Renderer(renderCh)
task0=stackless.tasklet(render.renderTask)()
testing.test1(render.scene_graph,  renderCh, 5, 20, 0, 42+(12*32))

task1=stackless.tasklet(events.sendEventTask)(eventCh)
task2=stackless.tasklet(testing.recvEventTestTask)(eventCh,  renderCh)

fc=first_controller.FirstContoller(render.scene_graph, eventCh,  renderCh)
task3=stackless.tasklet(fc.runTask)()

stackless.run()

#while ( True):
#    pass
