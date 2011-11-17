#
#
#
class Zvent:
    pass

class Zect:
    def __init__(self,
                 id = '', 
                 pos=(0, 0),
                 dims=(32, 32),
                 text='', 
                 color=(255,255,255, 255*0.2), 
                 tag='', 
                 children=[]):
        self.id = id
        self.pos=pos
        self.dims=dims
        self.text = text
        self.color=color
        self.tag = tag
        self.children = children
