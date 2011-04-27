import os
from Tkinter import *
import imp

import tkjv.TreeWidget
from tkjv.TreeWidget import TreeItem
from tkjv.TreeWidget import TreeNode
from tkjv.TreeWidget import ScrolledCanvas

import redis_tree

class RedisItem(TreeItem):
    def __init__(self, node_id):
        self.node_id = node_id
        self.node = redis_tree.redis_read(node_id)
    
    def GetText(self):
        return self.node.data
    
    def IsEditable(self):
        return True
    
    def SetText(self, data):
        self.node.data = data
        redis_tree.redis_write(self.node)
    
    def GetIconName(self):
        if not self.IsExpandable():
            return "python"
    
    def IsExpandable(self):
        return self.node.childPtr != 0
        
    def GetSubList(self):
	#print "in GetSubList()..."
        ns = self.getSubListHelp()
        sublist = []
        for n in ns:
            item = RedisItem(n)
            #print "in GetSubList(), adding node: ", item.node.id, item.node.data
            sublist.append(item)
        return sublist
    
    def getSubListHelp(self):
        sublist = []
        sublist.append(self.node.childPtr)
        r_node = redis_tree.redis_read(self.node.childPtr)
        while ( r_node.siblingPtr != 0 ):
            sublist.append(r_node.siblingPtr)
            r_node = redis_tree.redis_read(r_node.siblingPtr)
        return sublist

def test(node_id):
    root = Tk()
    root.configure(bd=0, bg="yellow")
    root.focus_set()
    
    sc = ScrolledCanvas(root, bg="white", highlightthickness=0, takefocus=1)
    sc.frame.pack(expand=1, fill="both")
    
    item = RedisItem(node_id)
    node = TreeNode(sc.canvas, None, item)
    node.expand()
    node.select()

if __name__ == '__main__':
    test()

