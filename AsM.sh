#!/bin/bash
echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
echo  "  Uruchomienie AS -ow:  pingall;  Test Bed"
echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#ssh rm rapas* 

ssh seriot1 sudo python3 AsM.py  1   >>rapas  2>>rapaser1&
ssh seriot2 sudo python3 AsM.py  2   >>rapas  2>>rapaser2&
ssh seriot3 sudo python3 AsM.py  3   >>rapas  2>>rapaser3&
ssh seriot4 sudo python3 AsM.py  4   >>rapas  2>>rapaser4&
ssh seriot5 sudo python3 AsM.py  5   >>rapas  2>>rapaser5&
ssh seriot6 sudo python3 AsM.py  6   >>rapas  2>>rapaser6&
