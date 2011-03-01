import redis_tree

from redis_tree import RedisNode

# A
#  A1
#    A11
#    A12
#  A2
#    A21
#    A22
#  A3
#    A31
#    A32

a = RedisNode('A')

a1 = RedisNode('A1')
a11 = RedisNode('A11')
a12 = RedisNode('A12')

a1.addChild(a11)
a1.addChild(a12)
a.addChild(a1)

a2 = RedisNode('A2')
a21 = RedisNode('A21')
a22 = RedisNode('A22')

a2.addChild(a21)
a2.addChild(a22)
a.addChild(a2)

a3 = RedisNode('A3')
a31 = RedisNode('A31')
a32 = RedisNode('A32')

a3.addChild(a31)
a3.addChild(a32)
a.addChild(a3)
