#
#
#
import redis
from utils.codeGen import CodeGeneratorBackend

r = redis.Redis(host='localhost', port=6379, db=0)

def getId():
    return r.incr('jvIdCnt')

def redis_write(node):
    r.hmset(node.id, { \
            'data': node.data, \
            'pptr': node.parentPtr, \
            'sptr': node.siblingPtr, \
            'cptr': node.childPtr })
 
def redis_read(node_id):
    d = r.hget(node_id,'data')
    #print "in redis_read(node_id): ", node_id, d
    p   = int(r.hget(node_id,'pptr'))
    s   = int(r.hget(node_id,'sptr'))
    c   = int(r.hget(node_id,'cptr'))
    return RedisNode(data=d,pp=p,sp=s,cp=c,nid=node_id)

def redis_print_node(node_id):
    data = r.hget(node_id,'data')
    pp   = int(r.hget(node_id,'pptr'))
    sp   = int(r.hget(node_id,'sptr'))
    cp   = int(r.hget(node_id,'cptr'))
    print node_id, pp, sp, cp

c = CodeGeneratorBackend()
def redis_print(node_id):
    c.begin(tab='   ')
    rp(node_id)
    print c.end()

def rp(node_id):
    data = r.hget(node_id,'data')
    sp   = int(r.hget(node_id,'sptr'))
    cp   = int(r.hget(node_id,'cptr'))
    if ( sp == 0 and cp == 0):
        c.write(data + '\n')
    elif ( sp > 0 and cp == 0 ):
        c.write(data + '\n')
        rp(sp)
    elif ( sp == 0 and cp > 0 ):
        c.write(data + '\n')
        c.indent()
        rp(cp)
        c.dedent()
    else:
        c.write(data + '\n')
        c.indent()
        rp(cp)
        c.dedent()
        rp(sp)

class RedisNode:
    def __init__(self, data='', pp=0, sp=0, cp=0, tags=[], nid=-99):
        self.id = nid
        self.data = data
        self.parentPtr = pp
        self.siblingPtr = sp
        self.childPtr = cp
        self.tags = tags
        self.tagPtr = None 
        if ( nid == -99 ) :
            self.id = getId()
            #print "created:", self.id, self.data
            redis_write(self)
    
    def addChild(self, child): 
        child.parentPtr = self.id
        child.siblingPtr = self.childPtr
        self.childPtr = child.id
        #print "adding child", child.id, "to", self.id
        redis_write(child)
        redis_write(self)

