import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import utils.utils
from utils.utils import *

import pygrend
 
import super_display
 
class Display(super_display.SuperDisplay):
    def __init__(self):
        #super(Display,  self).__init__()
        super_display.SuperDisplay.__init__(self)
    def run(self):
        while (True):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_background()
            #self.textview()
            pygame.display.flip()
