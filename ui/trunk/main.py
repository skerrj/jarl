#import pygrend
from pygrend import *
from widgets import *

DaSys = System()

# sg[id]= (view, children)
SceneGraph = dict([])

# ### init
InitPyGame(DaSys)

vTop = View()
r = Rect()
r.pos = (0, 0)
r.dims = (800,  600)
vTop.rect = r

# #######################
SceneGraph['vTop']= vTop
# #######################

#splitViewInX(vTop, 10)
splitViewInY(vTop, 10)

mainLoop(DaSys,  SceneGraph)
