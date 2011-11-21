
import stackless
import renderer
import pygrend
import view

render = renderer.Renderer()

rootView = view.RootView(render.sg,  render.eventChannel)

slider = view.XSliderView(
                        render.sg,
                        render.channel,
                        pygrend.Zect(id='slider',  pos=(394, 2), dims=(12, 596)))

v1 = view.ViewView(
                        render.sg, 
                        render.channel, 
                        pygrend.Zect(id='v1',  pos=(2, 2), dims=(390, 596)), 
                        announce=slider.announce, 
                        tag = 'left')

v3 = view.ViewView(
                        render.sg, 
                        render.channel, 
                        pygrend.Zect(id='v3',  pos=(408, 2), dims=(390, 596)), 
                        announce=slider.announce, 
                        tag = 'right')

rootView.addChild(v1)
rootView.addChild(slider)
rootView.addChild(v3)

v1.scheduleTask()
slider.scheduleTask()
v3.scheduleTask()

stackless.run()

#while ( True):
#    pass
