import pymorse
import sys, termios, tty, os, time
import math
from pymorse import Morse

from morse.builder import *

def print_pos(pose):
    print("I'm currently at %s" % pose)

def go_to():
    with pymorse.Morse() as simu:

        # subscribes to updates from the Pose sensor by passing a callback
        #simu.mouse.pose.subscribe(print_pos)

        # sends a destination
        simu.mouse.motion.publish({'x' : 10.0, 'y': 5.0, 'z': 0.0,
                                  'tolerance' : 0.5,
                                  'speed' : 1.0})

        # Leave a couple of millisec to the simulator to start the action
        simu.sleep(0.1)
        while simu.mouse.motion.get_status() != "Arrived":


        # waits until we reach the target
            char = getch()

            if (char == "p"):
                go_three()

            else:
                simu.sleep(0.5)


        print("Here we are!")

def go_three():

    #Fleeing reaction called when p button hit
    with pymorse.Morse() as simu, Morse() as morse:

        # subscribes to updates from the Pose sensor by passing a callback
        #simu.mouse.pose.subscribe(print_pos)

        mousePose = morse.mouse.mousePose

        mousePosition = where_is(mousePose)

        destination = go_where(mousePosition)

        simu.mouse.motion.publish(destination)

        simu.sleep(20)

        # sends a destination
        simu.mouse.motion.publish({'x' : 10.0, 'y': 5.0, 'z': 0.0,
                                  'tolerance' : 0.5,
                                  'speed' : 4.0})

        # Leave a couple of millisec to the simulator to start the action
        simu.sleep(0.1)

        # waits until we reach the target
        while simu.mouse.motion.get_status() != "Arrived":
            simu.sleep(0.5)

        print("Here we are!")

        go_to()

def go_where(mousePosition):

    pos1 = {'x' : 50.0, 'y': 20.0, 'z': 0.0, 'tolerance' : 0.5, 'speed' : 4.0}

    pos2 = {'x' : -50.0, 'y': -20.0, 'z': 0.0, 'tolerance' : 0.5, 'speed' : 4.0}

    pos3 = {'x' : 25.0, 'y': -20.0, 'z': 0.0, 'tolerance' : 0.5, 'speed' : 4.0}


    """if{mousePosition['x'] - pos1['x']} < {mousePosition['x'] - pos2['x']} and {mousePosition['y'] - pos1['y']} < {mousePosition['y'] - pos2['y']} and\
        {mousePosition['x'] - pos1['x']} < {mousePosition['x'] - pos3['x']} and {mousePosition['y'] - pos1['y']} < {mousePosition['y'] - pos3['y']}:
        optdist = pos1

    elif{mousePosition['x'] - pos2['x']} < {mousePosition['x'] - pos1['x']} and {mousePosition['y'] - pos2['y']} < {mousePosition['y'] - pos1['y']} and\
        {mousePosition['x'] - pos2['x']} < {mousePosition['x'] - pos3['x']} and {mousePosition['y'] - pos2['y']} < {mousePosition['y'] - pos3['y']}:
        optdist = pos2

    elif{mousePosition['x'] - pos3['x']} < {mousePosition['x'] - pos1['x']} and {mousePosition['y'] - pos3['y']} < {mousePosition['y'] - pos1['y']} and\
        {mousePosition['x'] - pos3['x']} < {mousePosition['x'] - pos2['x']} and {mousePosition['y'] - pos3['y']} < {mousePosition['y'] - pos2['y']}:
        optdist = pos3"""

    distance1 = math.sqrt(sum([(mousePosition['x'] - pos1['x']) ** 2 + (mousePosition['y'] - pos1['y']) ** 2]))
    distance2 = math.sqrt(sum([(mousePosition['x'] - pos2['x']) ** 2 + (mousePosition['y'] - pos2['y']) ** 2]))
    distance3 = math.sqrt(sum([(mousePosition['x'] - pos3['x']) ** 2 + (mousePosition['y'] - pos3['y']) ** 2]))

    if distance1 < distance2 and distance1 < distance3:
        optdist = pos1

    if distance2 < distance1 and distance2 < distance3:
        optdist = pos2

    if distance3 < distance1 and distance3 < distance2:
        optdist = pos3


    """else:
        optdist = pos1"""

    print("I'm going to %s" % optdist)

    return optdist

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


def main():
    """ Main behaviour """
    go_to()

if __name__ == "__main__":
    main()
