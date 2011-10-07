#
#
#
class Zvent:
    pass

class Zect:
    def __init__(self,x=0,y=0,
                 width=32,
                 height=32,
                 text='', 
                 color=(255,255,255, 255*0.2), 
                 tag='', 
                 children=[]):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text = text
        self.color=color
        self.tag = tag
        self.children = children
