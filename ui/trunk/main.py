#import pygrend
from scenegraph import *
from pygrend import *
from widgets import *
from view import *

renderer = Renderer()

vTop = BaseView('vTop')
r = Rect()
r.pos = (0, 0)
r.dims = (800,  600)
vTop.rect = r

SCENEGRAPH.add(vTop)

splitViewInX(vTop, 30)
#splitViewInY(vTop, 10)

# run main loop
renderer.mainLoop(SCENEGRAPH)
