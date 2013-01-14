#
#
#
from view import *

# Views ####################### 
class BaseView(View):
    def __init__ (self, name='aBaseView'):
        View.__init__(self, name)
        self.lastx, self.lasty = (0, 0)
        self.manage_mode = False 
        self.hasFocus = False
        self.hidden = False
    def processEvents(self, events):
        if len(self.children) == 0:
            for event in events:
                if event.type == pygame.KEYUP:
                    #print event.key, self.manage_mode, self.onTop
                    if event.key == K_ESCAPE:
                        self.boarder_color = (0, 0, 0,255)
                        self.manage_mode = False
                    elif event.key == K_m and not self.manage_mode:# and self.onTop:
                        #188-143-143
                        self.boarder_color = (188,143,143,255)
                        self.manage_mode = True
                    elif event.key == K_x and self.manage_mode:
                        splitViewInX(self,  10)
                    elif event.key == K_y and self.manage_mode:
                        splitViewInY(self,  10)

class XSlider(BaseView):
    def __init__(self, name='aXSlider'):
        BaseView.__init__(self, name)
        self.leftDown = False
        self.leftView = None
        self.rightView = None
        self.boarder = 1
    def processEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                dX = event.pos[0] - self.lastx
                self.lastx, self.lasty = event.pos
                if (self.leftDown):
                    self.resizeViews(dX)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.HitTest(event.pos): # left mouse down HitTest(self.rect,  event.pos)
                    self.leftDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left mouse up
                    self.leftDown = False
            elif ( event.type == pygame.NOEVENT):
                pass
    def resizeViews(self, dX):
        pos = self.rect.GetPos()
        leftVDims = self.leftView.rect.GetDims()
        rightVDims = self.rightView.rect.GetDims()
        rightVPos= self.rightView.rect.GetPos()
        
        self.rect.pos = (pos[0]+dX,  pos[1])
        self.leftView.rect.dims = (leftVDims[0]+dX, leftVDims[1])
        self.rightView.rect.pos = (rightVPos[0]+dX, rightVPos[1])
        self.rightView.rect.dims = (rightVDims[0]-dX, rightVDims[1])

class YSlider(BaseView):
    def __init__(self, name='aYSlider'):
        BaseView.__init__(self, name)
        self.leftDown = False
        self.topView = None
        self.bottomView = None
        self.boarder = 1
    def processEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                dY = event.pos[1] - self.lasty
                self.lastx, self.lasty = event.pos
                if (self.leftDown):
                    self.resizeViews(dY)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.HitTest(event.pos): # left mouse down HitTest(self.rect,  event.pos)
                    self.leftDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left mouse up
                    self.leftDown = False
            elif ( event.type == pygame.NOEVENT):
                pass
    def resizeViews(self, dY):
        pos = self.rect.GetPos()
        topVDims = self.topView.rect.GetDims()
        bottomVDims = self.bottomView.rect.GetDims()
        bottomVPos= self.bottomView.rect.GetPos()
        
        self.rect.pos = (pos[0],  pos[1]+dY)
        self.topView.rect.dims = (topVDims[0], topVDims[1]+dY)
        self.bottomView.rect.pos = (bottomVPos[0], bottomVPos[1]+dY)
        self.bottomView.rect.dims = (bottomVDims[0], bottomVDims[1]-dY)

def splitViewInX(view,  slider_width):
    view.hidden = True
    pos = view.rect.GetPos()
    dims = view.rect.GetDims()
    v1 = BaseView(view.name + '-left')
    v1r = Rect()
    v1r.pos = lambda: (pos[0], pos[1])
    v1r.dims = lambda: ((dims[0]/2)-(slider_width/2), dims[1]) #(395,  600)
    v1.rect = v1r
    v1.boarder = 5
    v1.boarder_color=(0,0,100,255)
    v2 = BaseView(view.name + '-right')
    v2r = Rect()
    v2r.pos = lambda: ((dims[0]/2)+(slider_width/2), pos[1]) #(405, 0)
    v2r.dims = lambda: ((dims[0]/2)-(slider_width/2), dims[1]) #(395,  600)
    v2.rect = v2r
    v2.boarder = 5
    v2.boarder_color=(0,0,100,255)
    slider = XSlider(view.name + '-xslide')
    sliderr = Rect()
    sliderr.pos = lambda: ((dims[0]/2)-(slider_width/2), pos[1]) #(395, 0)
    sliderr.dims = lambda: (slider_width, dims[1]) #(10,  600)
    slider.rect = sliderr
    slider.boarder = 5
    slider.boarder_color=(0,100,0,255)
    slider.leftView = v1
    slider.rightView = v2
    view.addChild(v1)
    view.addChild(v2)
    view.addChild(slider)
    #~ view.children['v1'] = v1
    #~ view.children['v2'] = v2
    #~ view.children['s1'] = slider

def splitViewInY(view,  slider_width):
    view.hidden = True
    pos = view.rect.GetPos()
    dims = view.rect.GetDims()
    v1 = BaseView(view.name + '-top')
    v1r = Rect()
    v1r.pos = lambda: (pos[0], pos[1])
    v1r.dims = lambda: (dims[0], (dims[1]/2)-(slider_width/2)) #(395,  600)
    v1.rect = v1r
    v2 = BaseView(view.name + '-bottom')
    v2r = Rect()
    v2r.pos = lambda: (pos[0],  (dims[1]/2)+(slider_width/2)) #(405, 0)
    v2r.dims = lambda: (dims[0], (dims[1]/2)-(slider_width/2)) #(395,  600)
    v2.rect = v2r
    slider = YSlider(view.name + '-yslide')
    sliderr = Rect()
    sliderr.pos = lambda: (pos[0], (dims[1]/2)-(slider_width/2)) #(395, 0)
    sliderr.dims = lambda: (dims[0], slider_width) #(10,  600)
    slider.rect = sliderr
    slider.topView = v1
    slider.bottomView = v2
    view.addChild(v1)
    view.addChild(v2)
    view.addChild(slider)
    #~ view.children['v1'] = v1
    #~ view.children['v2'] = v2
    #~ view.children['s1'] = slider
