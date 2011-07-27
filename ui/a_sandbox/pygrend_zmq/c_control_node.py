#
#   Connects SUB socket to 
#    tcp://localhost:5556
#    ipc://pygame1.ipc
#
import a_control_node
from a_control_node import *
theAControlNode = AControlNode('c1')
#testing
theAControlNode.test_commands(5, 20, 10, 42+(5*32))
theAControlNode.run()
