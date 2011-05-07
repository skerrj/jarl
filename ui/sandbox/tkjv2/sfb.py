#!/usr/bin/env python

from socket import getfqdn
from stat import *
import getopt
from fnmatch import fnmatch
import mutex
import os
import re
import sys
import thread
import time

from Tkinter import *
from tkMessageBox import askyesno, showerror, showinfo, showwarning
from tkSimpleDialog import askinteger, askstring

OSNAME     = os.name
OSPLATFORM = sys.platform

import grp
import pwd

CLRHIST       = '<Control-y>'              # Clear Command History
FONTDECR      = '<Control-bracketleft>'    # Decrease Font Size
FONTINCR      = '<Control-bracketright>'   # Increase Font Size
MOUSECTX      = '<ButtonRelease-3>'        # Pop-up Command Menu
MOUSEDIR      = '<Shift-ButtonRelease-3>'  # Pop-up Directory Menu
MOUSEHIST     = '<Shift-Control-ButtonRelease-3>' # Pop-up History Menu
MOUSESC       = '<Alt-Control-ButtonRelease-1>'    # Pop-up Shortcut Menu
MOUSESORT     = '<Alt-Shift-ButtonRelease-3>'     # Pop-up Sort Menu
KEYPRESS      = '<KeyPress>'               # Any keypress (for commands)
QUITPROG      = '<Control-q>'              # Quit the program
READCONF      = '<Control-r>'              # Re-read the configuration file
REFRESH       = '<Control-l>'              # Refresh screen
TOGAUTO       = '<Control-o>'              # Toggle autorefreshing
TOGDETAIL     = '<Control-t>'              # Toggle detail view
TOGLENGTH     = '<Control-0>'              # Toggle length display between actual and normalized
TOGSYMDIR     = '<Control-asciitilde>'     # Toggle sorting of symbolic links pointing to directories
TOGSYMEXPAND  = '<Control-exclam>'         # Toggle symbolic link expansion
TOGSYMRESOLV  = '<Control-at>'             # Toggle absolute symbolic link resolution
TOGWIN32ALL   = '<Control-w>'              # Toggle win32all features, if available

# Directory Navigation

CHANGEDIR   = '<Control-x>'              # Enter a new path
DIRHOME     = '<Control-h>'              # Goto $HOME
DIRBACK     = '<Control-b>'              # Goto previous directory
DIRROOT     = '<Control-j>'              # Goto root directory
DIRSTART    = '<Control-s>'              # Goto starting directory
DIRUP       = '<Control-u>'              # Go up one directory level
DRIVELIST   = '<Control-k>'              # On Win32, display Drive List View if possible
MOUSEBACK   = '<Control-Double-ButtonRelease-1>'  # Go back one directory with mouse
MOUSEUP     = '<Control-Double-ButtonRelease-3>'  # Go up one directory with mouse

# Selection Keys

SELALL      = '<Control-comma>'          # Select all items
SELINV      = '<Control-i>'              # Invert the current selection
SELNONE     = '<Control-period>'         # Unselect all items
SELNEXT     = '<Control-n>'              # Select next item
SELPREV     = '<Control-p>'              # Select previous item
SELEND      = '<Control-e>'              # Select bottom item
SELTOP      = '<Control-a>'              # Select top item

RUNCMD      = '<Control-z>'              # Run arbitrary user command
SELKEY      = '<Return>'                 # Select item w/keyboard
MOUSESEL    = '<Double-ButtonRelease-1>' # Select item w/mouse

HEIGHT   = 600
WIDTH    = 800
STARTX   = 0
STARTY   = 0

BCOLOR  = "black"
FCOLOR  = "green"

#####
# Default Display Fonts
#####

# Main Display Font

FNAME = "Courier"
FSZ   = 12
FWT   = "bold"

# Menu Font

MFNAME = "Courier"
MFSZ   = 12
MFWT   = "bold"

# Help Screen Font

HFNAME = "Courier"
HFSZ   = 10
HFWT   = "italic"


ACTUALLENGTH    = False           # Show actual file lengths
ADAPTREFRESH    = True            # Dynamically adjust refresh intervals
AFTERCLEAR      = True            # Clear all selections following REFRESHAFTER
AFTERWAIT       = 1               # Seconds to wait before REFRESHAFTER
AUTOREFRESH     = True            # Automatically refresh the directory display?
CMDMENUSORT     = False           # Sort the command menu?
CMDSHELL        = ""              # No CMDSHELL processing
DEBUGLEVEL      = 0               # No debug output
DEFAULTSEP      = "==>"           # Default separator in PROMPT and YES definitions
DOTFILE         = '.'             # Leading string of files suppressed by HIDEDOTFILES
FORCEUNIXPATH   = False           # Force Unix path separators regardless of OS
HIDEDOTFILES    = False           # Suppress display of files begining with DOTFILE
INVERTFILTER    = False           # Invert wildcard filtering logic
ISODATE         = False           # Display date/time in ISO 8601 Format
MAXMENU         = 32              # Maximum length of displayed menu
MAXMENUBUF      = 250             # Maximum size of internal menu buffer
MAXNESTING      = 32              # Maximum depth of nested variable definitions
NODETAILS       = False           # True means details can never be displayed
NONAVIGATE      = False           # True means that all directory navigation is prevented
QUOTECHAR       = '\"'            # Character to use when quoting Built-In Variables
REFRESHINT      = 5000            # Interval (ms) for automatic refresh
SCALEPRECISION  = 1               # Precision of scaled length representation
SORTBYFIELD     = "Name"          # Field to use as sort key
SORTREVERSE     = False           # Reverse specified sort order?
SORTSEPARATE    = True            # Separate Directories and Files in sorted displays?
SYMDIR          = True            # Sort symlinks pointing to directories as directories
SYMEXPAND       = True            # Expand symlink to show its target
SYMRESOLV       = False           # Show absolute path of symlink target
USETHREADS      = False           # Use threads on Unix?
USEWIN32ALL     = True            # Use win32all features if available?
WARN            = True            # Warnings on?
WILDNOCASE      = False           # Turns on case-insensitive wildcard matching
WIN32ALLON      = True            # Flag for toggling win32all features while running

CMDESCAPE     = '"'             # Character to force literal dialog processing
CMDSHELLESC   = CMDESCAPE       # Disable CMDSHELL processing for a  manual command entry
KB            = 1024            # 1 KB constant
MB            = KB * KB         # 1 MB constant
GB            = MB * KB         # 1 GB constant
HOMEDIRMARKER = '~'             # Shortcut string used to indicate home directory
NUMFUNCKEY    = 12              # Number of function keys
NUMPROGMEM    = 12              # Number of program memories
POLLINT       = 250             # Interval (ms) the poll routine should run
PSEP          = os.sep          # Character separating path components
REFRESHINDI   = "*"             # Titlebar character used to indicate refresh underway
REFRESHAFTER  = '+'             # Indicate we want a refresh after a command runs
SHOWDRIVES    = '\\\\'          # Logical directory name for Win32 Drive Lists
STRICTMATCH   = CMDESCAPE       # Tells wildcard system to enforce strict matching
STRIPNL       = '-'             # Tells variable execution to replace newlines with spaces
TTLMAXDIR     = 60              # Maximum length of current directory path to show in titlebar
TTLDIR2LONG   = "..."           # String to place at front of long dir paths in titlebar

fNONE        = "No Sort"
fPERMISSIONS = "Permissions"
fLINKS       = "Links"
fOWNER       = "Owner"
fGROUP       = "Group"
fLENGTH      = "Length"
fDATE        = "Time"
fNAME        = "Name"

dlvNONE      = "No Sort"
dlvLABEL     = "Label/Share"
dlvTYPE      = "Drive Type"
dlvFREE      = "Free Space"
dlvTOTAL     = "Total Space"
dlvLETTER    = "Drive Letter"

fREVERSE     = "Reverse"
fSEPARATE    = "Separate"

Name2Key = {}
index = -1

for x, y in [(fNONE, dlvNONE), (fPERMISSIONS, dlvLABEL), (fLINKS, dlvTYPE), (fOWNER, dlvFREE),
             (fGROUP, dlvTOTAL), (fLENGTH, dlvLETTER), (fDATE, None), (fNAME, None),
             (fREVERSE, fREVERSE), (fSEPARATE, None)]:
    Name2Key[x.lower()] = (index, x, y)
    index += 1

MAXDLVKEY = 4

STARTDIR = os.path.abspath("." + os.sep)

ENVHOME = os.getenv("HOME")
HOME = ENVHOME or STARTDIR

HOSTNAME = os.getenv("HOSTNAME") or getfqdn()

USERNAME = os.getenv("USER")

if USERNAME:
    FULLNAME = "%s@%s" % (USERNAME, HOSTNAME)
else:
    FULLNAME = HOSTNAME

CMDMENU_WIDTH = 16


ROOTBORDER    =  1
MENUBORDER    =  2
MENUPADX      =  2
MENUOFFSET    = ROOTBORDER + MENUBORDER + MENUPADX

ShiftMask     = (1<<0)
LockMask      = (1<<1)
ControlMask   = (1<<2)
Mod1Mask      = (1<<3)
Mod2Mask      = (1<<4)
Mod3Mask      = (1<<5)
Mod4Mask      = (1<<6)
Mod5Mask      = (1<<7)
Button1Mask   = (1<<8)
Button2Mask   = (1<<9)
Button3Mask   = (1<<10)
Button4Mask   = (1<<11)
Button5Mask   = (1<<12)

DontCareMask  = LockMask | Mod2Mask | Mod3Mask | Mod4Mask | Mod5Mask
    
AltMask = Mod1Mask

NOREBIND =  ["MOUSECTX", "MOUSEDIR", "MOUSEHIST", "MOUSESC", "MOUSESORT", "MOUSEWILDFILTER", "MOUSEWILDSEL", "MOUSEBACK","MOUSEUP", "MOUSESEL"]

FILEGROUP     = "group"
FILEOWNER     = "owner"
NODRIVE       = "<Drive Empty>"
NOLABEL       = "<No Label>"
SYMPTR        = " -> "
UNAVAILABLE   = "Unavailable"
WIN32GROUP    = "win32" + FILEGROUP
WIN32OWNER    = "win32" + FILEOWNER
WIN32FREE     = "free"
WIN32TOTAL    = "total  "        # Leave trailing space - drive letter follows

MAX_SZ_CHARS      = 17    # Number of digits needed to display max drive/file size - including commas
SZ_TRAILING_SPACE = 2     # Number of trailing spaces to add after a drive/file size field.

MAX_SZ_FIELD  =  MAX_SZ_CHARS + SZ_TRAILING_SPACE  # Biggest a drive/file size string can be

ST_MONTHS     = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04",
                 "May":"05", "Jun":"06", "Jul":"07", "Aug":"08",
                 "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"
                }

ST_PERMIT     = ["---", "--x", "-w-", "-wx",
                 "r--", "r-x", "rw-", "rwx"]


ST_SPECIALS   = {"01":"p", "02":"c", "04":"d", "06":"b",
                 "10":"-", "12":"l", "14":"s"}

ST_SZMODE     = 12
ST_SZNLINK    = 5
ST_SZUNAME    = 18
ST_SZGNAME    = 18
ST_SZLEN      = MAX_SZ_FIELD
ST_SZMTIME    = 18

ST_SZTOTAL    = ST_SZMODE + ST_SZNLINK + ST_SZUNAME + ST_SZGNAME + \
                ST_SZLEN + ST_SZMTIME

STICKY_MASK   = 1
SETGID_MASK   = 2
SETUID_MASK   = 4

ASSIGN      = "="               # Assignment for variable definitions
ASSOCBLANK  = "RESETASSOC"      # Internally used to indicate a blank ASSOC RHS
ASSOCDFLT   = "*"               # Symbol for default association action
ASSOCEXCL   = "!"               # Symbol for association exclusion action
ASSOCIATE   = "ASSOC"           # Association keyword
ASSOCNOCASE = "/"               # Introducer used to indicate case-insensitive ASSOCiations
CONF        = ""                # Config file user selected with -c option
COMMENT     = r"#"              # Comment introducer string
ENVVBL      = r'$'              # Symbol denoting an environment variable
FAKEFIELD   = r'#FAKEFIELD'     # Unsplittable field used to preserve PROMPT/YESNO content
STARTUP     = r'Starting Up'    # Used when doing parse of first config file
VAREXECUTE  = r'`'              # Indicate we want content of variable name to be executed


# Names Of Conditionals, Directives, And Pre-Defined Symbols

CONDENDIF    = '.endif'
CONDEQUAL    = '=='
CONDIF       = '.if'
CONDNOTEQUAL = '!='
DIRECTINC    = '.include'
SYMOS        = '.OS'
SYMPLATFORM  = '.PLATFORM'

# Globals Supporting Configutration File Conditional Processing

ConditionalStack  = []         # Stack for tracking conditional state


# Variable Name Pattern Matching Stuff

DIRSC      = "DIRSC"                            # Directory Shortcut naming
reDIRSC    = r'^' + DIRSC + r'([1-9]|1[0-2])$'  # Regex describing Directory Shortcut names
rePROMPT   = r'\+{PROMPT:.*?\}'                 # Regex describing prompt builtin
reVAR      = r"\[.+?\]"                         # Regex describing variable notation
reYESNO    = r'\{YESNO:.*?\}'                   # Regex describing yes or no builtin
WILDFILTER = "WILDFILTER"                       # Configuration statement for pre-loading Filter list
WILDSELECT = "WILDSELECT"                       # Configuration statement for pre-loading Selection list


# Create actual regex matching engines

REDIRSC    = re.compile(reDIRSC)
REPROMPT   = re.compile(rePROMPT)
REVAR      = re.compile(reVAR)
REYESNO    = re.compile(reYESNO)
CONDVAR    = re.compile(r'^' + reVAR + r'$')

# Built-In Variables

DIR         = r'[DIR]'
DSELECTION  = r'[DSELECTION]'
DSELECTIONS = r'[DSELECTIONS]'
HASH        = r'[HASH]'
MEM1        = r'[MEM1]'
MEM2        = r'[MEM2]'
MEM3        = r'[MEM3]'
MEM4        = r'[MEM4]'
MEM5        = r'[MEM5]'
MEM6        = r'[MEM6]'
MEM7        = r'[MEM7]'
MEM8        = r'[MEM8]'
MEM9        = r'[MEM9]'
MEM10       = r'[MEM10]'
MEM11       = r'[MEM11]'
MEM12       = r'[MEM12]'
PROMPT      = r'{PROMPT:'
SELECTION   = r'[SELECTION]'
SELECTIONS  = r'[SELECTIONS]'
YESNO       = r'{YESNO:'

# Shortcuts to the builtins available in RUNCMD

RUNCMD_SC = {"[D]"  : DIR,
             "[DN]" : DSELECTION,
             "[DS]" : DSELECTIONS,
             "[SN]" : SELECTION,
             "[SS]" : SELECTIONS,
             "[1]"  : MEM1,
             "[2]"  : MEM2,
             "[3]"  : MEM3,
             "[4]"  : MEM4,
             "[5]"  : MEM5,
             "[6]"  : MEM6,
             "[7]"  : MEM7,
             "[8]"  : MEM8,
             "[9]"  : MEM9,
             "[10]" : MEM10,
             "[11]" : MEM11,
             "[12]" : MEM12
             }
              

#----------------------------------------------------------#
#            Prompts, & Application Strings                #
#----------------------------------------------------------#


#####
# Menu, Error, Information, & Warning  Messages
#####

# Title-Bar Strings

TTLAUTO       = "Auto:"
TTLHIDEDOT    = "HideDot:"
TTLFILES      = "Files:"
TTLFILTER     = "Filter:"
TTLSIZE       = "Size:"
TTLSORTFLD    = "Sort:"
TTLSORTREV    = "Rev:"
TTLSORTSEP    = "Sep:"
TTLSYMLINKS   = "Symlinks:"


# Convert Logical Values Into Yes/No String

YesOrNo       = {True:"Y", False:"N"}


# Menu Button Titles

COMMANDMENU   = 'Commands'        # Title for Command Menu button
DIRMENU       = 'Directories'     # Title for Directory Menu button
HISTMENU      = 'History'         # Title for History Menu button
SCMENU        = 'Shortcuts'       # Title for Shortcut Menu button
SORTMENU      = 'Sorting'         # Title for Sort Menu button
FILTERMENU    = 'Filter'          # Title for Wildcard Filter Menu button
SELECTMENU    = 'Select'          # Title for Wildcard Selection Menu button
HELPMENU      = 'Help'            # Title for Help Menu button

# Sort Menu-Related

# And their names - used in Sorting Menu

sSORTBY        = "Sort By"
sREVERSE       = "Reverse Sort"
sSEPARATE      = "Separate Dirs/Files"

def ErrMsg(emsg):
    #showerror(PROGNAME + " " + VERSION + "    " + eERROR, emsg)
    error_string = PROGNAME + " " + VERSION + "    " + eERROR, emsg
    print error_string

def PadString(string, width, Rjust=False, Trailing=0):

    s = string[:(width-1)]
    if Rjust:
        s = s.rjust(width)
    else:
        s = s.ljust(width)

    # Rotate 'Trailing' number of spaces from left of string to right
    
    while (Trailing > 0) and (s[0] == ' ') :
        s = s[1:] + ' '
        Trailing -= 1

    return s

# End of 'PadString()'


#####
# Setup The GUI Visual Parameters, Menus, & Help Information 
#####

def SetupGUI():
    # Rebind all the handlers
    UI.BindAllHandlers()

    UI.DirList.config(font=(FNAME, FSZ, FWT),
                      foreground=FCOLOR, background=BCOLOR)
    UIroot.geometry("%sx%s+%s+%s" % (WIDTH,  HEIGHT, STARTX, STARTY))
# End of 'SetupGUI()'

#####
# Convert A String In Integer Or Hex Format To An Equivalent Numeric
# We assume that the string is either in correct format or that
# the calling routine will catch any error.
#####

def StringToNum(string):

    if string.lower().startswith('0x'):
        value = int(string, 16)
    else:
        value = int(string, 10)

    return value

# End of 'StringToNum()


######
## Strip Trailing Path Separator
######

def StripPSEP(s):

    if s and s[-1] == PSEP:
        return s[:-1]
    else:
        return s

# End of 'StripPSEP()'

#####
# Enacapsulate the UI in a class
#####


class twanderUI:

    def __init__(self, root):

        # Setup the Directory Listing and Scrollbars

        self.hSB = Scrollbar(root, orient=HORIZONTAL)
        self.vSB = Scrollbar(root, orient=VERTICAL)
        self.DirList = Listbox(root, selectmode=EXTENDED, exportselection=0,
                               xscrollcommand=self.hSB.set, yscrollcommand=self.vSB.set)

        # Make them visible by packing
        
        self.hSB.config(command=self.DirList.xview)
        self.hSB.pack(side=BOTTOM, fill=X)
        self.vSB.config(command=self.DirList.yview)
        self.vSB.pack(side=RIGHT, fill=Y)
        self.DirList.pack(side=LEFT, fill=BOTH, expand=1)

        # End of method 'twanderUI.__init__()'

    ###
    # Bind the relevant event handlers
    ###
        
    def BindAllHandlers(self):
        # Bind handler to invoke Decrement Font Size
        self.DirList.bind(self.KeyBindings["FONTDECR"], FontDecr)

        # Bind handler to invoke Increment Font Size
        self.DirList.bind(self.KeyBindings["FONTINCR"], FontIncr)

        # Bind handler to invoke Command Menu
        self.DirList.bind(self.KeyBindings["MOUSECTX"], MouseClick)

        # Bind handler to invoke Directory Menu
        self.DirList.bind(self.KeyBindings["MOUSEDIR"], MouseClick)

        # Bind handler to invoke Directory Menu
        self.DirList.bind(self.KeyBindings["MOUSEHIST"], MouseClick)

        # Bind handler to invoke Directory Menu
        self.DirList.bind(self.KeyBindings["MOUSESC"], MouseClick)

        # Bind handler to invoke Directory Menu
        self.DirList.bind(self.KeyBindings["MOUSESORT"], MouseClick)

        # Bind handler for individual keystrokes
        self.DirList.bind(self.KeyBindings["KEYPRESS"], KeystrokeHandler)

        # Bind handler for "Quit Program"
        self.DirList.bind(self.KeyBindings["QUITPROG"], KeyQuitProg)

        # Bind handler for "Refresh Screen" 

        # Bind handler for "Previous Dir"
        self.DirList.bind(self.KeyBindings["DIRBACK"], KeyBackDir)

        # Bind handler for "Up Dir"
        self.DirList.bind(self.KeyBindings["DIRUP"], KeyUpDir)

        # Bind handler for "Mouse Back Dir"
        self.DirList.bind(self.KeyBindings["MOUSEBACK"], MouseDblClick)

        # Bind handler for "Mouse Up Dir"
        self.DirList.bind(self.KeyBindings["MOUSEUP"], MouseDblClick)

        # Bind handler for "Select No Items"
        self.DirList.bind(self.KeyBindings["SELNONE"], KeySelNone)

        # Bind handler for "Run Command"
        self.DirList.bind(self.KeyBindings["RUNCMD"], lambda event : KeyRunCommand(event, DoCmdShell=True))

        # Bind handler for "Item Select"
        self.DirList.bind(self.KeyBindings["SELKEY"], DirListHandler)

        # Bind handler for "Mouse Select"
        self.DirList.bind(self.KeyBindings["MOUSESEL"], MouseDblClick)


        # Give the listbox focus so it gets keystrokes
        self.DirList.focus()

    # End Of method 'twanderUI.BindAllHandlers()

    #####
    # Return name of currently selected item
    #####

    def LastInSelection(self):

        nameindex = self.NameFirst
        index = self.DirList.curselection()
        #print ('index: %s, %s' % (index,  index[-1]))
        index_int = int(index[0])
        print 'index: ',   index_int,  index[-1]
        if index:
            return (self.DirList.get(index[-1])[nameindex:].split(SYMPTR)[0],  index_int)
            #return self.DirList.get(index[-1])[nameindex:].split(SYMPTR)[0]
        else:
            return ("", -99)
            #return ""

    # End of method 'twanderUI.LastInSelection()'


    #####
    # Support periodic polling to make sure widget stays
    # in sync with reality of current directory.
    #####

    def poll(self):
#        global POLLCNT
#        POLLCNT += 1
#        print 'poll: ', POLLCNT 
        # If new dir entered via mouse, force correct activation
        if self.MouseNewDir:
            print 'if self.MouseNewDir'
            self.DirList.activate(0)
            self.MouseNewDir = False

        # Do autorefreshing as required

        if AUTOREFRESH:

            # Is it time for a refresh?

            elapsed = int((time.time() - self.LastRefresh) * 1000)
            if elapsed >= REFRESHINT:

                # Don't autorefresh on drive list views
                if UI.CurrentDir != SHOWDRIVES:

                    # Don't autorefresh if there is a lock outstanding

                    if not UI.DirListMutex.test():
                        RefreshDirList(None)

        # Setup next polling event
        self.DirList.after(POLLINT, self.poll)

    # End of method 'twanderUI.poll()'

    #####
    # Set a particular selection, w/bounds checking
    # Note that 'selection' is passed as a string
    # but 'active' is passed as a number.
    #####

    def SetSelection(self, selection, active):
        #print 'UI.SetSelection'
        # Clear all current selection(s)
        self.DirList.selection_clear(0, END)

        # Get current maximum index
        maxindex =  self.DirList.size() - 1

        # And bounds check/adjust

        if active > maxindex:
            active = maxindex

        # Set desired selected items, if any

        if selection:
            for entry in selection:
                self.DirList.select_set(entry)
            self.DirList.see(selection[-1])

        # Now set the active entry
        self.DirList.activate(active)

    # End of method 'twanderUI.SetSelection()'



# End of class definition, 'twanderUI'


#----------------------------------------------------------#
#                   Handler Functions                      #
#----------------------------------------------------------#

#---------------- Mouse Click Dispatchers -----------------#

# We intercept all mouse clicks (of interest) here so it
# is easy to uniquely handle the Control, Shift, Alt,
# variations of button presses.  We use Tkinter itself
# keep track of single- vs. double-clicks and hand-off
# the event to the corresponding Mouse Click Dispatcher.

#####
# Event Handler: Single Mouse Clicks
#####

def MouseClick(event):
    pass

# End Of 'MouseClick()'


#####
# Event Handler: Mouse Double-Clicks
#####

def MouseDblClick(event):

    event.state &= ~DontCareMask                      # Kill the bits we don't care about
    
    if event.state == Button1Mask:                    # Double-Button-1 / No Modifier
        print 'MouseDblClick.button-1.noMod'
        DirListHandler(event)                         # Execute selected item

    elif event.state == (Button1Mask | ControlMask):  # Control-DblButton-1
        KeyBackDir(event)                             # Move back one directory

    elif event.state == (Button3Mask | ControlMask):  # Control-DblButton-3
        KeyUpDir(event)                               # Move up one directory

    return "break"

# End Of 'MouseDblClick()

#####
# Decrement Font Size
#####

def FontDecr(event):
    global FSZ, MFSZ, HFSZ
    
    if FSZ > 1:
        FSZ  -= 1
    if MFSZ > 1:
        MFSZ -= 1
    if HFSZ > 1:
        HFSZ -= 1

    SetupGUI()
    return 'break'

# End of 'FontDecr()'


#####
# Increment Font Size
#####

def FontIncr(event):
    global FSZ, MFSZ, HFSZ

    FSZ  += 1
    MFSZ += 1
    HFSZ += 1

    SetupGUI()
    return 'break'

# End of 'FontIncr()'


#####
# Event Handler: Individual Keystrokes
#####

def KeystrokeHandler(event):
    print 'keyStrokeHandler'
    event.state &= ~DontCareMask                      # Kill the bits we don't care about

    # We *only* want to handle simple single-character
    # keystrokes.  This means that there must be a character
    # present and that the only state modifier permitted
    # is the Shift key
    
    if not event.char or (event.state and event.state != 1):
        return 

# end of 'KeystrokeHandler()'
    

#####
# Event Handler: Program Quit
#####

def KeyQuitProg(event):
    sys.exit()

# End of 'KeyQuitProg()'

#####
# Event Handler: Move To Previous Directory
#####

def KeyBackDir(event):

    # Move to last directory visited, if any - inhibit this from
    # being placed on the directory traversal stack
    if UI.LastDir:
        LoadDirList(UI.LastDir.pop(), 0, save=False)

    # No previous directory
    else:
        pass

    return 'break'

# End of 'KeyBackDir()'

#####
# Event Handler: Move Up One Directory
#####
def KeyUpDir(event):
    print 'KeyUpDir..'
    # Move up one directory level unless we're already at the root
    if UI.CurrentDir != os.path.abspath(PSEP):
        LoadDirList(UI.CurrentDir + "..", 0)

    # Unless we're running on Win32 and we are able to do
    # a Drive List View
#
#    elif OSPLATFORM == 'win32' and GetWin32Drives():
#        LoadDirList(SHOWDRIVES)

    return 'break'
    
# End of 'KeyUpDir()'

#####
# Event Handler: Select No Items
#####
def KeySelNone(event):
    UI.DirList.selection_clear(0, END)

    return 'break'

# End of 'KeySelNone()'

#####
# Event Handler: Process Current Selection
#####
def DirListHandler(event):
    print 'DirListHandler...'
    global UI
    
    # Get current selection.  If none, just return, otherwise process
    selected,  index =  UI.LastInSelection()
    print 'selected: ',  selected
    if not selected:
        return

    # If selection is a directory, move there and list contents.
    if os.path.isdir(os.path.join(UI.CurrentDir, selected)):
        # Build full path name
        selected = os.path.join(os.path.abspath(UI.CurrentDir), selected)

        # Convert ending ".." into canonical path
        if selected.endswith(".."):
            selected = PSEP.join(selected.split(PSEP)[:-2])
        
        # Need to end the directory string with a path
        # separator character so that subsequent navigation
        # will work when we hit the root directory of the file
        # system.  In the case of Unix, this means that
        # if we ended up at the root directory, we'll just
        # get "/".  In the case of Win32, we will get
        # "DRIVE:/".

        if selected[-1] != PSEP:
            selected += PSEP

        # Load UI with new directory
        LoadDirList(selected, index,  save=True)

        # Indicate that we entered a new directory this way.
        # This is a workaround for Tk madness.  When this
        # routine is invoked via the mouse, Tk sets the
        # activation *when this routine returns*.  That means
        # that the activation set at the end of LoadDirList
        # gets overidden.  We set this flag here so that
        # we can subsequently do the right thing in our
        # background polling loop.  Although this routine
        # can also be invoked via a keyboard selection,
        # we run things this way regardless since no harm
        # will be done in the latter case.

        UI.MouseNewDir = True

    return 'break'

# End of 'DirListHandler()'

#####
# Event Handler: Popup Menus
#####
def PopupMenu(menu, x, y):

    # Popup requested menu at specified coordinates
    # but only if the menu has at least one entry.

    if menu.index(END):
        menu.tk_popup(x, y)

# End of 'PopupMenu()'

#####
# Load UI With Selected Directory
#####
def LoadDirList(newdir, index,  save=True, updtitle=True):
    print ('LoadDirList.newdir: %s, %d' %  (newdir,  index))
    newdir = os.path.abspath(newdir)
    # Make sure newdir properly terminated
    if newdir[-1] != PSEP:
        newdir += PSEP
    try:
        contents = BuildDirList(newdir)
    except:
        # If CurrentDir set, we're still there: error w/ recovery
        if UI.CurrentDir:
            ErrMsg(eDIRRD % newdir)
            return
        # If not, we failed on the initial directory: error & abort
        else:
            ErrMsg(eINITDIRBAD % newdir)
            sys.exit(1)
    # Push last directory visited onto the visited stack
    # Are we trying to move back into same directory?
    if os.path.abspath(UI.CurrentDir) == os.path.abspath(newdir):
        save = False
    # Now save if we're supposed to.
    if save and UI.CurrentDir:
        UI.LastDir.append(UI.CurrentDir)
    # And select new directory to visit
    UI.CurrentDir = newdir
    # Wait until we have exclusive access to the widget
    while not UI.DirListMutex.testandset():
        pass
    # Clear out the old contents
    #print 'END: ',  END
    UI.DirList.delete(0,END)
    # Load new directory contents into UI
    for x in contents:
        print 'inserting content: ',  x
        UI.DirList.insert(END, x)
    os.chdir(newdir)
    # Nothing should be pre-selected in the new directory listing
    KeySelNone(None)
    #Release the lock
    UI.DirListMutex.unlock()
# End of 'LoadDirList():

#####
# Return Ordered List Of Directories & Files For Current Root
# Posts A Warning Message If SORTBYFIELD Is Out Of Range
#####
def BuildDirList(currentdir):
    global UI, SORTBYFIELD, REFRESHINT

    # Set time of the refresh
    begintime = time.time()

    # We'll need the nominal refresh interval later
    nominal = UI.OptionsNumeric["REFRESHINT"]

    # Check to see if SORTBYFIELD makes sense

    if SORTBYFIELD.lower() not in Name2Key.keys():
        default = UI.OptionsString["SORTBYFIELD"]
        WrnMsg(wBADSORTFLD % (SORTBYFIELD, default))
        SORTBYFIELD = default
        LoadHelpMenu()

    UI.TotalSize = 0

    fileinfo = []
    dKeys,  fKeys  = {}, {}
    UI.NameFirst = 0

    cwd = os.path.abspath(os.path.curdir)
    os.chdir(currentdir)

    # Get and sort directory contents
    filelist = os.listdir(currentdir)
    keyindex = Name2Key[SORTBYFIELD.lower()][0]
    dList, fList = [], []
    
    for x in range(len(filelist)):
        # Get File/Dir name
        file = filelist[x]

        UI.TotalSize += 3
        dList.append(file)
    dotdot = [".." + PSEP,]

    os.chdir(cwd)
    return dotdot + dList + fList
    
# End of  'BuildDirList()'

#####
# Refresh Contents Of Directory Listing To Stay In Sync With Reality
#####
def RefreshDirList(event, ClearFilterWildcard=False):
    global UI, INVERTFILTER

    # Indicate that we are doing an refresh
    #UI.UpdateTitle(UIroot, refreshing=REFRESHINDI)
    
    # Wait until we have exclusive access to the widget

    while not UI.DirListMutex.testandset():
        pass

    # Clearout any active wildcard filtering if asked to

    if ClearFilterWildcard:
        UI.FilterWildcard = ("None", None, None, False)
        INVERTFILTER = False
        
    # Keep track of current selection and active line *by name*.  This
    # will ensure correct reselection after a refresh where the
    # contents of the directory have changed.  Since this uses simple
    # string matching, the algorithm below has to be sensitive to
    # expanded symbolic links so that the match is made on the symlink
    # name, not it's expansion (which can change by toggling one of
    # the SYM* options).

    selections = []
    for sel in list(UI.DirList.curselection()) + [str(UI.DirList.index(ACTIVE))]:
        selections.append(StripPSEP(UI.DirList.get(sel).split(SYMPTR)[0].split()[-1]))

    # Save current scroll positions

    xs = UI.hSB.get()
    ys = UI.vSB.get()

    # Clean out old listbox contents

    UI.DirList.delete(0,END)

    # Get and load the new directory information, restoring selections
    # and active marker

    try:
        dirlist = BuildDirList(UI.CurrentDir)
        UI.DirList.insert(0, *dirlist)

        # Build list of all file and directory names

        names = []
        for entry in dirlist:
            names.append(StripPSEP(entry.split(SYMPTR)[0].split()[-1]))

        # Get the active entry off the list and convert to an integer index
        
        active = selections.pop()
        try:
            active = names.index(active)
        except:
            active = 0

        # Build a list of strings describing selections, discarding
        # references to files/directories that no longer exist
        
        sellist = []
        for name in selections:
            try:
                sellist.append(str(names.index(name)))
            except:
                pass

        # Restore selection(s)

        UI.SetSelection(sellist, active)

        # Restore scroll positions

        UI.DirList.xview(MOVETO, xs[0])
        UI.DirList.yview(MOVETO, ys[0])


    # Cannot read current directory - probably media removed.
    # Just revert back to the original starting directory
    # This won't work if the original starting directory is
    # no longer readable - i.e. *It* was removed.
    
    except:
        UI.CurrentDir=STARTDIR
        os.chdir(STARTDIR)
        UI.DirList.insert(0, *BuildDirList(UI.CurrentDir))
        KeySelTop(None, clearsel=True)

    # Update titlebar to reflect any changes
    #UI.UpdateTitle(UIroot)

    # Release the mutex
    UI.DirListMutex.unlock()

    return 'break'

# End of 'RefreshDirList()

#----------------------------------------------------------#
#                  Program Entry Point                     #
#----------------------------------------------------------#

#####
# Create an instance of the UI
#####
POLLCNT=0
UIroot = Tk()
UI = twanderUI(UIroot)

# Make the Tk window the topmost in the Z stack.
# 'Gotta do this or Win32 will not return input
# focus to our program after a startup warning
# display.

UIroot.tkraise()

#####
# Setup global UI variables
#####

# Setup Built-In Variables
UI.BuiltIns = {DIR:"", DSELECTION:"", DSELECTIONS:"", HASH:"",
               MEM1:"", MEM2:"", MEM3:"", MEM4:"", MEM5:"", MEM6:"",
               MEM7:"", MEM8:"", MEM9:"", MEM10:"", MEM11:"", MEM12:"", 
               PROMPT:"", SELECTION:"", SELECTIONS:"", YESNO:""}

# Options (and their default values) which can be set in the configuration file

UI.OptionsBoolean = {"ACTUALLENGTH":ACTUALLENGTH,
                     "ADAPTREFRESH":ADAPTREFRESH,
                     "AFTERCLEAR":AFTERCLEAR,
                     "AUTOREFRESH":AUTOREFRESH,
                     "CMDMENUSORT":CMDMENUSORT,
                     "FORCEUNIXPATH":FORCEUNIXPATH,
                     "HIDEDOTFILES":HIDEDOTFILES,
                     "INVERTFILTER":INVERTFILTER,
                     "ISODATE":ISODATE,
                     "NODETAILS":NODETAILS,
                     "NONAVIGATE":NONAVIGATE,
                     "SORTREVERSE":SORTREVERSE,
                     "SORTSEPARATE":SORTSEPARATE,
                     "SYMDIR":SYMDIR,
                     "SYMEXPAND":SYMEXPAND,
                     "SYMRESOLV":SYMRESOLV,
                     "USETHREADS":USETHREADS,
                     "USEWIN32ALL":USEWIN32ALL,
                     "WARN":WARN,
                     "WILDNOCASE":WILDNOCASE,
                     }

UI.OptionsNumeric = {"AFTERWAIT":AFTERWAIT,"DEBUGLEVEL":DEBUGLEVEL, "FSZ":FSZ, "MFSZ":MFSZ, "HFSZ":HFSZ,
                     "HEIGHT":HEIGHT, "MAXMENU":MAXMENU, "MAXMENUBUF":MAXMENUBUF, "MAXNESTING":MAXNESTING,
                     "REFRESHINT":REFRESHINT, "SCALEPRECISION":SCALEPRECISION, "STARTX":STARTX, "STARTY":STARTY, "WIDTH":WIDTH}

UI.OptionsString  = {"BCOLOR":BCOLOR,   "FCOLOR":FCOLOR,   "FNAME":FNAME,   "FWT":FWT,    # Main Font/Colors
#                     "MBCOLOR":MBCOLOR, "MFCOLOR":MFCOLOR, "MFNAME":MFNAME, "MFWT":MFWT,  # Menu Font/Colors
#                     "HBCOLOR":HBCOLOR, "HFCOLOR":HFCOLOR, "HFNAME":HFNAME, "HFWT":HFWT,  # Help Font/Colors
#                     "MBARCOL":MBARCOL, "QUOTECHAR":QUOTECHAR, "SORTBYFIELD":SORTBYFIELD, # Other
                     "STARTDIR":STARTDIR, "CMDSHELL":CMDSHELL, "DEFAULTSEP":DEFAULTSEP, "DOTFILE":DOTFILE} 

# Prepare storage for key bindings
UI.KeyBindings = {}

# Storage For Associations

UI.Associations = {ASSOCEXCL:[]}

# Initialize list of all directories visited
UI.AllDirs    = []

# Initialize directory stack
UI.LastDir    = []

# Initialize storage for last manually entered directory path
UI.LastPathEntered = ""

# Initialize storage for last manually entered Filter and Selection wildcards
UI.LastFiltWildcard = ""
UI.LastSelWildcard = ""

# Initialize storage for current location
UI.CurrentDir = ""

# Initialize storage for filtering wildcard
UI.FilterWildcard = ("None", None, None, False)

# Initialize various menu data structures
#ClearHistory(None)

# Initialize Storage For Program Memories

UI.ProgMem = [[], [], [], [], [], [], [], [], [], [], [], []]

# Need mutex to serialize on widget updates
UI.DirListMutex = mutex.mutex()

# Intialize the "new dir via mouse" flag
UI.MouseNewDir = False

# Initialize the refresh timers
UI.LastRefresh    = 0

# Initialize storage for list of configuration files processed
UI.ConfigVisited = []

UI.KeyBindings = {"CLRHIST":CLRHIST,
                  "FONTDECR":FONTDECR,
                  "FONTINCR":FONTINCR,
                  "MOUSECTX":MOUSECTX,
                  "MOUSEDIR":MOUSEDIR,
                  "MOUSEHIST":MOUSEHIST,
                  "MOUSESC":MOUSESC,
                  "MOUSESORT":MOUSESORT,
                  "KEYPRESS":KEYPRESS,
                  "QUITPROG":QUITPROG,
                  "READCONF":READCONF,
                  "REFRESH":REFRESH,
                  "TOGAUTO":TOGAUTO,
                  "TOGDETAIL":TOGDETAIL,
                  "TOGLENGTH":TOGLENGTH,
                  "TOGSYMDIR":TOGSYMDIR,
                  "TOGSYMEXPAND":TOGSYMEXPAND,
                  "TOGSYMRESOLV":TOGSYMRESOLV,
                  "TOGWIN32ALL":TOGWIN32ALL,
                  "CHANGEDIR":CHANGEDIR,
                  "DIRHOME":DIRHOME,
                  "DIRBACK":DIRBACK,
                  "DIRROOT":DIRROOT,
                  "DIRSTART":DIRSTART,
                  "DIRUP":DIRUP,
                  "DRIVELIST":DRIVELIST,
                  "MOUSEBACK":MOUSEBACK,
                  "MOUSEUP":MOUSEUP,
                  "SELALL":SELALL,
                  "SELINV":SELINV,
                  "SELNONE":SELNONE,
                  "SELNEXT":SELNEXT,
                  "SELPREV":SELPREV,
                  "SELEND":SELEND,
                  "SELTOP":SELTOP,
#                  "PGDN":PGDN,
#                  "PGUP":PGUP,
#                  "PGRT":PGRT,
#                  "PGLFT":PGLFT,
                  "RUNCMD":RUNCMD,
                  "SELKEY":SELKEY,
                  "MOUSESEL":MOUSESEL,
#                  "KDIRSC1":KDIRSC1,
#                  "KDIRSC2":KDIRSC2,
#                  "KDIRSC3":KDIRSC3,
#                  "KDIRSC4":KDIRSC4,
#                  "KDIRSC5":KDIRSC5,
#                  "KDIRSC6":KDIRSC6,
#                  "KDIRSC7":KDIRSC7,
#                  "KDIRSC8":KDIRSC8,
#                  "KDIRSC9":KDIRSC9,
#                  "KDIRSC10":KDIRSC10,
#                  "KDIRSC11":KDIRSC11,
#                  "KDIRSC12":KDIRSC12,
#                  "KDIRSCSET":KDIRSCSET,
#                  "MEMCLR1":MEMCLR1,
#                  "MEMCLR2":MEMCLR2,
#                  "MEMCLR3":MEMCLR3,
#                  "MEMCLR4":MEMCLR4,
#                  "MEMCLR5":MEMCLR5,
#                  "MEMCLR6":MEMCLR6,
#                  "MEMCLR7":MEMCLR7,
#                  "MEMCLR8":MEMCLR8,
#                  "MEMCLR9":MEMCLR9,
#                  "MEMCLR10":MEMCLR10,
#                  "MEMCLR11":MEMCLR11,
#                  "MEMCLR12":MEMCLR12,
#                  "MEMCLRALL":MEMCLRALL,
#                  "MEMSET1":MEMSET1,
#                  "MEMSET2":MEMSET2,
#                  "MEMSET3":MEMSET3,
#                  "MEMSET4":MEMSET4,
#                  "MEMSET5":MEMSET5,
#                  "MEMSET6":MEMSET6,
#                  "MEMSET7":MEMSET7,
#                  "MEMSET8":MEMSET8,
#                  "MEMSET9":MEMSET9,
#                  "MEMSET10":MEMSET10,
#                  "MEMSET11":MEMSET11,
#                  "MEMSET12":MEMSET12,
#                  "SORTBYNONE":SORTBYNONE,
#                  "SORTBYPERMS":SORTBYPERMS,
#                  "SORTBYLINKS":SORTBYLINKS,
#                  "SORTBYOWNER":SORTBYOWNER,
#                  "SORTBYGROUP":SORTBYGROUP,
#                  "SORTBYLENGTH":SORTBYLENGTH,
#                  "SORTBYTIME":SORTBYTIME,
#                  "SORTBYNAME":SORTBYNAME,
#                  "SORTREV":SORTREV,
#                  "SORTSEP":SORTSEP,
#                  "MOUSEWILDFILTER":MOUSEWILDFILTER,
#                  "MOUSEWILDSEL":MOUSEWILDSEL,
#                  "FILTERWILD":FILTERWILD,
#                  "SELWILD":SELWILD,
#                  "TOGFILT":TOGFILT,
#                  "TOGHIDEDOT":TOGHIDEDOT
                  }


# Get starting directory into canonical form
STARTDIR = os.path.abspath(STARTDIR)

# Initialize the UI directory listing
LoadDirList(STARTDIR, 0, updtitle = False)

# Process options to catch any changes detected in
# environment variable or command line

#ProcessOptions()
SetupGUI()
RefreshDirList(None)

# And start the periodic polling of the widget
UI.poll()

# Run the program interface
UIroot.mainloop()

