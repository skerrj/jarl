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

from OpenGL.GL import *
from OpenGL.GLU import *

class Error(Exception):
    pass

def pil_loader(path):
    """Load an image file as a 2D texture using PIL"""
    from Image import open, NEAREST
    im = open(path).resize((256,256), NEAREST)
    
    texid = glGenTextures(1)
    
    try:
        # get image meta-data (dimensions) and data
        ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
    except SystemError:
        # has no alpha channel, synthesize one, see the
        # texture module for more realistic handling
        ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
            
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    # copy the texture into the current texture ID
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    # return the ID for use
    return (texid, pygame.Rect(0, 0, ix, iy))

IMAGE_CACHE = {}

def pygame_gltexture(surf, txtr = None):
    """Load surface into texture object. Return texture object. 
    @param surf: surface to make texture from.
    """
    if not txtr:
        txtr = glGenTextures(1)
    textureData = pygame.image.tostring(surf, "RGBA", 1)

    glBindTexture(GL_TEXTURE_2D, txtr)
    width, height = surf.get_size()
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, 
      GL_RGBA, GL_UNSIGNED_BYTE, textureData )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    return (txtr, pygame.Rect(0, 0, width, height))

NOT_FOUND = set()

def pygame_loader(filename, cache = None):
    if not cache:
        cache = IMAGE_CACHE
    full_path = os.path.abspath(filename)
    if os.path.exists(full_path):
        filename = full_path
    else:
        if full_path not in NOT_FOUND:
            logging.error("Image %s (%s) not found" % (filename, full_path))
        NOT_FOUND.add(full_path)
        filename = os.path.abspath('noimage.png')
    if filename not in cache:
        image = pygame.image.load(filename)
        texture = pygame_gltexture(image)
        cache[filename] = texture
    txture, rect = cache[filename]
    return txture, pygame.Rect(rect)

def draw_image(image, scale = 100.0, color1 = (1.0, 1.0, 1.0, 1.0), color2 = None):
    texture, rect = image
    #rect.center = (0, 0)
    glScale(1.0/scale, 1.0/scale, 0.0)        
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor4f(*color1)
    glTexCoord2f( 0.0, 0.0 ); glVertex3f( (rect.left), (rect.top),  0.0 )
    glTexCoord2f( 1.0, 0.0 ); glVertex3f( (rect.right), (rect.top),  0.0 )
    if not color2:
        color2 = color1
    glColor4f(*color2)
    glTexCoord2f( 1.0, 1.0 ); glVertex3f( (rect.right),  (rect.bottom),  0.0 )
    glTexCoord2f( 0.0, 1.0 ); glVertex3f( (rect.left),  (rect.bottom),  0.0 )
    glEnd() 
    
def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """
    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            #for word in words:
            #    if font.size(word)[0] >= rect.width:
            #        pass
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size, SRCALPHA) 
    #surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        #if accumulated_height + font.size(line)[1] >= rect.height:
        #    pass
            #raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise Error("Invalid justification argument: %s" % justification)
        accumulated_height += font.size(line)[1]

    return surface

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

def rounded_border_surface(surf, border = 10, color = (0, 0, 0, 255 * 0.8)):
    rounded_rect = draw_rounded_rect(surf.get_rect(), border, color)
    rounded_rect.blit(surf, (border, border))
    return rounded_rect

def text_surface(string, font, rect = None, justification = 0):
    if rect is not None:
        rendered_text = render_textrect(string, font, rect, (255, 255, 255), None, justification)
    else:
        rendered_text = font.render(string, True, (255, 255, 255))
    #if rounded_borders:
    #    rendered_text = rounded_border_surf(rendered_text, 10)    
    return rendered_text

def draw_surface(surface, rect):
    text_data = pygame.image.tostring(surface,"RGBA",1)
    w, h = surface.get_size()
    
    glPushMatrix()
    
    glRasterPos2d(rect.left, rect.top - h)
    glPixelZoom(1,1)
    
    glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    glPopMatrix()
