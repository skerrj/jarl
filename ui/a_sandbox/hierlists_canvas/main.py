#!/usr/bin/env python
import sys
import Tkinter as tk
import tkFont
import props
import utils
#import random
class TreeState:
    EXPANDED = 1
    COLLAPSED = 2
    NOTEXPANDABLE = 3
class TreeViewNode:
    def __init__(self, data=''):
        self.data = data
        #self.state = TreeState.COLLAPSED
        self.state = TreeState.EXPANDED
        self.selected = False
        self.children = []
        self.address = []
#
def generateTree(n, m, address = []):
    if n <= 0:
        return []
    elif n == 1:
        x = []
        for i in range(m):
            node = TreeViewNode(data = utils.generateNodeData(3))
            node.state = TreeState.NOTEXPANDABLE
            node.address = address + [i]
            x.append(node)
        return x
    else:
        x = []
        for i in range(m):
            node = TreeViewNode(data = utils.generateNodeData(3))
            node.address = address + [i]
            node.children = generateTree(n-1, m,  address = node.address)
            x.append(node)
        return x
def lookUpNode(tree,  address):
    if len(address) == 1:
        return tree[address[0]]
    else:
        i = address[0]
        rest = address[1:]
        return lookUpNode(tree[i].children,  rest)
def refreshTree(tree,  last_selected_index):
    Ui.IndexMap = []
    #Ui.HierList.delete(0, tk.END)
    Ui.HierList.delete(ALL)
    #scroll bar offsets
    (sb_v_i,  sb_v_j) = Ui.vSB.get()
    (sb_h_i,  sb_h_j) = Ui.hSB.get()
    insertTree(tree)
    Ui.HierList.selection_set(first = last_selected_index)
    Ui.HierList.activate(last_selected_index)
    Ui.vSB.set(sb_v_i,  sb_v_j)
    Ui.hSB.set(sb_h_i,  sb_h_j)
    #Ui.HierList.yview_moveto(sb_v_i)
def insertTree(tree):
    if tree == []: 
        return None
    else:
        for node in tree:
            #print 'insertTree: ',  node.data,  Ui.x,  Ui.y
            Ui.IndexMap.append(node.address)
#            if i == 0:
#                #Ui.HierList.insert(tk.END,  node.data)
#            else:  
#                Ui.HierList.insert(tk.END,  (utils.indent(i)+node.data))
            font = tkFont.Font ( family=props.FNAME,size=props.FSZ, weight=props.FWT )
            label = tk.Label(Ui.HierList, text=node.data, bd=0, padx=2, pady=2, font=font)
            if node.selected:
                label.configure({'foreground': props.BCOLOR, 'background': props.FCOLOR})
            else:
                label.configure({'foreground': props.FCOLOR, 'background': props.BCOLOR})
            Ui.HierList.create_window(Ui.x, Ui.y, anchor="nw", window=label)
            Ui.y += props.YOFF
            #x += props.XOFF
            if node.state == TreeState.EXPANDED:
                Ui.x += props.XOFF
                insertTree(node.children)
                Ui.x -= props.XOFF
def SetupGUi():
    Ui.BindAllHandlers()
    #Ui.HierList.config(font=(props.FNAME, props.FSZ, props.FWT),
    #                 foreground=props.FCOLOR, background=props.BCOLOR)
    Ui.hSB.config(activebackground = props.FCOLOR, background= props.BCOLOR, troughcolor = props.FCOLOR, relief=tk.FLAT)
    Ui.vSB.config(activebackground = props.FCOLOR, background= props.BCOLOR, troughcolor = props.FCOLOR, relief=tk.FLAT)
    Ui.HierList.config(background=props.BCOLOR)
    Root.geometry("%sx%s+%s+%s" % (props.WIDTH,  props.HEIGHT, props.STARTX, props.STARTY))
#    for item in ["one", "two", "three", "four"]:
#        Ui.HierList.insert(tk.END, item)
    insertTree(Ui.TreeViewModel)
    #Ui.HierList.selection_set(first=0)
#
def onUp(event):
    print 'onUp'
def onDown(event):
    print 'onDown'
def onCollapse(event):
    #scroll_bar_vertical_offset = Ui.vSB.get()
    data,  index = Ui.GetSelection()
    address = Ui.IndexMap[index]
    print 'onCollapse',  data,  index,  address
    node = lookUpNode(Ui.TreeViewModel,  address)
    if node.state != TreeState.NOTEXPANDABLE:
        node.state = TreeState.COLLAPSED
        refreshTree(Ui.TreeViewModel,  index)
    #Ui.HierList.selection_set(first = select_tup[1])
    #Ui.HierList.activate(select_tup[1])
    #Ui.vSB.set(scroll_bar_vertical_offset[0],  scroll_bar_vertical_offset[1])
def onExpand(event):
    #scroll_bar_vertical_offset = Ui.vSB.get()
    data,  index = Ui.GetSelection()
    address = Ui.IndexMap[index]
    print 'onExpand',  data,  index,  address
    node = lookUpNode(Ui.TreeViewModel,  address)
    if node.state != TreeState.NOTEXPANDABLE:
        node.state = TreeState.EXPANDED
        refreshTree(Ui.TreeViewModel,  index)
    #Ui.HierList.selection_set(first = select_tup[1])
    #Ui.HierList.activate(select_tup[1])
    #Ui.vSB.set(scroll_bar_vertical_offset[0],  scroll_bar_vertical_offset[1])
#
class JarlViewHierList:
    def __init__(self, Root):
        self.hSB = tk.Scrollbar(Root, orient=tk.HORIZONTAL)
        self.vSB = tk.Scrollbar(Root, orient=tk.VERTICAL)
        #
        #self.HierList = tk.Listbox(Root, selectmode=tk.EXTENDED, exportselection=0,
        #                      xscrollcommand=self.hSB.set, yscrollcommand=self.vSB.set)
        #self.frame = tk.Frame(Root)
        #self.HierList = tk.Canvas(self.frame, xscrollcommand=self.hSB.set, yscrollcommand=self.vSB.set)
        self.HierList = tk.Canvas(Root, xscrollcommand=self.hSB.set, yscrollcommand=self.vSB.set)
        #
        self.hSB.config(command=self.HierList.xview)
        self.hSB.pack(side=tk.BOTTOM, fill=tk.X)
        self.vSB.config(command=self.HierList.yview)
        self.vSB.pack(side=tk.RIGHT, fill=tk.Y)
        self.HierList.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    def BindAllHandlers(self):
        print 'in BindAllHandlers'
        self.HierList.bind(self.KeyBindings["COLLAPSE"], onCollapse)
        self.HierList.bind(self.KeyBindings["EXPAND"], onExpand)
        self.HierList.bind(self.KeyBindings["UP"], onUp)
        self.HierList.bind(self.KeyBindings["DOWN"], onDown)
        self.HierList.focus_set()
    def GetSelection(self):
        pass
#        index_tup = self.HierList.curselection()
#        index = int(index_tup[0])
#        if index_tup:
#            return (self.HierList.get(index_tup[-1]).strip(),  index)
#        else:
#            return ("", -99)
#
# main
Root = tk.Tk()
Ui = JarlViewHierList(Root)
Root.tkraise()
#
Ui.KeyBindings = {\
                    "COLLAPSE":props.COLLAPSE, 
                    "EXPAND":props.EXPAND, 
                    "UP":props.UP,
                    "DOWN":props.DOWN
                    }
Ui.TreeViewModel = generateTree(5, 4)
Ui.IndexMap = []
Ui.SelectedIndex = 0
Ui.x = Ui.y = 1
#
SetupGUi()
#
# Run the program interface
Root.mainloop()
