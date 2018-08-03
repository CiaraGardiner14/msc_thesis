""" Simple script for the FLYING CAT AND MOUSE game tutorial

This will command the flying cat, using the pose sensor of the mouse, to follow
after the latter."""

import math
from pymorse import Morse
import pymorse
import sys, termios, tty, os, time

from morse.builder import *
# Use sockets through pymorse interface


""" The minimal distance to maintain between the mouse and the cat. """
minDist = 0.0

""" The height for the flying cat. """
# NB: this is the absolute height not the one relative to the ground...
# TODO: use sensors (laser?) to take into account the ground and the obstacle
height= 3.5


def where_is(agentPose_stream):
    """ Read data from the [mouse|cat] pose sensor, and determine the position of the agent """
    pose = agentPose_stream.get()

    return pose


def frighten_mouse():
    """ Use the mouse pose sensor to locate and "chase" it """

    with pymorse.Morse() as simu, Morse() as morse:
        catPose = morse.cat.catPose
        mousePose = morse.mouse.mousePose
        motion = morse.cat.waypoint
        bat = morse.cat.cat_battery
        bat_lev = battery_life(bat)
        is_free = True
        while (bat_lev > 50 and is_free == True):
            catPosition = where_is(catPose)
            mousePosition = where_is(mousePose)

            if mousePosition and catPosition:
                # go behind the mouse
                waypoint = {    "x": mousePosition['x'] - minDist*math.cos(mousePosition['yaw']), \
                                "y": mousePosition['y'] - minDist*math.sin(mousePosition['yaw']), \
                                "z": height, \
                                "yaw": catPosition['yaw'], \
                                "tolerance": 0.5 \
                            }

                # look at the mouse
                if((catPosition['y'] - mousePosition['y']) < 1 and (catPosition['x'] - mousePosition['x']) < 1 and is_hiding(mousePosition) = False):
                    is_free = False
                    print("CAPTURE")
                    #print("%s" % is_free)
                elif mousePosition['x']==catPosition['x']:
                     waypoint['yaw']= math.sign(mousePosition['y']-catPosition['y']) * math.pi
                else:
                    waypoint['yaw']= math.atan2(mousePosition['y']-catPosition['y'],mousePosition['x']-catPosition['x'])

                # send the command through the socket
                motion.publish(waypoint)

        cnt = 0
        while True:
            cnt+1


def battery_life(agentBattery_stream):
    """ Read data from the [mouse|cat] pose sensor, and determine the position of the agent """
    set = agentBattery_stream.get()
    charge = set['charge']
    return charge

def is_hiding(pose):
    pos1 = {'x' : 49.0, 'y': 17.0, 'z': 0.0, 'tolerance' : 0.5, 'speed' : 4.0}
    pos2 = {'x' : -22.46, 'y': -20.0, 'z': 0.0, 'tolerance' : 0.5, 'speed' : 4.0}
    pos3 = {'x' : 10.48, 'y': 58.73, 'z': 0.0, 'tolerance' : 0.5, 'speed' : 4.0}
    if(pose == pos1 or pose == pos2 or pose == pos3):
        return True
    else:
        return False


def main():
    """ Main behaviour """
    frighten_mouse()

if __name__ == "__main__":
    main()
