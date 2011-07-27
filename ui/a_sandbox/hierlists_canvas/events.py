#
def onCollapse(event):
    global Ui
    data,  index = Ui.GetSelection()
    address = Ui.IndexMap[index]
    print 'onCollapse',  data,  index,  address
    node = lookUpNode(Ui.TreeViewModel,  address)
    if node.state != tree_node.TreeState.NOTEXPANDABLE:
        node.state = tree_node.TreeState.COLLAPSED
        refreshTree(Ui.TreeViewModel,  index)
def onExpand(event):
    global Ui
    data,  index = Ui.GetSelection()
    address = Ui.IndexMap[index]
    print 'onExpand',  data,  index,  address
    node = lookUpNode(Ui.TreeViewModel,  address)
    if node.state != tree_node.TreeState.NOTEXPANDABLE:
        node.state = tree_node.TreeState.EXPANDED
        refreshTree(Ui.TreeViewModel,  index)
