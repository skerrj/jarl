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
render = renderer.Renderer(renderCh)
task0=stackless.tasklet(render.renderTask)()

test1 = testing.TestViews(render.scene_graph,  renderCh)
test1.test_commands(5, 20, 10, 42+(5*32))

eventCh = channels.broadcast.BroadcastChannel()
task1=stackless.tasklet(events.sendEventTask)(eventCh)

task2=stackless.tasklet(testing.recvEventTestTask)(eventCh,  renderCh, 'a')

fc=first_controller.FirstContoller(render.scene_graph, eventCh,  renderCh)
task3=stackless.tasklet(fc.runTask)()

stackless.run()

#while ( True):
#    pass
