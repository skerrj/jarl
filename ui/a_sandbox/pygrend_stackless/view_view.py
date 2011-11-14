#

import sys
import stackless

import pygrend

class ViewView:
    def __init__(self, 
                 sceneGraph, 
                 eventChannel, 
                 renderChannel, 
                 id, 
                 pos, 
                 dims):
        self.sceneGraph = sceneGraph
        self.eventChannel = eventChannel
        self.renderChannel = renderChannel
        self.childChannels = {}
        self.running = True
        self.id = id
        self.pos = pos
        self.dims = dims
        self.initView()
        self.task = stackless.tasklet(self.runTask)()
        
    def initView(self):
        v = pygrend.Zect(id = self.id,  
                         x=self.pos[0],y=self.pos[1],  
                         width=self.dims[0], height=self.dims[1])
        self.sceneGraph.graph.append(v)
        self.renderChannel.send('render')
    
    def addChild(self,  id):
        self.childChannels[id] = stackless.channel()
    
    def runTask(self):
        while( self.running ):
            self.process_events()
    
    def process_events(self):
        event = self.eventChannel.receive()
        self.renderChannel.send('render')
    


