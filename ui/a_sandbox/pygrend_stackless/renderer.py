#
#
#
import stackless
import channels.broadcast
import events
import testing

import core

class Renderer:
    def __init__(self):
        self.pg = core.PyGame()
        self.sg = core.SceneGraph()
        self.channel = stackless.channel()
        self.task = stackless.tasklet(self.renderTask)()
        self.eventChannel = None
        self.eventTask = None
        self.InitEventTask()
    
    def InitEventTask(self):
        self.eventChannel = channels.broadcast.BroadcastChannel()
        self.eventTask=stackless.tasklet(events.sendEventTask)(self.eventChannel)
#        testTask=stackless.tasklet(testing.recvEventTestTask)(
#                                                              self.eventChannel,  self.channel)
    
    def renderView(self,  z):
        self.pg.drawView(z.text, z.pos[0],  z.pos[1], z.dims[0],  z.dims[1],  z.color)
    
    def renderTask(self):
        while (True):
            cmd = self.channel.receive()
            if cmd == 'render':
                self.pg.clearScreen()
                self.pg.clockTick()
                map(self.renderView,  self.sg.getSceneGraph())
                #self.pg.drawView(str(self.pg.clockTick()), 10, 10, w=32)
                #self.pg.drawView('1234567890', 42, 10)
                self.pg.updateScreen()
    
