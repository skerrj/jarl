# -*- coding: utf-8 -*-
#Copyright (C) 2009 Alexandre Inácio Rosenfeld
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import logging
import time
import math
import ConfigParser

import pygame
from pygame.locals import *

class Error(Exception):
    pass


def draw_rounded_rect(rect, border = 20, color = (0, 0, 0, 255 * 0.8)):
    full_rect = rect.inflate(border * 2.0, border * 2.0)
    full_rect.topleft = (0, 0)
    surf = pygame.Surface(full_rect.size, SRCALPHA)
    
    pygame.draw.circle(surf, color, (border, border), border)
    pygame.draw.circle(surf, color, (border, border + rect.height), border)
    pygame.draw.circle(surf, color, (border + rect.width, border), border)
    pygame.draw.circle(surf, color, (border + rect.width, border + rect.height), border)
    surf.fill(color, pygame.Rect(border, 0, rect.width, rect.height + border * 2.0))
    surf.fill(color, pygame.Rect(0, border, rect.width + border * 2.0, rect.height))
    return surf

#def rounded_border_surface(surf, border = 10, color = (0, 0, 0, 255 * 0.8)):
def rounded_border_surface(surf, border = 10, color = (255, 255, 255, 255 * 0.2)):
    rounded_rect = draw_rounded_rect(surf.get_rect(), border, color)
    rounded_rect.blit(surf, (border, border))
    return rounded_rect
#
# end file
#
