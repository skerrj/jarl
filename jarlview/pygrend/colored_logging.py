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

import logging
import logging.handlers
import os

#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8) 

def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': GREEN,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    COLOR_FORMAT = formatter_message(FORMAT, True)
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)                

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return

#LOG_FILENAME = os.path.join(os.path.expanduser("~"), "FoG_menu.log")
#LOG_FILENAME = "logs/PyGrenderer.log"
LOG_FILENAME = "PyGrenderer.log"

def move_logs(basename, filename, d = 0):
    if d > 3:
        return
    if os.path.exists(filename):
        new_filename = "%s.%d" % (basename, d)
        move_logs(basename, new_filename, d + 1)
        os.rename(filename, new_filename)
move_logs(LOG_FILENAME, LOG_FILENAME)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s (%(filename)s:%(lineno)d)',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILENAME,
                    filemode='w')

#file_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, 'w', maxBytes=1024*8, backupCount = 5)
#logging.getLogger('').addHandler(file_handler)

FORMAT = "[%(levelname)-19s] %(name)s %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
COLOR_FORMAT = formatter_message(FORMAT, True)

color_formatter = ColoredFormatter(COLOR_FORMAT)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(color_formatter)
logging.getLogger('').addHandler(console)

#logging.setLoggerClass(ColoredLogger)

