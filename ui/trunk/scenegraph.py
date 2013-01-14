#
# sg
#
class SceneGraph:
    def __init__(self):
      self.scene = dict([])
    def add(self, view):
      self.scene[view.name]=view
    def getGraph(self):
      return self.scene
    def delete(self, key):
      del self.scene[key]

# global sg
SCENEGRAPH = SceneGraph()
