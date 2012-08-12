#import pygrend
from pygrend import *
from widgets import *

DaSys = System()

# sg[id]= (view, children)
SceneGraph = dict([])

# ### init
InitPyGame(DaSys)


#v1 = View()
#v1r = Rect()
#v1r.dims = (800,  600)
#v1.rect = v1r

vTop = View()
r = Rect()
r.pos = (0, 0)
r.dims = (800,  600)
vTop.rect = r

#slider_width = 10
#
#pos = vTop.rect.GetPos()
#dims = vTop.rect.GetDims()
#
#v1 = View()
#v1r = Rect()
#v1r.pos =  lambda: (pos[0], pos[1]) #(0, 0)
#v1r.dims = lambda: ((dims[0]/2)-(slider_width/2), dims[1]) #(395,  600)
#v1.rect = v1r
#v2 = View()
#v2r = Rect()
#v2r.pos = lambda: ((dims[0]/2)+(slider_width/2), pos[1]) #(405, 0)
#v2r.dims = lambda: ((dims[0]/2)-(slider_width/2), dims[1]) #(395,  600)
#v2.rect = v2r
#slider = XSlider()
#sliderr = Rect()
#sliderr.pos = lambda: ((dims[0]/2)-(slider_width/2), pos[1]) #(395, 0)
#sliderr.dims = lambda: (slider_width, dims[1]) #(10,  600)
#slider.rect = sliderr
#slider.leftView = v1
#slider.rightView = v2
#
#vTop.children['v1'] = v1
#vTop.children['v2'] = v2
#vTop.children['s1'] = slider
# #######################
SceneGraph['vTop']= vTop
#SceneGraph['v1']= v1
#SceneGraph['v2']= v2
#SceneGraph['s1']= slider
# #######################

splitViewInX(vTop, 10)

mainLoop(DaSys,  SceneGraph)
