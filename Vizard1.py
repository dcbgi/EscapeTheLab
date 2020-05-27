import viz
import vizact
import viztask
import vizshape
import vizconnect
import vizproximity
from vizconnect.util import view_collision

viz.go()
vizconnect.go('vizconnect_config.py')
viz.phys.enable()

#crouch function
def fc():
  vp.setEnabled(viz.TOGGLE)
  vp2.setEnabled(viz.TOGGLE)

#add the room
room =  viz.addChild('CRSim.osgb')
#whiteboard = viz.addChild('whiteboard.osgb')
#whiteboard.setPosition([7.38297, 2.91289, 15.74552])
door = viz.addChild('Door.osgb')
door.setEuler([90,0,0])
door.setPosition([14.72,0,7.92])

room.collidePlane()

oriMode = vizconnect.VIEWPOINT_MATCH_DISPLAY
posMode = vizconnect.VIEWPOINT_MATCH_FEET

# Add a vizconnect viewpoint.
vp = vizconnect.addViewpoint(   pos=[5, 0, 8.83],
                                euler=[90, 0, 0],
                                posMode=posMode,
                                oriMode=oriMode,
)

vp2 =vizconnect.addViewpoint(   pos=[5, -.5, 8.83],
                                euler=[90, 0, 0],
                                posMode=posMode,
                                oriMode=oriMode,
)

# Displays are added to vizconnect viewpoints
vp.add(vizconnect.getDisplay())
vp2.add(vizconnect.getDisplay())
vp.setEnabled(viz.ON)

# Call reset viewpoints, which forces the display into the vizconnect viewpoint position.
vizconnect.resetViewpoints()
# add a reset key so when r is pressed the user is moved back to the viewpoint
vizact.onkeydown('r', vizconnect.resetViewpoints)
#crouch key
vizact.onkeydown('c', fc)

inorderprompt = viz.addText3D('It must be done in order',viz.SCREEN)

#made grabbable rbg spheres
sphere1 = vizshape.addSphere(radius = .1) 
sphere1.setPosition(10.62,.3,12)
sphere1.color(1,0,0) #red
sphere1physics = sphere1.collideSphere(bounce=1.5) 

sphere2 = vizshape.addSphere(radius = .1) 
sphere2.setPosition(9.62,.3,12)
sphere2.color(0,1,0) #green
sphere2physics = sphere2.collideSphere(bounce=1.5) 

sphere3 = vizshape.addSphere(radius = .1) 
sphere3.setPosition(8.62,.3,12)
sphere3.color(0,0,1) #blue
sphere3physics = sphere3.collideSphere(bounce=1.5) 

shapes = [sphere1,sphere2,sphere3]
grabber = vizconnect.getRawTool('grabber')
grabber.setItems(shapes)

#rgb boxes 
p1= vizshape.addCube(size = 1)
p1.color(1,0,0)
p1.setPosition(9,0,10)
p1p = p1.collideBox()
sensor1 = vizproximity.addBoundingBoxSensor(p1)
target1 = vizproximity.Target(sphere1)

p2= vizshape.addCube(size = 1)
p2.color(0,1,0)
p2.setPosition(9,0,8)
p2p = p2.collideBox()
sensor2 = vizproximity.addBoundingBoxSensor(p2)
target2 = vizproximity.Target(sphere2)

p3= vizshape.addCube(size = 1)
p3.color(0,0,1)
p3.setPosition(9,0,6)
p3p = p3.collideBox()
sensor3 = vizproximity.addBoundingBoxSensor(p3)
target3 = vizproximity.Target(sphere3)

#Create proximity manager 
manager = vizproximity.Manager()
manager1 = vizproximity.Manager()
manager2 = vizproximity.Manager()

manager.addSensor(sensor1)
manager1.addSensor(sensor2)
manager2.addSensor(sensor3)
manager.addTarget(target1)
manager1.addTarget(target2)
manager2.addTarget(target3)

#Toggle debug shapes with keypress 
vizact.onkeydown('d',manager.setDebug,viz.TOGGLE)

sensors = [sensor1, sensor2, sensor3]
targets = [target1, target2, target3]

def finished():
  inorderprompt.remove()
  text3D = viz.addText3D('You\'ve beat the game.',viz.SCREEN)
  door.remove() 

def proximityTask():
  yield vizproximity.waitEnter(sensor1, target1, None)
  active = [manager.getActiveSensors()]
  print(active)
  yield vizproximity.waitEnter(sensor2, target2, None)
  active += [manager1.getActiveSensors()]
  print(active)
  yield vizproximity.waitEnter(sensor3, target3, None)
  active += [manager2.getActiveSensors()]

  if(len(active) == 3):
    finished()

viztask.schedule(proximityTask())

#when all balls interact with their respective cubes in order, 
#   you did it' sign pops up
#
#Controls:
#directional pad to move
#c to crouch
#r to reset position in case of bugs
#left-click-hold to grab
#right click press to drop
#scroll bar to extend hand