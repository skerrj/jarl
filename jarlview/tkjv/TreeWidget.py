# XXX TO DO:
# - popup menu
# - support partial or total redisplay
# - key bindings (instead of quick-n-dirty bindings on Canvas):
#   - up/down arrow keys to move focus around
#   - ditto for page up/down, home/end
#   - left/right arrows to expand/collapse & move out/in
# - more doc strings
# - add icons for "file", "module", "class", "method"; better "python" icon
# - callback for selection???
# - multiple-item selection
# - tooltips
# - redo geometry without magic numbers
# - keep track of object ids to allow more careful cleaning
# - optimize tree redraw after expand of subnode

import os
from Tkinter import *
import imp

import ZoomHeight

class TreeNode:

    def __init__(self, canvas, parent, item):
		self.canvas = canvas
		self.parent = parent
		self.item = item
		self.state = 'collapsed'
		self.selected = False
		self.children = []
		self.x = self.y = None
		self.canvas.bind("<Key-Down>", self.select_next_item)
	
    def select_next_item(self, event=None):
		print 'in select_next_item'
		self.expand()
		# if self.children != []:
			# print 'children not empty'
			# next_child = self.children[0]
			# next_child.select()
	
    def destroy(self):
        for c in self.children[:]:
            self.children.remove(c)
            c.destroy()
        self.parent = None

    def select(self, event=None):
        if self.selected:
            return
        self.deselectall()
        self.selected = True
        self.drawtext()

    def deselect(self, event=None):
        if not self.selected:
            return
        self.selected = False
        self.drawtext()

    def deselectall(self):
        if self.parent:
            self.parent.deselectall()
        else:
            self.deselecttree()

    def deselecttree(self):
        if self.selected:
            self.deselect()
        for child in self.children:
            child.deselecttree()

    def flip(self, event=None):
        #print "in flip...event = ", event
        if self.state == 'expanded':
            self.collapse()
        else:
            self.expand()
        self.item.OnDoubleClick()
        return "break"

    def expand(self, event=None):
        print "in expand...event = ", event
        if not self.item._IsExpandable():
            return
        if self.state != 'expanded':
            self.state = 'expanded'
            self.update()
            self.view()

    def collapse(self, event=None):
        #print "in collapse...event = ", event
        if self.state != 'collapsed':
            self.state = 'collapsed'
	    self.children = []
            self.update()

    def view(self):
        top = self.y - 2
        bottom = self.lastvisiblechild().y + 17
        height = bottom - top
        visible_top = self.canvas.canvasy(0)
        visible_height = self.canvas.winfo_height()
        visible_bottom = self.canvas.canvasy(visible_height)
        if visible_top <= top and bottom <= visible_bottom:
            return
        x0, y0, x1, y1 = self.canvas._getints(self.canvas['scrollregion'])
        if top >= visible_top and height <= visible_height:
            fraction = top + height - visible_height
        else:
            fraction = top
        fraction = float(fraction) / y1
        self.canvas.yview_moveto(fraction)

    def lastvisiblechild(self):
        if self.children and self.state == 'expanded':
            return self.children[-1].lastvisiblechild()
        else:
            return self

    def update(self):
	#print "in update..."
	self.item._GetSubList()
        if self.parent:
            self.parent.update()
        else:
            oldcursor = self.canvas['cursor']
            self.canvas['cursor'] = "watch"
            self.canvas.update()
            self.canvas.delete(ALL)     # XXX could be more subtle
            self.draw(7, 2)
            x0, y0, x1, y1 = self.canvas.bbox(ALL)
            self.canvas.configure(scrollregion=(0, 0, x1, y1))
            self.canvas['cursor'] = oldcursor

    def draw(self, x, y):
        # XXX This hard-codes too many geometry constants!
        #print "in draw: ", self.item.node.id, self.item.node.data
        self.x, self.y = x, y
        self.drawtext()
        if self.state != 'expanded':
            return y+17
        # draw children
        if not self.children:
            sublist = self.item._GetSubList()
            if not sublist:
                # _IsExpandable() was mistaken; that's allowed
                return y+17
            for item in sublist:
                child = self.__class__(self.canvas, self, item)
                self.children.append(child)
	cx = x+5
        cy = y+17
        cylast = 0
        for child in self.children:
            cylast = cy
            cy = child.draw(cx, cy)
            if child.item._IsExpandable():
                self.drawexpandableicon(child, x, cylast)
        return cy
    
    def drawexpandableicon(self,  child, x, cylast):
        if child.state == 'expanded':
            iconname = "minusnode"
            icontext = '-'
            callback = child.collapse
        else:
            iconname = "plusnode"
            icontext = '+'
            callback = child.expand
        id = self.canvas.create_text(x+9, cylast, anchor="nw",
                                     text=icontext)
        # XXX This leaks bindings until canvas is deleted:
        self.canvas.tag_bind(id, "<1>", callback)
        self.canvas.tag_bind(id, "<Double-1>", lambda x: None)

    def drawtext(self):
        textx = self.x+20-1
        texty = self.y-1
        labeltext = self.item.GetLabelText()
        if labeltext:
            id = self.canvas.create_text(textx, texty, anchor="nw",
                                         text=labeltext)
            self.canvas.tag_bind(id, "<1>", self.select)
            self.canvas.tag_bind(id, "<Double-1>", self.flip)
            x0, y0, x1, y1 = self.canvas.bbox(id)
            textx = max(x1, 200) + 10
        text = self.item.GetText() or "<no text>"
        try:
            self.entry
        except AttributeError:
            pass
        else:
            self.edit_finish()
        try:
            label = self.label
        except AttributeError:
            # padding carefully selected (on Windows) to match Entry widget:
            self.label = Label(self.canvas, text=text, bd=0, padx=2, pady=2)
        if self.selected:
            self.label.configure({'foreground': '#000000', 'background': 'gray'})
        else:
            self.label.configure({'foreground': '#000000', 'background': '#ffffff'})
        id = self.canvas.create_window(textx, texty,
                                       anchor="nw", window=self.label)
        self.label.bind("<1>", self.select_or_edit)
        self.label.bind("<Double-1>", self.flip)
        self.text_id = id

    def select_or_edit(self, event=None):
        if self.selected and self.item.IsEditable():
            self.edit(event)
        else:
            self.select(event)

    def edit(self, event=None):
        self.entry = Entry(self.label, bd=0, highlightthickness=1, width=0)
        self.entry.insert(0, self.label['text'])
        self.entry.selection_range(0, END)
        self.entry.pack(ipadx=5)
        self.entry.focus_set()
        self.entry.bind("<Return>", self.edit_finish)
        self.entry.bind("<Escape>", self.edit_cancel)

    def edit_finish(self, event=None):
        try:
            entry = self.entry
            del self.entry
        except AttributeError:
            return
        text = entry.get()
        entry.destroy()
        if text and text != self.item.GetText():
            self.item.SetText(text)
        text = self.item.GetText()
        self.label['text'] = text
        self.drawtext()
        self.canvas.focus_set()

    def edit_cancel(self, event=None):
        try:
            entry = self.entry
            del self.entry
        except AttributeError:
            return
        entry.destroy()
        self.drawtext()
        self.canvas.focus_set()


class TreeItem:

    """Abstract class representing tree items.

    Methods should typically be overridden, otherwise a default action
    is used.

    """

    def __init__(self):
        """Constructor.  Do whatever you need to do."""

    def GetText(self):
        """Return text string to display."""

    def GetLabelText(self):
        """Return label text string to display in front of text (if any)."""

    expandable = None

    def _IsExpandable(self):
        """Do not override!  Called by TreeNode."""
        if self.expandable is None:
            self.expandable = self.IsExpandable()
        return self.expandable

    def IsExpandable(self):
        """Return whether there are subitems."""
        return 1

    def _GetSubList(self):
        """Do not override!  Called by TreeNode."""
	#print "in _GetSubList()"
        if not self.IsExpandable():
            return []
        sublist = self.GetSubList()
        if not sublist:
            self.expandable = 0
        return sublist

    def IsEditable(self):
        """Return whether the item's text may be edited."""

    def SetText(self, text):
        """Change the item's text (if it is editable)."""

    def GetIconName(self):
        """Return name of icon to be displayed normally."""

    def GetSelectedIconName(self):
        """Return name of icon to be displayed when selected."""

    def GetSubList(self):
        """Return list of items forming sublist."""

    def OnDoubleClick(self):
        """Called on a double-click on the item."""

# A canvas widget with scroll bars and some useful bindings

class ScrolledCanvas:
    def __init__(self, master, **opts):
        if not opts.has_key('yscrollincrement'):
            opts['yscrollincrement'] = 17
        self.master = master
        self.frame = Frame(master)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.canvas = Canvas(self.frame, **opts)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vbar = Scrollbar(self.frame, name="vbar")
        self.vbar.grid(row=0, column=1, sticky="nse")
        self.hbar = Scrollbar(self.frame, name="hbar", orient="horizontal")
        self.hbar.grid(row=1, column=0, sticky="ews")
        self.canvas['yscrollcommand'] = self.vbar.set
        self.vbar['command'] = self.canvas.yview
        self.canvas['xscrollcommand'] = self.hbar.set
        self.hbar['command'] = self.canvas.xview
        self.canvas.bind("<Key-Prior>", self.page_up)
        self.canvas.bind("<Key-Next>", self.page_down)
        #self.canvas.bind("<Key-Up>", self.unit_up)
        #self.canvas.bind("<Key-Down>", self.unit_down)
        #if isinstance(master, Toplevel) or isinstance(master, Tk):
        self.canvas.bind("<Alt-Key-2>", self.zoom_height)
        self.canvas.focus_set()
    def page_up(self, event):
        self.canvas.yview_scroll(-1, "page")
        return "break"
    def page_down(self, event):
        self.canvas.yview_scroll(1, "page")
        return "break"
    def unit_up(self, event):
        self.canvas.yview_scroll(-1, "unit")
        return "break"
    def unit_down(self, event):
        self.canvas.yview_scroll(1, "unit")
        return "break"
    def zoom_height(self, event):
        ZoomHeight.zoom_height(self.master)
        return "break"
