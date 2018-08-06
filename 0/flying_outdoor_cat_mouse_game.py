from morse.builder import *

from math import pi

""" Cat (Quadrotor) """
cat = Quadrotor()
cat.translate(x=-51.0, z=1.0)
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

cat_battery = Battery()
cat_battery.translate(x=0.3, z=-0.05)
cat_battery.rotate(x=+0.2)
cat.append(cat_battery)
cat_battery.add_stream('socket')

""" mouse (atrv)"""
mouse = ATRV()
mouse.translate (x=51.0,y=-59, z=0.6)
mouse.rotate(z=0.70*pi)

keyb = Keyboard()
keyb.properties(Speed=4.0)
mouse.append(keyb)

# waypoint = Waypoint()
# # waypoint.translate(<x>, <y>, <z>)
# # waypoint.rotate(<rx>, <ry>, <rz>)
# mouse.append(waypoint)
# waypoint.add_interface('socket')

# collision = Collision()
# collision.translate(x=0.3, z=0.05)
# collision.rotate(x=+0.2)
# mouse.append(collision)
# collision.add_interface('socket')

# orientation = Orientation()
# orientation.translate(x=0.3, z=0.05)
# orientation.rotate(x=+0.2)
# mouse.append(orientation)
# orientation.add_interface('socket')

proximity = Proximity()
proximity.translate(x=0.3, z=0.05)
proximity.rotate(x=+0.2)
mouse.append(proximity)
proximity.properties(track = "drone", range = 50)
#proximity.add_interface('text')
proximity.add_interface('socket')

motion = Waypoint()
motion.add_interface('socket')
mouse.append(motion)

mousePose = Pose()
mouse.append(mousePose)
mousePose.add_stream('socket')

mouse_battery = Battery()
mouse_battery.translate(x=0.3, z=-0.05)
mouse_battery.rotate(x=+0.2)
mouse.append(mouse_battery)
mouse_battery.add_stream('socket')

""" The playground """
env = Environment('outdoors')
env.set_camera_location([70.0, -80.0, 30.0])
env.set_camera_rotation([1.0470, 0, 0.7854])
env.select_display_camera(semanticC)
env.set_camera_clip(clip_end=1000)
