#!/bin/bash
# COMPILE !
javac -cp ".:./unitedRNNPlugin.jar:" SimulatorCommunicator.java
#cp SimulatorCommunicator.class  /home/osboxes/mininet/Rnn/Tmp/org/iitis/implementation
#cd Tmp
#  org.iitis.InformationFeeder  to klasa MAIN info w Tmp/META-INF/MANIFEST.MF 
#java  org.iitis.InformationFeeder topology3.json pajp
# rozpakowac wczesniej:  jar -xf unitedRNNPlugin.jar
#nie dzdiala: find mininet  -type f   -iname "*.py" -o  -iname "*.java" -o -iname "*.sh" -o -iname "*.json" -not -print0 | tar -cvf somefile.tar --null -T -
# ok:    find mininet  -type f   -name "*.py" -o  -name "*.java" -o -name "*.sh" -o -name "*.json"  -o -name "*.txt"|tar -cf somefile.tar  -T -
