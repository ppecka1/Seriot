[General]
#
#$$$$$$$$$$$$$$$$$$ UWAGA Ruch pakietow USER jest definowany w myUDPbasicApp.cc linia 473
#
#cpu-time-limit =0.01s NIE DZIALA!!!
#sim-time-limit =0.2s opcjonalnie //104,26,104,26 ....(pakietow odebranych)
sim-time-limit =1s # dlugi czas bo pakiety nie zdaza dotrzec
network = openflow.scenarios.Scenario14nodes
ned-path = /Users/PiotrPecka/Desktop/omnetpp-4.2-src-windows/inet/src/;/Users/PiotrPecka/Desktop/omnetpp-4.2-src-windows/omnetpp-4.2/projects/openflow

output-vector-file = ${resultdir}/${inifile}/${inifile}-${runnumber}.vec
output-scalar-file = ${resultdir}/${inifile}/${inifile}-${runnumber}.sca

debug-on-errors = false
**.open_flow_switch*.etherMAC[*].doRegisterAtIft = false 

# UDP app ( PECK)
**.numUdpApps = 2
# musi byc plik:myUDPBasicApp.ned dzidziczy (like) IUDPApp
**.udpApp[0].typename = "myUDPBasicApp"
**.udpApp[1].typename = "myUDPBasicApp"
#**.server1.udpApp[0].typename = "UDPBasicApp"
#**.server2.udpApp[0].typename = "UDPBasicApp"
#**.server*.udpApp[0].active = false
**.udpApp[0].localPort = 5005  # wysyla i nasluchuje
**.udpApp[0].destPort = 5005   
**.udpApp[1].localPort = 5006
**.udpApp[1].destPort = 5006
**.udpApp[*].messageLength = 1000B

#************tu opozniamy**********************************************szenario_Domains.ini:
#    opoznienie  switcha  dla licznikow:   OpenflowProcessing

#
#       UWAGA   sendInterval=0.05 - 13 ; 0.005 - 130 pakietow ; 0.0005 - 1300 pakietow 
#   

###  pakiety COGNITYWNE port=5005

#@%^&*@#$%^&*@#$#$%^^&& NAJWAZNIEJSZA CZESC

**.ctrlApp.routingAlg = 2 # 1: DW (z wagami)  0: DA (bez wag) 2:RN  ctrlApps/Switch.ned
**.udpApp[0].startTime  = 0.0s  # pakiety wysylane po czasie start !!! dla SD (pakiety kognitywne) startTime = 0s !!!
**.udpApp[0].stopTime   = 6.0s   # 0.1pakiety wysylane przez start-stop czasu globalnie dla wszystkich

#!!!!!!!!!!!!!!!!!!!!!!!!!!!1
**.udpApp[0].sendInterval = 1s  #0.05  dla RNN 15 minut trwa symulacja
#!!! TYLKO SERVER dla SD linia 174 myUDPBasicApp.cc !!! nadaje ?? 100 kazdy nadaje 1 do kazdego 6*7; 10- kazdy nadaje 15; 2- nadaje 8; 0.1 150 pakietow
# $*&$&* TIMEOUT *********************************
#************************************************ to=0.001s, opoz=256  timeout=0.1 opoz=38 0.01 opoz=60  0.001 25opoz=43//DA opoz=257
# timeout do wszystkich , jak do jednego nie ma efektu
#   st =0.00025 (32Mb/s),  0.00005 (160Mb/s) 0.0001 80Mb/s
**.open_flow_switch*.ofa_switch.flow_timeout = 0.1s # czas ustawiania nowych flowow PPECKA  0- co chwile resetuje
**.open_flow_switch*.alfa=1 # parametr dla zuzycia energi (0) i 
                            #wydajnosci(1) alfa=<0,1> 
**.open_flow_switch*.serviceTime = 0.000025s # nie może być 0.00004 albo mniej, bo nie wychodzi; mniese niz 0.0000005s nie zmienia opozniien

#@%^&*@#$%^&*@#$#$%^^&& NAJWAZNIEJSZA CZESC KONIEC 
#################

#           serwis time: ponizej 0.00002s: 22/56  powyzej 0.00005 266/60
#USER:

#**************************UWAGA jesli stopTime<startTime SYMULATOR WYLATUJE Z DZIWNYM BLEDEM
#INTENSYWNE: 3--->10 ; 4--->9; 
**.sd3.udpApp[1].startTime  = 0.15s #bylo 0.05
#**.sd3.udpApp[1].stopTime   = 1.0s  # 0.1
**.sd3.udpApp[1].sendInterval = exponential(0.0005s) #

**.sd4.udpApp[1].startTime  = 0.1s #bylo 0.05
#**.sd4.udpApp[1].stopTime   = 1.0s  # 0.1
**.sd4.udpApp[1].sendInterval =exponential(0.0005s) #
#sendinterval< 0.00005 :  <!> Error in module (EtherMACFullDuplex) Scenario_SPT_Small.sd4.eth[0].mac (id=106) at event #902473, t=0.4473: #Model error: txQueue length exceeds 10000 -- this is probably due to a bogus app model generating excessive traffic #(or if this is normal, increase txQueueLimit!).
**.sd*.udpApp[1].startTime  = 0s
**.sd*.udpApp[1].sendInterval = exponential(0.05s) #
**.udpApp[1].stopTime   = 1.0s 

**.udpApp[0].msgName="user pack. (app 0)"
**.udpApp[1].msgName="user pack. (app 1)"

#   @@@@@@@@@@@@@  USTAWIANIE HOSTOW 

# z servera 1 polaczenia do 3 serwero intensywnos jak dla SD
#**.server1.udpApp[0].destAddresses= "192.168.1.3  192.168.1.7 192.168.1.8 192.168.1.19"   
#**.server0.udpApp[0].destAddresses= "192.168.1.4"            
#**.server*.udpApp[0].destAddresses="192.168.1.1 192.168.1.2 192.168.1.3 192.168.1.4 192.168.1.5 192.168.1.6 192.168.1.7 192.168.1.8"
# od 1 do 0.1 s cos se dzieje
#**.server*.udpApp[0].sendInterval = 0.5s #8* pakietow =40  USER >> 0.01 max do wszystkich rownoczesnie



#   @@@@@@@@@@@@@  USTAWIENIA SD (zrodla COGN)  NIE AKTUALNE!!!!!!!!!!!!!!!!
#**.open_Flow_Processing.mode=1 #  SPTree(0);  Dijkstra(1) Rnn(2)
#**.udpApp[0].sendInterval = 0.3s #50 pakietow  COGN


#Czesty timeout nie jest dobry
##########################
#################
###  pakiety COGNITYWNE port=5005 ROZNE TIMEOUTY
###################
#**.open_flow_switch1.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch2.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch3.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch4.ofa_switch.flow_timeout = 0.001s # 
#**.open_flow_switch5.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch6.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch7.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch8.ofa_switch.flow_timeout = 0.001s # 
#**.open_flow_switch9.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch10.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch11.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch12.ofa_switch.flow_timeout = 0.001s
#**.open_flow_switch13.ofa_switch.flow_timeout = 0.001s
#Dijkstra optymalny: switch zna cala topologie i wagi na biezaco nie uzywa tablicy flowow- do porownania  z gorszymi #algorytm


#szenario_Domains.ini:**.controller.serviceTime = 0.00024s
# open_flow_switch1: Open_Flow_Switch

#**.sd0.udpApp[0].destAddresses="192.168.1.2 192.168.1.3 192.168.1.7"  # #CEL:  server4 MAC_00-12
#**.server0.udpApp[0].destAddresses="192.168.1.2 192.168.1.3 192.168.1.7"  # #CEL:  server4 MAC_00-12
#**.server*.udpApp[0].burstDuration = 0.4s
#**.server*.udpApp[0].sleepDuration = 0.3s


#openflow
**.controller.ofa_controller.port = 6633
**.open_flow_switch*.sendCompletePacket = true #// PP mod Uwaga bylo: false
#**.controller.behavior = "Switch" #PPECKA - sterownik kontrolera : forwarding, switch(SPT) , moj (Dijkstra)

**.ofa_switch.connectPort = 6633
**.ofa_switch.connectAddress = "controller"
**.buffer.capacity = 10

**.open_flow_switch*.etherMAC[*].promiscuous = true
#**.controller.ofa_controller.address = 

# NIC configuration
**.ppp[*].queueType = "DropTailQueue" # in routers
**.ppp[*].queue.frameCapacity = 10 # in routers

*.configurator.networkAddress = "192.168.1.0"

**.open_flow_switch*.tcp.mss = 800
**.controller.tcp.mss = 800 #smax segm. size tcp protokol UWAGA sprawdz obcinanie wiadomosci
#**.controller.serviceTime = 0.00024s
 
###  pakiety UZYTKOWNIKA port=5006
#**.udpApp[1].startTime  = 0.0s #bylo 0.05
#**.udpApp[1].stopTime   = 1.0s  # 0.1
#**.udpApp[1].sendInterval = 0.005s #exponential(0.005s) # 0.05 1 pakiet ...   0.0005 100 pakietow 

# schemat polaczen: plik myUDPBasicApp.c 
#  0 ---->n , 1 ---> n-1 , 2 ---> n-2 ....
#**.sd0.udpApp[1].sendInterval = 0.05s # 0 ---> 13 (1000pakietow) 0.00005
#**.sd1.udpApp[1].sendInterval = 0.05s #  1--->12 (10 p)
#**.sd2.udpApp[1].sendInterval = 0.05s #  2 --->11 (10p)
#**.sd3.udpApp[1].sendInterval = 0.05s #
#**.sd4.udpApp[1].sendInterval = 0.05s #
#**.sd5.udpApp[1].sendInterval = 0.05s #
#**.sd6.udpApp[1].sendInterval = 0.05s #
#**.sd7.udpApp[1].sendInterval = 0.05s #
#**.sd8.udpApp[1].sendInterval = 0.05s #
#**.sd9.udpApp[1].sendInterval = 0.05s #
#**.sd10.udpApp[1].sendInterval = 0.05s #
#**.sd11.udpApp[1].sendInterval = 0.05s #
#**.sd12.udpApp[1].sendInterval = 0.05s # 12--->11 (1000 p)
#**.sd13.udpApp[1].sendInterval = 0.05s # 13--->0 (1000 pakietow) 0.00005
#   !!! DLA SD: !!!   const double CogPackInterval=0.1;// myUDPBasicApp.cc linia 31

#**.server0.udpApp[0].sendInterval = 0.003s 
#**.server1.udpApp[0].sendInterval = 0.004s 
#sd0.udpApp[0].sendInterval = 0.05s
#**.udpApp[1].startTime = 0s
#**.udpApp[1].stopTime =  5s
#**.udpApp[0].sendInterval = 0.0001s

#server0.udpApp[0].startTime = 0s # pakiety wysylane po czasie start
#server0.udpApp[0].stopTime =  0s  # pakiety wysylane przez start-stop czasu

#**.udpApp[1].sendInterval = 1s
