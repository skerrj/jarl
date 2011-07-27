import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import utils.utils
from utils.utils import *

import pygrend
 
SCREEN_SIZE = (800, 600)
#SCREEN_SIZE = (0, 0)

FACTOR1 = 0.2
FACTOR2 = 0.3

DARK_ORDER = [-5,-4,-3,-2,-1,5,4,3,2,1,0]
DARK_COLOR1 = [FACTOR1,FACTOR1,FACTOR1,0.7]
DARK_COLOR2 = [FACTOR2,FACTOR2,FACTOR2,0.8]
 
class SuperDisplay:
    def __init__(self):
        self.order = DARK_ORDER
        self.color1 = DARK_COLOR1
        self.color2 = DARK_COLOR2
        self.fonts = {}
        pygame.init()
        pygame.font.init()
        self.font = self.get_font(28)
        self.flags = HWSURFACE|OPENGL|DOUBLEBUF|RESIZABLE#|FULLSCREEN
        self.screen = pygame.display.set_mode(SCREEN_SIZE, self.flags)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.projection_setup()
        self.gl_setup()
        pygame.display.set_caption('Display')
        #
    def get_font(self, size, bold = False):
        key = (size, bold)
        if not key in self.fonts:
            if bold:
                font_name = 'fonts/bitstream_bold.ttf'
            else:
                font_name = 'fonts/bitstream.ttf'
            self.fonts[key] = pygame.font.Font(font_name, size)
        return self.fonts[key]
        #
    def projection_setup(self):
        """Setup viewport and perspective - each time the window is resized."""
        glViewport(0, 0, self.width, self.height)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #
        gluPerspective(45.0, (self.width / float(self.height)), 0.1, 100.0) 
        glMatrixMode(GL_MODELVIEW)
        #
    def gl_setup(self):
        #
        glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
        glShadeModel( GL_SMOOTH )
        glEnable(GL_TEXTURE_2D)
        #
        glClearColor(.0, .0, .0, .0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        self.order = DARK_ORDER
        self.color1 = DARK_COLOR1
        self.color2 = DARK_COLOR2
        #
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
    def textview(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width - 1.0, 0.0, self.height, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def draw_background(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
        #
        glMatrixMode(GL_MODELVIEW)        
        glLoadIdentity()
        #
        #glDisable(GL_DEPTH_TEST)
        #
        Back_Z = 0.0
        back_x_size = 1.0
        back_y_size = 0.5
        back_division = 0.4
        #
        back_colors = ((0.4,), (0.3,), (0.4,), (.6,))
        #
        glBegin(GL_QUADS)
        glColor3f(*(back_colors[3]*3));
        glVertex2f( 0.0, back_division);
        glVertex2f( 1.0, back_division);
        glColor3f(*(back_colors[2]*3));
        glVertex2f( 1.0, 0.0);
        glVertex2f( 0.0, 0.0);
        glEnd()
        #
        glBegin(GL_QUADS)
        glColor3f(*(back_colors[1]*3));
        glVertex2f( 0.0, 1.0);
        glVertex2f( 1.0, 1.0);
        glColor3f(*(back_colors[0]*3));
        glVertex2f( 1.0, back_division);
        glVertex2f( 0.0, back_division);
        glEnd()
