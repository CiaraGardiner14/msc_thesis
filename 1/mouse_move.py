#Cautious mouse. Moves when dron eis closer than 30m and hides until drone is gone


import pymorse
import sys, termios, tty, os, time
import math
from pymorse import Morse

from morse.builder import *

def print_pos(pose):
    print("I'm currently at %s" % pose)

def go_to():
    with pymorse.Morse() as simu, Morse() as morse:

        #subscribes to updates from the Pose sensor by passing a callback
        nearObj = morse.mouse.proximity
        mousePose = morse.mouse.mousePose
        mouseColl = morse.mouse.collision

        # sends a destination
        simu.mouse.motion.publish({'x' : -6.363116264343262, 'y': 45.8295783996582, 'z': 0.0,
                                  'tolerance' : 0.5,
                                  'speed' : 1.0})

        # Leave a couple of millisec to the simulator to start the action
        simu.sleep(0.1)
        curr = 0
        while simu.mouse.motion.get_status() != "Arrived":
        # waits until we reach the target
            mousePosition = where_is(mousePose)

            if(is_collision(mouseColl) != 0):
                #avoid_col(mousePosition)
                #go_to()
                simu.mouse.motion.publish({'x' : mousePosition['x']-1, 'y': mousePosition['y']-2, 'z': mousePosition['z'],
                                           'tolerance' : 0.5,
                                           'speed' : 1.0})
                go_to()

            prev = curr
            curr = near_robot(nearObj)

            if (curr and 1 < curr < 30):
                ######tests######
                print("Too close")
                ######tests######
                simu.sleep(0.5)
                go_three()

            else:
                simu.sleep(0.5)

        print("Here we are!")

def go_three():

    #Fleeing reaction called when p button hit
    with pymorse.Morse() as simu, Morse() as morse:

        # subscribes to updates from the Pose sensor by passing a callback

        mousePose = morse.mouse.mousePose
        nearObj = morse.mouse.proximity
        bat = morse.mouse.mouse_battery

        mousePosition = where_is(mousePose)
        destination = go_where(mousePosition)
        battery = battery_life(bat)
        simu.mouse.motion.publish(destination)

        cnt = 0

        while nearObj:
            cnt+1
            print(cnt)

        go_to()

def go_where(mousePosition):
    pos1 = {'x' : 43.4794807434082, 'y': 0.876022458076477, 'z': 0.08955984562635422, 'tolerance' : 0.5, 'speed' : 4.0}
    pos2 = {'x' : -22.46, 'y': -20.0, 'z': 0.0, 'tolerance' : 0.5, 'speed' : 4.0}
    pos3 = {'x' : 10.48, 'y': 58.73, 'z': 0.0, 'tolerance' : 0.5, 'speed' : 4.0}

    distance1 = math.sqrt(sum([(mousePosition['x'] - pos1['x']) ** 2 + (mousePosition['y'] - pos1['y']) ** 2]))
    distance2 = math.sqrt(sum([(mousePosition['x'] - pos2['x']) ** 2 + (mousePosition['y'] - pos2['y']) ** 2]))
    distance3 = math.sqrt(sum([(mousePosition['x'] - pos3['x']) ** 2 + (mousePosition['y'] - pos3['y']) ** 2]))

    if distance1 < distance2 and distance1 < distance3:
        optdist = pos1
    if distance2 < distance1 and distance2 < distance3:
        optdist = pos2
    if distance3 < distance1 and distance3 < distance2:
        optdist = pos3
    print("I'm going to %s" % optdist)
    return optdist

# def avoid_col(mousePosition):
#     with pymorse.Morse() as simu, Morse() as morse:
#         avoid = {'x' : mousePosition['x']-1, 'y': mousePosition['y']-2, 'z': mousePosition['z'],
#                                    'tolerance' : 0.5,
#                                    'speed' : 1.0}
#
#         simu.mouse.motion(avoid)


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

button_delay = 0.2


def where_is(agentPose_stream):
    """ Read data from the [mouse|cat] pose sensor, and determine the position of the agent """
    pose = agentPose_stream.get()

    return pose

def is_collision(agentCollision_stream):
   """ Read data from the [mouse|cat] pose sensor, and determine the position of the agent """
   pose = agentCollision_stream.get()
   objects = pose['objects']
   objects = objects.split(',')
   if (len(objects) <= 1):
       return 0
   else:
       return objects[1]


def near_robot(agentProximity_stream):
    """ Read data from the [mouse|cat] pose sensor, and determine the position of the agent """
    pose = agentProximity_stream.get()
    ind = pose['near_robots']
    # ind2 = pose['timestamp']

    if not ind:
        return 0
    else:
        item = ind['cat']
        return item

def battery_life(agentBattery_stream):
   """ Read data from the [mouse|cat] pose sensor, and determine the position of the agent """
   set = agentBattery_stream.get()
   charge = set['charge']
   return charge


def main():
    """ Main behaviour """
    while True:
        go_to()

if __name__ == "__main__":
    main()
