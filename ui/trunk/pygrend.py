#
# core
#
import pygame
from pygame.locals import *
from types import *

class Rect:
    def __init__(self,
                 pos=(0, 0),
                 dims=(32, 32)):
        self.pos=pos
        self.dims=dims

def GetRectPos(rect):
    return rect.pos() if isinstance(rect.pos,  FunctionType) else rect.pos
def GetRectDims(rect):
    return rect.dims() if isinstance(rect.dims,  FunctionType) else rect.dims
def HitTest(rect,  mouse_pos):
    x = mouse_pos[0]
    y = mouse_pos[1]
    pos =GetRectPos(view.rect)
    dims =GetRectDims(view.rect)
    x1 = pos[0]
    x2 = pos[0]+ dims[0]
    y1 = pos[1]
    y2 = pos[1]+ dims[1]
    if x >= x1 and x <= x2 and \
       y >= y1 and y <= y2:
        return True
    else:
        return False

class View:
    def __init__(self,
                 rect = None,
                 text='', 
                 color=(255,255,255, 255*0.2)):
        self.rect = rect
        self.text = text
        self.color=color
    def processEvents(self,  events):
        return

class System:
    def __init__(self):
        self.FONT = None
        self.clock = None
        self.SCREEN_SIZE = None
        self.screen = None
        self.running = True

# ### PyGame interface ###
def InitPyGame(system):
    pygame.init()
    pygame.font.init()
    system.FONT = pygame.font.Font('fonts/bitstream.ttf', 12)
    system.clock = pygame.time.Clock()
    system.SCREEN_SIZE = (800, 500)
    system.screen = pygame.display.set_mode(system.SCREEN_SIZE)
    pygame.display.set_caption('DisplayNode')
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(
        [QUIT, KEYUP, KEYDOWN, \
         VIDEORESIZE, VIDEOEXPOSE, MOUSEMOTION, \
         MOUSEBUTTONUP, MOUSEBUTTONDOWN])

def clearScreen(system):
    system.screen.fill((0, 0, 0))

def clockTick(system):
    return system.clock.tick()

def updateScreen():
    pygame.display.update()

def filterEvents():
    events = pygame.event.get()
    filteredEvents = []
    if events != []:
        i = 0
        mouse_motion_events = []
        for event in events:
            if (event.type == pygame.MOUSEMOTION):
                mouse_motion_events.append(event)
            elif ( event.type == pygame.QUIT):
                return [pygame.QUIT]
            else:
                filteredEvents.append(event)
            i += 1
        if (mouse_motion_events != []):
            filteredEvents.append(mouse_motion_events[len(mouse_motion_events)-1])
    return filteredEvents

# lowlevel pygame rect
def __draw_rounded_rect( 
                      rect, 
                      color = (0, 0, 0, 255 * 0.8),
                      boarder = 15,
                      boarder_color = (0,0,0,255),
                      corner = 5):
    rect.topleft = (0, 0)
    surf = pygame.Surface(rect.size, SRCALPHA)
    # draw circles in corners
    pygame.draw.circle(surf, boarder_color, (corner, corner), corner)
    pygame.draw.circle(surf, boarder_color, (corner, rect.height - corner), corner)
    pygame.draw.circle(surf, boarder_color, (rect.width - corner, corner), corner)
    pygame.draw.circle(surf, 
                       boarder_color, 
                       (rect.width - corner, rect.height - corner), 
                       corner)
    # draw two rect that combine to create big rect with corners cut out
    surf.fill(boarder_color, pygame.Rect(corner, 0, rect.width - corner * 2, rect.height))
    surf.fill(boarder_color, pygame.Rect(0, corner, rect.width, rect.height - corner * 2))
    
    pygame.draw.circle(surf, color, (corner+boarder, corner+boarder), corner)
    pygame.draw.circle(surf, color, (corner+boarder, rect.height - corner - boarder), corner)
    pygame.draw.circle(surf, color, (rect.width - corner - boarder, corner + boarder), corner)
    pygame.draw.circle(surf, color, 
                       (rect.width - corner - boarder, rect.height - corner - boarder), 
                       corner)
    surf.fill(color, 
              pygame.Rect(
               corner+boarder, 
               boarder, 
               rect.width - (corner * 2) - (boarder * 2), 
               rect.height - (boarder * 2)))
    surf.fill(color, 
              pygame.Rect(
               boarder, corner+boarder, 
               rect.width-(boarder*2), 
               rect.height - (corner * 2) - (boarder*2)))
    return surf

def drawView(system, view):
    text = view.text
    x, y = GetRectPos(view.rect)
    w, h = GetRectDims(view.rect)
    color = view.color
    if (text != ''):
        surface = system.FONT.render(text, True, (255, 255, 255))
        surface_rect = surface.get_rect()
        h_padding = (h/2) -  round(surface_rect.height/2.0)
        w_padding = h_padding
        new_width = surface_rect.width+(h_padding*2)
        if ( w > new_width): 
            new_width = w
            w_padding = (w/2) - round(surface_rect.width/2.0)
        rect = pygame.Rect(0, 0, new_width,  h)
        rounded_surface = __draw_rounded_rect(rect, color)
        rounded_surface.blit(surface, (w_padding, h_padding))
    else:
        rect = pygame.Rect(0, 0, w, h)
        rounded_surface = __draw_rounded_rect(rect, color)
    system.screen.blit(rounded_surface, (x, y))

# ### end PyGame interface ###
# ### mainLoop helpers: Event processing and rendering ###
# processEvents acts on sg and builds and returns flat sg of views for rendering
def processEvents(events,  sg):
    for (k, v) in sg.iteritems():
        v[0].processEvents(events)
        if (v[1] != []):
            processEvents(events,  v[1])
def render(system,  sg):
    clearScreen(system)
    clockTick(system)
    f = lambda dic: [drawView(system,  v[0]) for (k, v) in dic.iteritems()]
    f(sg)
    updateScreen()
# ### end Renderer ###
DaSys = System()

# sg[id]= (view, children)
SceneGraph = dict([])

# ### init
InitPyGame(DaSys)

# #######################
v1 = View(rect = Rect(dims = (800, 500)))
# #######################
SceneGraph['v1']= (v1,  [])
# #######################

# ### MAIN LOOP ####
def mainLoop(system,  sg):
    while(system.running):
        events = filterEvents()
        if pygame.QUIT in events:
            system.running = False
        else:
            processEvents(events,  sg)
            render(system,  sg)

mainLoop(DaSys,  SceneGraph)
