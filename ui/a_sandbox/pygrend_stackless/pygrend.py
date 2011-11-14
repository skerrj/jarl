#
#
#
class Zvent:
    pass

class Zect:
    def __init__(self,
                 id = '', 
                 x=0,y=0,
                 width=32,
                 height=32,
                 text='', 
                 color=(255,255,255, 255*0.2), 
                 tag='', 
                 children=[]):
        self.id = id
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text = text
        self.color=color
        self.tag = tag
        self.children = children
