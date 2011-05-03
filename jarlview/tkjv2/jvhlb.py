#!/usr/bin/env python
import sys
import Tkinter as tk
import jvhlbProps as props
import random
class TreeState:
    EXPANDED = 1
    COLLAPSED = 2
    NOTEXPANDABLE = 3
class TreeViewNode:
    def __init__(self, data=''):
        self.data = data
        self.state = TreeState.COLLAPSED
        #self.state = TreeState.EXPANDED
        self.children = []
        self.address = []
def indent(i):
    if i == 0: ''
    else: return reduce(lambda x, y: x+y,  ['   ']*i)
def printTree(tree,  i=0):
    if tree == []: return
    else:
        for node in tree:
            if i == 0: print node.address,  node.data
            else: print indent(i),  node.address, node.data
            printTree(node.children,  i+1)
def generateNodeData(n):
    x = ''
    for i in range(n): x += chr(random.randint(97,122))
    return x
def generateTree(n, m, address = []):
    if n <= 0:
        return []
    elif n == 1:
        x = []
        for i in range(m):
            node = TreeViewNode(data = generateNodeData(3))
            node.state = TreeState.NOTEXPANDABLE
            node.address = address + [i]
            x.append(node)
        return x
    else:
        x = []
        for i in range(m):
            node = TreeViewNode(data = generateNodeData(3))
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
def refreshTree(tree):
    Ui.IndexMap = []
    Ui.HierList.delete(0, tk.END)
    insertTree(tree)
def insertTree(tree,  i=0):
    if tree == []: return
    else:
        for node in tree:
            Ui.IndexMap.append(node.address)
            if i == 0:
                Ui.HierList.insert(tk.END,  node.data)
            else:  
                Ui.HierList.insert(tk.END,  (indent(i)+node.data))
            if node.state == TreeState.EXPANDED:
                insertTree(node.children,  i+1)
def SetupGUi():
    Ui.BindAllHandlers()
    Ui.HierList.config(font=(props.FNAME, props.FSZ, props.FWT),
                      foreground=props.FCOLOR, background=props.BCOLOR)
    Root.geometry("%sx%s+%s+%s" % (props.WIDTH,  props.HEIGHT, props.STARTX, props.STARTY))
#    for item in ["one", "two", "three", "four"]:
#        Ui.HierList.insert(tk.END, item)
    insertTree(Ui.TreeViewModel)
    #Ui.HierList.selection_set(first=0)
#
def onCollapse(event):
    select_tup = Ui.GetSelection()
    address = Ui.IndexMap[select_tup[1]]
    print 'onCollapse',  select_tup,  address
    node = lookUpNode(Ui.TreeViewModel,  address)
    if node.state != TreeState.NOTEXPANDABLE:
        node.state = TreeState.COLLAPSED
        refreshTree(Ui.TreeViewModel)
    Ui.HierList.selection_set(first = select_tup[1])
    Ui.HierList.activate(select_tup[1])
def onExpand(event):
    select_tup = Ui.GetSelection()
    address = Ui.IndexMap[select_tup[1]]
    print 'onExpand',  select_tup,  Ui.IndexMap[select_tup[1]]
    node = lookUpNode(Ui.TreeViewModel,  address)
    if node.state != TreeState.NOTEXPANDABLE:
        node.state = TreeState.EXPANDED
        refreshTree(Ui.TreeViewModel)
    Ui.HierList.selection_set(first = select_tup[1])
    Ui.HierList.activate(select_tup[1])
class JarlViewHierList:
    def __init__(self, Root):
        self.hSB = tk.Scrollbar(Root, orient=tk.HORIZONTAL)
        self.vSB = tk.Scrollbar(Root, orient=tk.VERTICAL)
        self.HierList = tk.Listbox(Root, selectmode=tk.EXTENDED, exportselection=0,
                               xscrollcommand=self.hSB.set, yscrollcommand=self.vSB.set)
        self.hSB.config(command=self.HierList.xview)
        self.hSB.pack(side=tk.BOTTOM, fill=tk.X)
        self.vSB.config(command=self.HierList.yview)
        self.vSB.pack(side=tk.RIGHT, fill=tk.Y)
        self.HierList.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    def BindAllHandlers(self):
        self.HierList.bind(self.KeyBindings["COLLAPSE"], onCollapse)
        self.HierList.bind(self.KeyBindings["EXPAND"], onExpand)
        self.HierList.focus()
    def GetSelection(self):
        index_tup = self.HierList.curselection()
        index = int(index_tup[0])
        if index_tup:
            return (self.HierList.get(index_tup[-1]).strip(),  index)
        else:
            return ("", -99)
#
# main
Root = tk.Tk()
Ui = JarlViewHierList(Root)
Root.tkraise()
#
Ui.KeyBindings = {\
                    "COLLAPSE":props.COLLAPSE, 
                    "EXPAND":props.EXPAND\
                    }
Ui.TreeViewModel = generateTree(5, 4)
Ui.IndexMap = []
#
SetupGUi()
# Run the program interface
Root.mainloop()
