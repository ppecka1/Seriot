#!/bin/bash
echo "killing ping processes"
rsh seriot1 pkill ping #&
rsh seriot2 pkill ping #&
rsh seriot3 pkill ping #&
rsh seriot4 pkill ping #&
rsh seriot5 pkill ping #&
rsh seriot6 pkill ping #&
pkill ping
echo "end of killing ping processes"

