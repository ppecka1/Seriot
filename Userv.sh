#!/bin/bash
echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
echo  "  Uruchomienie USERS -ow:  pingall;  Test Bed"
echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#ssh rm rapas* 

ssh seriot1 python3 Userv.py  1   >>rapas  2>>rapaser&
ssh seriot2 python3 Userv.py  2   >>rapas  2>>rapaser&
ssh seriot3 python3  Userv.py 3   >>rapas  2>>rapaser&
ssh seriot4 python3 Userv.py  4   >>rapas  2>>rapaser&
ssh seriot5 python3  Userv.py 5   >>rapas  2>>rapaser&
ssh seriot6 python3  Userv.py 6   >>rapas  2>>rapaser&
