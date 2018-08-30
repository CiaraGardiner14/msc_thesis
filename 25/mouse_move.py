#Cautious mouse. Moves when drone is closer than 30m and hides until drone is gone


import pymorse
import sys, termios, tty, os, time, datetime
import math
import csv
from pymorse import Morse
from morse.builder import *

def main():
    print("Test")
    with pymorse.Morse() as simu, Morse() as morse:
        """ Main behaviour """
        mousePose = morse.mouse.mousePose
        motion = morse.mouse.motion
        destination = set_pos(simu, morse)
        start = time.time()
        bat = morse.mouse.mouse_battery
        waypoint = destination
        motion.publish(waypoint)
        first_attack = True
        while motion.get_status()!= 'Arrived':
            print_res(bat, start)
            mousePosition = where_is(mousePose)
            if(check_speed(simu, morse) == 1 and check_hide(simu, morse) != 1 and first_attack == True):
                print("running")
                destination = {'x' : -6.363116264343262, 'y': 45.8295783996582, 'z': 0.0,
                                              'tolerance' : 0.5,'speed': 4.0}
            elif(check_hide(simu, morse) == 1 and first_attack == True):
                print("hiding")
                motion.publish(go_where(mousePosition))
                first_attack = False
                for i in range(120):
                    time.sleep(1)
                    print_suc_res(bat, start, "HIDING")
            elif(check_speed(simu, morse) == 1 and first_attack == False):
                print("Running 2")
                # motion.publish({'x' : -6.363116264343262, 'y': 45.8295783996582, 'z': 0.0,
                #                               'tolerance' : 0.5,
                #                               'speed' : 4.0})

            motion.publish(destination)
        print("Here we are!")
        print_suc_res(bat, start, "SUCCESS")

def set_pos(simu, morse):
    destination = {'x' : -6.363116264343262, 'y': 45.8295783996582, 'z': 0.0,
                                  'tolerance' : 0.5,
                                  'speed' : 2.0}
    return destination

def print_suc_res(bat, start, status):

    battery_level = battery_life(bat)
    print(battery_level)
    end = time.time()
    time_taken = end - start
    print(time_taken)

    row = [battery_level, time_taken, status]
    with open('results.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()

def print_res(bat, start):

    battery_level = battery_life(bat)
    print(battery_level)
    end = time.time()
    time_taken = end - start
    print(time_taken)

    row = [battery_level, time_taken]
    with open('results.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()

def check_speed(simu, morse):
    nearObj = morse.mouse.proximity
    curr = near_robot(nearObj)
    if (curr and 1 < curr < 30):
        return 1
    else:
        return 0

def check_hide(simu, morse):
    nearObj = morse.mouse.proximity
    curr = near_robot(nearObj)
    if (curr and 1 < curr < 30):
        return 1
    else:
        return 0

def go_where(mousePosition):
    pos1 = {'x' : 43.4794807434082, 'y': 0.876022458076477, 'z': 0.08955984562635422, 'tolerance' : 0.5, 'speed' : 4.0}
    pos2 = {'x' : -38.12936019897461, 'y': -42.35550308227539, 'z': 4.007661819458008, 'tolerance' : 0.5, 'speed' : 4.0}
    pos3 = {'x': -42.76996612548828, 'y': 56.309364318847656, 'z': 0.5312402248382568, 'tolerance' : 0.5, 'speed' : 4.0}

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

def near_robot(agentProximity_stream):
    """ Read data from the [mouse|cat] pose sensor, and determine the position of the agent """
    pose = agentProximity_stream.get()
    ind = pose['near_robots']
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

def print_pos(pose):
    print("I'm currently at %s" % pose)

if __name__ == "__main__":
    main()
