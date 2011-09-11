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

renderCh=stackless.channel()
render = renderer.Renderer(renderCh)
task0=stackless.tasklet(render.renderTask)()

eventCh = channels.broadcast.BroadcastChannel()
task1=stackless.tasklet(events.sendEventTask)(eventCh)

task2=stackless.tasklet(testing.recvEventTestTask)(eventCh,  renderCh, 'a')
#task3=stackless.tasklet(testing.recvEventTestTask)(eventCh,  renderCh, 'b')
#task4=stackless.tasklet(testing.recvEventTestTask)(eventCh,  renderCh, 'c')
#
#cNodeA1 = a_control_node.AControlNode('a1',  render.scene_graph,  eventCh,  renderCh)
#cNodeA1.test_commands(5, 20, 10, 42)
#task6=stackless.tasklet(cNodeA1.runTask)()

cNodeB1 = a_control_node.AControlNode('b1',  render.scene_graph,  eventCh,  renderCh)
cNodeB1.test_commands(5, 20, 10, 42+(11*32))
task7=stackless.tasklet(cNodeB1.runTask)()

#cNodeC1 = a_control_node.AControlNode('c1',  render.scene_graph,  eventCh,  renderCh)
#cNodeC1.test_commands(5, 20, 10, 42+(5*32))
#task8=stackless.tasklet(cNodeC1.runTask)()

viewManager = view_manager.ViewManager('z1',  render.scene_graph,  eventCh, renderCh)
task9 = stackless.tasklet(viewManager.runTask)()

stackless.run()

#while ( True):
#    pass
