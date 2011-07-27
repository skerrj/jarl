#!/usr/bin/env python
import sys
import Tkinter as tk
import props
import utils
import tree_node
import events

def lookUpNode(tree,  address):
    if len(address) == 1:
        return tree[address[0]]
    else:
        i = address[0]
        rest = address[1:]
        return lookUpNode(tree[i].children,  rest)
def refreshTree(tree,  last_selected_index):
    Ui.IndexMap = []
    Ui.HierList.delete(0, tk.END)
    #scroll bar offsets
    (sb_v_i,  sb_v_j) = Ui.vSB.get()
    (sb_h_i,  sb_h_j) = Ui.hSB.get()
    insertTree(tree)
    Ui.HierList.selection_set(first = last_selected_index)
    Ui.HierList.activate(last_selected_index)
    Ui.vSB.set(sb_v_i,  sb_v_j)
    Ui.hSB.set(sb_h_i,  sb_h_j)
    Ui.HierList.yview_moveto(sb_v_i)
def insertTree(tree,  i=0):
    if tree == []: return
    else:
        for node in tree:
            Ui.IndexMap.append(node.address)
            if i == 0:
                Ui.HierList.insert(tk.END,  node.data)
            else:  
                Ui.HierList.insert(tk.END,  (utils.indent(i)+node.data))
            if node.state == tree_node.TreeState.EXPANDED:
                insertTree(node.children,  i+1)
#
def onCollapse(event):
    data,  index = Ui.GetSelection()
    address = Ui.IndexMap[index]
    print 'onCollapse',  data,  index,  address
    node = lookUpNode(Ui.TreeViewModel,  address)
    if node.state != tree_node.TreeState.NOTEXPANDABLE:
        node.state = tree_node.TreeState.COLLAPSED
        refreshTree(Ui.TreeViewModel,  index)
def onExpand(event):
    data,  index = Ui.GetSelection()
    address = Ui.IndexMap[index]
    print 'onExpand',  data,  index,  address
    node = lookUpNode(Ui.TreeViewModel,  address)
    if node.state != tree_node.TreeState.NOTEXPANDABLE:
        node.state = tree_node.TreeState.EXPANDED
        refreshTree(Ui.TreeViewModel,  index)
def onEdit(event):
    print 'onEdit'
class JarlViewHierList:
    def __init__(self, Root):
        self.hSB = tk.Scrollbar(Root, orient=tk.HORIZONTAL)
        self.vSB = tk.Scrollbar(Root, orient=tk.VERTICAL)
        #
        self.HierList = tk.Listbox(Root, selectmode=tk.EXTENDED, exportselection=0,
                               xscrollcommand=self.hSB.set, yscrollcommand=self.vSB.set)
        #
        self.Shell = tk.Entry(Root)
        self.Shell.pack(side=tk.BOTTOM,  fill=tk.X)
        self.hSB.config(command=self.HierList.xview)
        self.hSB.pack(side=tk.BOTTOM, fill=tk.X)
        self.vSB.config(command=self.HierList.yview)
        self.vSB.pack(side=tk.RIGHT, fill=tk.Y)
        self.HierList.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    def BindAllHandlers(self):
        self.HierList.bind(self.KeyBindings["COLLAPSE"], onCollapse)
        self.HierList.bind(self.KeyBindings["EXPAND"], onExpand)
        self.HierList.bind(self.KeyBindings["EDIT"], onEdit)
        self.HierList.focus()
    def GetSelection(self):
        index_tup = self.HierList.curselection()
        index = int(index_tup[0])
        if index_tup:
            return (self.HierList.get(index_tup[-1]).strip(),  index)
        else:
            return ("", -99)
    def SetupGUi(self):
        self.BindAllHandlers()
        self.HierList.config(font=(props.FNAME, props.FSZ, props.FWT),
                      foreground=props.FCOLOR, background=props.BCOLOR)
        self.Shell.config(font=(props.FNAME, props.FSZ, props.FWT),
                      foreground=props.FCOLOR, background=props.BCOLOR)
        Root.geometry("%sx%s+%s+%s" % (props.WIDTH,  props.HEIGHT, props.STARTX, props.STARTY))
        insertTree(Ui.TreeViewModel)
#
# main
Root = tk.Tk()
Ui = JarlViewHierList(Root)
Root.tkraise()
#
Ui.KeyBindings = {\
                    "COLLAPSE":props.COLLAPSE, 
                    "EXPAND":props.EXPAND, 
                    "EDIT":props.EDIT
                    }
Ui.TreeViewModel = utils.generateTree(5, 4)
Ui.IndexMap = []
#
Ui.SetupGUi()
#
# Run the program interface
Root.mainloop()
