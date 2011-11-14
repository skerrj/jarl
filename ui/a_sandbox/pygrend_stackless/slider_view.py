#

import sys
import stackless

import pygrend

class SliderView:
    def __init__(self, 
                 sceneGraph,  
                 eventChannel):
        self.eventChannel = eventChannel
        self.sceneGraph = sceneGraph
        self.childChannels = {}
        self.running = True
        
    def addChild(self,  id,  channel):
        self.childChannels[id] = channel
    
    def runTask(self):
        while( self.running ):
            self.process_events()
    
    def route_events(self):
        event = self.eventChannel.receive()
        
    


