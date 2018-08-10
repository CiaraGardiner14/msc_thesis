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
minDist = 0.05

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
        motion = simu.cat.waypoint
        bat = morse.cat.cat_battery
        start = time.time()
        bat_lev = battery_life(bat)
        is_free = True
        cnt = 0
        while (bat_lev > 50 and is_free == True):
            bat_lev = battery_life(bat)
            catPosition = where_is(catPose)
            mousePosition = where_is(mousePose)
                # go behind the mouse
            if(is_hiding( mousePosition['y'], mousePosition['x']) == False):
                if(how_far(catPosition['y'], mousePosition['y'], catPosition['x'], mousePosition['x']) == True):
                    is_free = False
                    print("CAPTURE")
                    print_res(bat_lev, start)
                else:
                    pursue_mouse(mousePosition['y'], mousePosition['x'], mousePosition['z'], mousePosition['yaw'], motion)
            else:
                is_free = True

            # send the command through the socket
        catPosition = where_is(catPose)
        motion.publish({"x":51.0, "y":-59, "z": height, "yaw": catPosition['yaw'], "tolerance": 0.5, "speed": 5})
        while(mousePosition['x'] != -6.363116264343262 or mousePosition['y'] != 45.8295783996582):
            time.sleep(1)
        print_res(bat_lev, start)

def print_res(battery_level, start):
    print(battery_level)
    end = time.time()
    time_taken = end - start
    print(time_taken)


def pursue_mouse(mouse_y, mouse_x, mouse_z, mouse_yaw, motion):
    waypoint = {    "x": mouse_x, \
                    "y": mouse_y, \
                    "z": height, \
                    "yaw": mouse_yaw, \
                    "tolerance": 0.02, \
                    "speed": 5\
                }
            #print("%s" % is_free)
    # if(mouse_x==cat_x):
    #      waypoint['yaw']= math.sign(mouse_y-cat_y) * math.pi
    # else:
    #     waypoint['yaw']= math.atan2(mouse_y-cat_y,mouse_x-cat_x)
    motion.publish(waypoint)


def battery_life(agentBattery_stream):
    """ Read data from the [mouse|cat] pose sensor, and determine the position of the agent """
    set = agentBattery_stream.get()
    charge = set['charge']
    return charge

def how_far(mouse_y, cat_y, mouse_x, cat_x):

    distance1 = math.sqrt(sum([(cat_x - mouse_x) ** 2 + (mouse_y - cat_y) ** 2]))

    if distance1 < 0.139:
        return True
    else:
        return False

def is_hiding(mouse_y, mouse_x):
    pos1 = {'x' : 43.4794807434082, 'y': 0.876022458076477, 'z': 0.08955984562635422, 'tolerance' : 0.5, 'speed' : 4.0}
    pos2 = {'x' : -38.12936019897461, 'y': -42.35550308227539, 'z': 4.007661819458008, 'tolerance' : 0.5, 'speed' : 4.0}
    pos3 = {'x': -42.76996612548828, 'y': 56.309364318847656, 'z': 0.5312402248382568, 'tolerance' : 0.5, 'speed' : 4.0}
    if(42 <= mouse_x <= 45 and -1<=mouse_y<=2):
        return True
    elif(-40 <= mouse_x <= -37 and -44<=mouse_y<=-41):
        return True
    elif(-44 <= mouse_x <= -41 and 55<=mouse_y<=58):
        return True
    else:
        return False


def main():
    """ Main behaviour """
    frighten_mouse()

if __name__ == "__main__":
    main()
