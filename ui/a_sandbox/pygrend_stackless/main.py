
import stackless
import renderer
import pygrend
import view

render = renderer.Renderer()

rootView = view.RootView(render.sg,  render.eventChannel)

v1 = view.ViewView(
                        render.sg, 
                        render.channel, 
                        pygrend.Zect(id='v1',  pos=(2, 2), dims=(390, 596)))

v2 = view.SliderView(
                        render.sg, 
                        render.channel, 
                        pygrend.Zect(id='v2',  pos=(394, 2), dims=(12, 596)))

v3 = view.ViewView(
                        render.sg, 
                        render.channel, 
                        pygrend.Zect(id='v3',  pos=(408, 2), dims=(390, 596)))

rootView.addChild(v1)
rootView.addChild(v2)
rootView.addChild(v3)

v1.scheduleTask()
v2.scheduleTask()
v3.scheduleTask()

stackless.run()

#while ( True):
#    pass
