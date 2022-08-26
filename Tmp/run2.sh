#!/bin/bash
# RUN !
#javac -cp ".:./unitedRNNPlugin.jar:" SimulatorCommunicator.java
#cp SimulatorCommunicator.class  /home/osboxes/mininet/Rnn/Tmp/org/iitis/implementation
cd Tmp
java  org.iitis.InformationFeeder ../$1.json pipe
