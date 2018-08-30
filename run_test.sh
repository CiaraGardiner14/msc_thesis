#!/bin/bash

echo "TEST"
sleep 15 

Range = 30
number=$RANDOM
let "number %= $RANGE"

echo "$number"

python3 mouse_move.py &
sleep $number &
python3 Cat_waypoints_pymorse_socket_script.py

exit 0


