from morse.builder import *

from math import pi

""" Cat (Quadrotor) """
cat = Quadrotor()
cat.translate(x=-7.0, z=1.0)
cat.rotate(z=pi/3)
cat.properties(Type = "drone", Label = "mal_drone")

# Waypoint controller (x,y,z, yaw and tolerance (default is 0.2))
waypoint = RotorcraftWaypoint()
cat.append(waypoint)
waypoint.add_stream('socket')

semanticC = SemanticCamera()
semanticC.translate(x=0.3, z=-0.05)
semanticC.rotate(x=+0.2)
cat.append(semanticC)
semanticC.properties(cam_far=800)

catPose = Pose()
cat.append(catPose)
catPose.add_stream('socket')


""" mouse (atrv)"""
mouse = ATRV()
mouse.translate (x=-4.0,y=6.5, z=0.1)
mouse.rotate(z=0.70*pi)

keyb = Keyboard()
keyb.properties(Speed=4.0)
mouse.append(keyb)

proximity = Proximity()
proximity.translate(x=0.3, z=0.05)
proximity.rotate(x=+0.2)
mouse.append(proximity)
proximity.properties(track = "drone", range = 50)
#proximity.add_interface('text')
proximity.add_interface('socket')

mousePose = Pose()
mouse.append(mousePose)
mousePose.add_stream('socket')

motion = Waypoint()
motion.add_interface('socket')
mouse.append(motion)


""" The playground """
env = Environment('outdoors')
env.set_camera_location([10.0, -10.0, 10.0])
env.set_camera_rotation([1.0470, 0, 0.7854])
env.select_display_camera(semanticC)
env.set_camera_clip(clip_end=1000)
