IP_ADDR="10.0.1." # na test bandzie  zmienic MAX liczba wezlow: 0xFF-1 :ostatni bajt
NS=6 #liczba switchy mozna odczytac funkcja  createLinksDijkstra("connections12mesh.pickle")
#TestMode=True #rowne opoznienia do testow MOZLIWE sztuczne obciazenie wybranych wezlow:   *simple_switch0_Mat.py* linia: @wagi
TestMode=False
RoutingAlgo= 1 # 0 (DA) 1 (DW) 2 (Rnn) Dijkstra bez wag, z wagami, oparty o siec  neuronowa 
ALFA=0.15 # parametr sredniej wazonej dla algorytmu DW 
#EqualWeigthMode=False 
################################
NaS=0.000000001 # nano sekunda
US=0.000001 # mikro sekunda
MS=0.001 
Sec=1.0 #float
SEC=1 # integer
##################################
SendIntCog=10000*MS# odstep czasu  [US,MS] miedzy wysylanymi  pakietami Cognitywnymi 
FlowTimeOut=400*SEC  # po tym czasie wywolany zostanie alg. routingu
CAP=1000 # pojemnosc zgloszen pakietow kognitywnych (default 1000)- po przekroczeniu - wywolanie alg. Routingu
COPORT=5007 # nr portu dla pakietow COG :   TYLKO  mininet 
PRIOCOG=58888 # priorytet dla COG - nie uzywane na TestBed (prio=12345, obowiazuje dla wszystkich pakietow)
UDP_CTRL=5006 # wyslanie na ten port przekierowuje pakiet do kontrolera plik   *AsM.py*
BUFSIZE=1024
DELTA=1*1000 #  opoznienie progowe   [NS] - ponizej nie wysylamy infomacji do kontrolera  *AsM.py*
#####################################
# po uruchomieniu aliasu asm pojawia sie ponizsze reguly TYLKO dla  conf.RoutingAlgo>0
USPORT=5008 # nr portu dla pakietow USER *users.py*  *Userv.py* /mininet: *user.cli* *init12sv.cli*
PRIOUS=58889 # priorytet dla pakietow user  (proporcjonalnie do wielkosci)
SendIntUser=0.0001*MS# odstep czasu [US,MS] miedzy wysylanymi  pakietami
NP=4000000 # liczba pakietow wysylanych prze USER plik:  *users.py*
# plik binarny z topolagia sieci dla alg routingu : plik *topo_dijkstra.py* *RoutingAlgoInterface.py* *simple_switch0_Mat.py*
TOPO="connections12mesh.pickle" # wykorzystano w Mini Net : nazwa pliku
################################
# Topologia dla Test Bed:
edges6=[(1, 2, 1, 1), (1,3,1,2),(2,1,1,1),(2,4,1,2),(3,1,1,1),(3,4,1,2),(3,5,1,3),  
        (4,2,1,1),(4,3,1,2),(4,6,1,3),(5,3,1,1),(5,6,1,2),(6,4,1,1),(6,5,1,2),(6,0,0,0)]  # (src,dst,waga,port) 
# adresy wezlow od 1 do 6 ,  dpid=0 nie uzywamy
MACS=['','54:b2:03:93:e9:7d','54:b2:03:93:75:2b','54:b2:03:93:50:9e','54:b2:03:93:ea:94','54:b2:03:93:e7:b3','54:b2:03:93:76:53']


# pingi 10.0.1.x do 10.0.1.y powinny dzialac wezlach
# pingi 10.0.2.x do 10.0.2.y powinny dzialac na wszystkim
"""
poleceniea arp na seriot (kontroler):


seriot@seriot:~/ryu/ryu/app$ arp
Address                  HWtype  HWaddress           Flags Mask            Iface
_gateway                 ether   04:d5:90:bf:ca:26   C                     wlp6s0
seriot1                  ether   54:b2:03:93:e9:7e   C                     eno1
seriot3                  ether   54:b2:03:93:50:9f   C                     eno1
seriot2                  ether   54:b2:03:93:75:2c   C                     eno1
seriot5                  ether   54:b2:03:93:e7:b4   C                     eno1
seriot4                  ether   54:b2:03:93:ea:95   C                     eno1
seriot6                  ether   54:b2:03:93:76:54   C                     eno1

#tu sa statyczne MAC-i
less /etc/ethers 

#MAC-i recznie
sudo arp -s 10.0.1.1 54:b2:03:93:e9:7d  statyczne MACI ??????
sudo arp -s 10.0.1.2 54:b2:03:93:75:2b
sudo arp -s 10.0.1.3 54:b2:03:93:50:9e
sudo arp -s 10.0.1.4 54:b2:03:93:ea:94
sudo arp -s 10.0.1.5 54:b2:03:93:e7:b3
sudo arp -s 10.0.1.6 54:b2:03:93:76:53
"""
# SEKWENCJA WYWOLAN : kip,def,kontroler,pil, asm
# wazne komendy:
#sudo tshark -i br0
#arp
#ip a
#ssh seriot1 sudo ovs-ofctl dump-flows br0 
# geany plugin manager : addons - podswietla wszystkie wystapienia 
#http://localhost:8080/
#:~/ryu$ PYHTONPATH=. ryu-manager  --observe-links ryu/app/gui_topology/gui_topology.py ryu/app/simple_switch_13.py
"""

#to wszystko  recznie na wezlach, nie na seriot, zeby postawic openvswitch

 sudo ip link set eno1 down
  599  ip a
  600  sudo ip link set eno1.134 up  !!!!!!!!!!!
  601  sudo ip link set eno1 up  ???????? !!!!!!
  602  ip a
  603  sudo ip link del ovs-system
  604  sudo systemctl start  openvswitch-switch
  605  sudo ovs-vsctl show
  606  ovs-vsctl add-port br0 eno1.134
  607  sudo ovs-vsctl add-port br0 eno1.134
  608  ip r
  609  ping 10.0.134.1
  610  sudo systemctl stop openvswitch-switch.service # stop  
  611  sudo ls /etc/openvswitch/*
  612  sudo rm /etc/openvswitch/conf.db  -  usuniecie konfiguracji
  613  sudo ls /etc/openvswitch/* 
  614  sudo ovs-vsctl show  - pokazuje wirualne karty 
  615  sudo systemctl start openvswitch-switch.service tworzy db ? 
  616  sudo ovs-vsctl show
  617  sudo ovs-vsctl add-br br0
  618  sudo ovs-vsctl show
  619  sudo ovs-vsctl add-port br0 eno1.124  #jak numeruje porty trze
  620  sudo ovs-vsctl add-port br0 eno1.134
  621  sudo ovs-vsctl add-port br0 eno1.146
  622  sudo ovs-vsctl set-controller br0 tcp:10.0.2.50:6633  # na kazdym wezle pokazuje gdzie jest kontr
  623  sudo ovs-vsctl set bridge br0 other_config:datapath-id=0000000000000004 # datapath   ?????????????????
  624  sudo ovs-ofctl show br0
  625  ip a
  626  sudo ip addr add 10.0.1.4/24 dev br0  ??????????????????
   pip3 install oslo_config ????
   traceroute 8.8.8.8
    ip a show dev eno1
 sudo dhclient enp5s0 ??????????
  statyczne MACI
  cat /etc/network/interfaces - inf o kartach wirtualnych  zwiazane z tym sudo ip link set eno1.134 up  !!!!!!!!!!! 
  cat /etc/network/if-up.d/br0 # na wezlach, nie na seriot

 sudo ip a add 10.0.1.50/24 dev enp5s0 
 2133  ip a
 2134* sudo ip a del 10.0.1.50/24 dev enp
 2135  sudo ip a add 10.0.1.50/24 dev eno1
 2136  ip a
 2137  sudo apt install ntpdate
 2138  shall sudo apt install ntpdate
 2139  shall sudo apt update
 2140  shall sudo apt install ntpdate
 2141  sudo apt install ntp
 2142  less /etc/ntp.conf 
 2143  sudo systemctl start ntp.service 
 2144  sudo systemctl status ntp.service 
 2145  shall sudo apt install ntp
 2146  shall sudo apt -y install ntp
 2147  vim /etc/ntp.conf 
 2148  sudo vim /etc/ntp.conf 
 2149  sudo systemctl restart ntp.service 
 2150  sudo systemctl status ntp.service 
 2151  scp ntp.conf seriot@seriot1:~
 2152  scp ntp.conf seriot@seriot2:~
 2153  scp ntp.conf seriot@seriot3:~
 2154  scp ntp.conf seriot@seriot4:~
 2155  scp ntp.conf seriot@seriot5:~
 2156  scp ntp.conf seriot@seriot6:~
 2157  shall sudo cp ntp.conf /etc
 2158  shall sudo systemctl restart ntp.service
 2159  shall sudo systemctl status ntp.service
 2160  shall sudo systemctl stop ntp.service
 2161  shall sudo ntpdate 10.0.2.50
 2162  shall sudo systemctl start ntp.service




"""


