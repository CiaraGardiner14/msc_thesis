#!/bin/bash
 for i in `seq 1 50`;
        do
		morse run flying_outdoor_cat_mouse_game.py&
		sleep 20
		NUMBER=$[ ( $RANDOM % 30 )  + 1 ]
		echo "$NUMBER"
		AR+=("$NUMBER")
		python3 mouse_move.py &
		sleep $NUMBER 
		python3 Cat_waypoints_pymorse_socket_script.py
                echo $i
        done 
echo "$NUMBER"
echo "delay is:"
echo ${AR[*]}
exit 0


