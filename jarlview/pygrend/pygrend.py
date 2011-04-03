#
#
#
class Zvent:
    pass

class Zect:
    def __init__(self,x=0,y=0,width=32,height=32,color=(255,255,255)):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color

class RenderMessage:
    def __init__(self, cmd='', view=None):
        self.command=cmd
        self.view=view
