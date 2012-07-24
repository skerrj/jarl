import pygrend
from pygrend import *

DaSys = System()

# sg[id]= (view, children)
SceneGraph = dict([])

# ### init
InitPyGame(DaSys)

# Views ####################### 
class BaseView(View):
    def __init__ (self):
        View.__init__(self)
        self.lastx, self.lasty = (0, 0)

class XSlider(BaseView):
    def __init__(self):
        BaseView.__init__(self)
        self.leftDown = False
        self.leftView = None
        self.rightView = None
    def processEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                dX = event.pos[0] - self.lastx
                self.lastx, self.lasty = event.pos
                if (self.leftDown):
                    self.resizeViews(dX)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and HitTest(self.rect,  event.pos): # left mouse down
                    self.leftDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left mouse up
                    self.leftDown = False
            elif ( event.type == pygame.NOEVENT):
                pass
    def resizeViews(self, dX):
        self.rect.pos = (self.rect.pos[0]+dX,  self.rect.pos[1])
        self.leftView.rect.dims = (self.leftView.rect.dims[0]+dX, self.leftView.rect.dims[1])
        self.rightView.rect.dims = (self.rightView.rect.dims[0]-dX, self.rightView.rect.dims[1])
        self.rightView.rect.pos = (self.rightView.rect.pos[0]+dX, self.rightView.rect.pos[1])

#v1 = View(rect = Rect(dims = (800, 500)))
v1 = View()
v1r = Rect()
v1r.pos = (0, 0)
v1r.dims = (350,  600)
v1.rect = v1r
v2 = View()
v2r = Rect()
v2r.pos = (450, 0)
v2r.dims = (350,  600)
v2.rect = v2r
slider = XSlider()
sliderr = Rect()
sliderr.pos = (350, 0)
sliderr.dims = (100,  600)
slider.rect = sliderr
slider.leftView = v1
slider.rightView = v2
# #######################
SceneGraph['v1']= (v1,  [])
SceneGraph['v2']= (v2,  [])
SceneGraph['s1']= (slider,  [])
# #######################

mainLoop(DaSys,  SceneGraph)
