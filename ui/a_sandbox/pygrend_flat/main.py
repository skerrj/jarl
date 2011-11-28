
import core
import renderer
import view

sceneGraph = core.SceneGraph()
rootView = view.RootView(sceneGraph)
render = renderer.Renderer(sceneGraph,  rootView)

v1 = view.ViewView(
                        sceneGraph, 
                        core.Zect(id='v1',  pos=(2, 2), dims=(390, 596)))

v2 = view.ViewView(
                        sceneGraph, 
                        core.Zect(id='v3',  pos=(408, 2), dims=(390, 596)))

slider = view.XSliderView(
                        sceneGraph, 
                        core.Zect(id='slider',  pos=(394, 2), dims=(12, 596)), 
                        (v1,  v2))

rootView.addChild(v1)
rootView.addChild(slider)
rootView.addChild(v2)

render.mainLoop()
