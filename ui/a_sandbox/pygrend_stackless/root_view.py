#

import sys
import stackless

import pygrend

class RootView:
    def __init__(self, 
                 sceneGraph,  
                 eventChannel):
        self.eventChannel = eventChannel
        self.sceneGraph = sceneGraph
        self.childChannels = {}
        self.running = True
        
    def addChild(self,  id):
        self.childChannels[id] = stackless.channel()
    
    def runTask(self):
        while( self.running ):
            self.route_events()
    
    def route_events(self):
        pass #event = self.eventChannel.receive()
        
    


