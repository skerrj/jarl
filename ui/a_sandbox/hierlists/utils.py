import random
import tree_node

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
            node = tree_node.TreeViewNode(data = generateNodeData(3))
            node.state = tree_node.TreeState.NOTEXPANDABLE
            node.address = address + [i]
            x.append(node)
        return x
    else:
        x = []
        for i in range(m):
            node = tree_node.TreeViewNode(data = generateNodeData(3))
            node.address = address + [i]
            node.children = generateTree(n-1, m,  address = node.address)
            x.append(node)
        return x
