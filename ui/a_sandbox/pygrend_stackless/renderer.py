#
#
#
import stackless
import pygame
from pygame.locals import *

class Renderer:
    def __init__(self,  renderCh):
        pygame.init()
        pygame.font.init()
        
        self.FONT = pygame.font.Font('fonts/bitstream.ttf', 12)
        #self.scene_graph = {}
        self.scene_graph = []
        self.clock = pygame.time.Clock()
        self.SCREEN_SIZE = (800, 600)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.channel = renderCh
        
        pygame.display.set_caption('DisplayNode')
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(
            [QUIT, KEYUP, KEYDOWN, \
             VIDEORESIZE, VIDEOEXPOSE, MOUSEMOTION, \
             MOUSEBUTTONUP, MOUSEBUTTONDOWN])
    
    def draw_rounded_rect(self,  rect, color = (0, 0, 0, 255 * 0.8)):
        corner = 5
        rect.topleft = (0, 0)
        #print 'draw_rounded_rect.rect.size',  rect.size
        surf = pygame.Surface(rect.size, SRCALPHA)
        # draw circles in corners
        pygame.draw.circle(surf, color, (corner, corner), corner)
        pygame.draw.circle(surf, color, (corner, rect.height - corner), corner)
        pygame.draw.circle(surf, color, (rect.width - corner, corner), corner)
        pygame.draw.circle(surf, color, (rect.width - corner, rect.height - corner), corner)
       # draw two rect that combine to create big rect with corners cut out
        surf.fill(color, pygame.Rect(corner, 0, rect.width - corner * 2, rect.height))
        surf.fill(color, pygame.Rect(0, corner, rect.width, rect.height - corner * 2))
        return surf
    
    def draw_view(self, text,  x,  y,  w=32,  h=32,  color = (0, 0, 0, 255 * 0.8)):
        if (text != ''):
            surface = self.FONT.render(text, True, (255, 255, 255))
            surface_rect = surface.get_rect()
            h_padding = (h/2) -  round(surface_rect.height/2.0)
            w_padding = h_padding
            new_width = surface_rect.width+(h_padding*2)
            if ( w > new_width): 
                new_width = w
                w_padding = (w/2) - round(surface_rect.width/2.0)
            rect = pygame.Rect(0, 0, new_width,  h)
            rounded_surface = self.draw_rounded_rect(rect, color)
            rounded_surface.blit(surface, (w_padding, h_padding))
        else:
            rect = pygame.Rect(0, 0, w, h)
            rounded_surface = self.draw_rounded_rect(rect, color)
        self.screen.blit(rounded_surface, (x, y))
    
    def renderView(self,  v):
        self.draw_view(v.text, v.x,  v.y, v.width,  v.height,  v.color)
    
    def renderTask(self):
        while (True):
            cmd = self.channel.receive()
            if cmd == 'render':
                self.screen.fill((0, 0, 0))
                self.clock.tick()
                #for id, node_sg in self.scene_graph.iteritems():
                    #for v in node_sg:
                #for v in self.scene_graph:
                    #self.draw_view(v.text, v.x,  v.y, v.width,  v.height)
                map(self.renderView,  self.scene_graph)
                self.draw_view(str(self.clock.tick()), 10, 10, w=32)
                self.draw_view('1234567890', 42, 10)
                pygame.display.update()
    
