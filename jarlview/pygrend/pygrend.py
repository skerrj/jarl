#
#
#
class Zvent:
    pass

class Zect:
    def __init__(self,x=0,y=0,width=32,height=32,text='', color=(255,255,255)):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text = text
        self.color=color

class SceneGraphSyncMessage:
    def __init__(self, node_id,  command, view_list=None,  index_list=None):
        self.node_id = node_id
        self.command=command
        self.view_list=view_list
        self.index_list = index_list

#def send_message(sock,  mes):
#        ms = pickle.dumps(mes)
#        sock.send(ms)
