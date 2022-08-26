#!/bin/bash
echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
echo  "  Uruchomienie AS -ow:  pingall;  Test Bed"
echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#ssh rm rapas* 

ssh seriot1 python3 AsM.py  1   >>rapas  2>>rapaser&
ssh seriot2 python3 AsM.py  2   >>rapas  2>>rapaser&
ssh seriot3 python3 AsM.py  3   >>rapas  2>>rapaser&
ssh seriot4 python3 AsM.py  4   >>rapas  2>>rapaser&
ssh seriot5 python3 AsM.py  5   >>rapas  2>>rapaser&
ssh seriot6 python3 AsM.py  6   >>rapas  2>>rapaser&
