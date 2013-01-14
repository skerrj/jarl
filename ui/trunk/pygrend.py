#
# core
#
import pygame
from pygame.locals import *
from types import *

class Renderer:
  def __init__(self):
    pygame.init()
    pygame.font.init()
    self.FONT = pygame.font.Font('fonts/bitstream.ttf', 12)
    self.clock = pygame.time.Clock()
    self.SCREEN_SIZE = (800, 600)
    self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
    pygame.display.set_caption('DisplayNode')
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(
        [QUIT, KEYUP, KEYDOWN, \
         VIDEORESIZE, VIDEOEXPOSE, MOUSEMOTION, \
         MOUSEBUTTONUP, MOUSEBUTTONDOWN])
    self.running = True
  def __clearScreen(self):
      self.screen.fill((0, 0, 0))
  def __clockTick(self):
      return self.clock.tick()
  def __updateScreen(self):
      pygame.display.update()
  def __filterEvents(self):
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
  def __draw_rect(self,
                  rect, 
                  color = (0, 0, 0, 255 * 0.8),
                  boarder = 2,
                  boarder_color = (0,0,0,255)):
      rect.topleft = (0, 0)
      surf = pygame.Surface(rect.size, SRCALPHA)
      surf.fill(boarder_color, pygame.Rect(0, 0, rect.width, rect.height))
      surf.fill(color, pygame.Rect(
                                   boarder, boarder, 
                                   rect.width - (boarder * 2), 
                                   rect.height - (boarder * 2)))
      return surf
  def __drawView(self, view):
      text = view.text
      x, y = view.rect.GetPos()
      w, h = view.rect.GetDims()
      color = view.color
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
          rect_surface = self.__draw_rect(rect, color,  view.boarder,  view.boarder_color)
          rect_surface.blit(surface, (w_padding, h_padding))
      else:
          rect = pygame.Rect(0, 0, w, h)
          rect_surface = self.__draw_rect(rect, color,  view.boarder,  view.boarder_color)
      self.screen.blit(rect_surface, (x, y))
  def __processEvents(self, events,  sg):
      for (k, v) in sg.iteritems():
          v.processEvents(events)
  def __render(self,  sg):
      self.__clearScreen()
      self.__clockTick()
      for (k, v) in sg.iteritems():
          print v.name
          self.__drawView(v)
      self.__updateScreen()
  def mainLoop(self,  sg):
      while(self.running):
          events = self.__filterEvents()
          if pygame.QUIT in events:
              self.running = False
          else:
              self.__processEvents(events, sg.getGraph())
              self.__render(sg.getGraph())


