#
class TreeState:
    EXPANDED = 1
    COLLAPSED = 2
    NOTEXPANDABLE = 3
class TreeViewNode:
    def __init__(self, data=''):
        self.data = data
        #self.state = TreeState.COLLAPSED
        self.state = TreeState.EXPANDED
        self.children = []
        self.address = []
