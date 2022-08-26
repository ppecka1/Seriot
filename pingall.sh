#!/bin/bash
rsh seriot1 ping 10.0.1.2 &
rsh seriot1 ping 10.0.1.3 &
rsh seriot1 ping 10.0.1.4 &
rsh seriot1 ping 10.0.1.5 &
rsh seriot1 ping 10.0.1.6 &


rsh seriot2 ping 10.0.1.1 &
rsh seriot2 ping 10.0.1.3 &
rsh seriot2 ping 10.0.1.4 &
rsh seriot2 ping 10.0.1.5 &
rsh seriot2 ping 10.0.1.6 &

rsh seriot3 ping 10.0.1.1 &
rsh seriot3 ping 10.0.1.2 &
rsh seriot3 ping 10.0.1.4 &
rsh seriot3 ping 10.0.1.5 &
rsh seriot3 ping 10.0.1.6 &

rsh seriot4 ping 10.0.1.1 &
rsh seriot4 ping 10.0.1.2 &
rsh seriot4 ping 10.0.1.3 &
rsh seriot4 ping 10.0.1.5 &
rsh seriot4 ping 10.0.1.6 &

rsh seriot5 ping 10.0.1.1 &
rsh seriot5 ping 10.0.1.2 &
rsh seriot5 ping 10.0.1.3 &
rsh seriot5 ping 10.0.1.4 &
rsh seriot5 ping 10.0.1.6 &

rsh seriot6 ping 10.0.1.1 &
rsh seriot6 ping 10.0.1.2 &
rsh seriot6 ping 10.0.1.3 &
rsh seriot6 ping 10.0.1.4 &
rsh seriot6 ping 10.0.1.5 &




#ping 10.0.1.1 &
#ping 10.0.1.2 &
#ping 10.0.1.3 &
#ping 10.0.1.4 &
#ping 10.0.1.5 &
#ping 10.0.1.7 &

# 
echo "start to sleep 10 s"
sleep 5
echo "end of sleeping"
echo "killing ping processes"
rsh seriot1 pkill ping #&
rsh seriot2 pkill ping #&
rsh seriot3 pkill ping #&
rsh seriot4 pkill ping #&
rsh seriot5 pkill ping #&
rsh seriot6 pkill ping #&
#pkill ping
echo "end of killing ping processes"

