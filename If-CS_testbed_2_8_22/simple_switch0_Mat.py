# Copyright (C) 2021 IITIS PAN
# Copyright (C) 2021 Mateusz Nowak
# & Piotr Pecka:  piotr@iitis.pl ZmioesK

#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import networkx as nx # STP kod Mateusza

from ryu.topology.api import get_all_switch
#, get_all_link, get_all_host, get_switch,get_link
from ryu.app.ofctl.api import get_datapath
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.topology import event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, ipv4, arp, udp,ipv6
# *******   WAZNE KOMENDY:  ******************:
#sudo mn --custom  ./proj12.py --topo=project  --mac --controller remote --switch ovsk,protocols=OpenFlow13
# rm -rf rap.tmp; ryu-manager  --observe-links   simple_switch0_Mat.py 2>rap.tmp >>rap.tmp

#BASH_PROMPT./ryu$       PYTHONPATH=~/.local ~/.local/bin/ryu run --observe-links ryu/app/gui_topology/gui_topology.py
#for i in {1..12}; do sudo ovs-ofctl  -O OpenFlow13 dump-flows s$i |grep 5008|wc; done
# python3 ifcsLinkMonitor.py   1  12   5008
#***********************************************
# Piotr Pecka
import conf  # plik konfiguracyjny

import  os, time,sys
from topo_dijkstra import nearestNodeDijkstra 
from topo_dijkstra import createLinksDijkstra
from util import hid2mac
from  RoutingAlgoInterface import RnnAlgo
from  RoutingAlgoInterface import DWAlgo
#TIME_OUT_SIGNAL=False
Sec=1 # sekunda
US=0.000001
MS=0.001
# test
#  sudo ovs-ofctl  dump-flows s1  SPRAWDZA FLOWE 

####### Parametry dal al Routingu:
#NS=12 #liczba switchy mozna odczytac funkcja  createLinksDijkstra("connections12mesh.pickle")
#FlowTimeOut=5*Sec  # po tym czasie wywolany zostanie alg. routingu
#CAP=100 # pojemnosc zgloszen pakietow kognitywnych - po przekroczeniu - wywolania alg. Routingu
#conf.TOPOUS=59999 # dla pakietow user i cog 
#conf.TOPOCOG=58888

#COPORT=5007 # nr portu dla pakietow COG
#USPORT=5008 # nr portu dla pakietow USER
#TOPO="connections12mesh.pickle" # plik binarny z topolagia sieci dla alg routingu
# ATENCJONE w lini @INIT_FLOW (topo_hostadd() ) ustawiane sa flowy dla COG (port 5007) i USER(port 5008) wg Dijkstry (DA, waga=1)
# w lini @VAR_FLOW ()  (packet_in_handler() )

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        logFileName="./Logs/logController.txt"
        if os.path.exists(logFileName):
            os.remove(logFileName)
        self.log = open(logFileName,"w")
        self.topo_no_lnk = self.topo_no_sw = self.topo_no_h = 0
        self.logcnt = 0
        #links = {} #slownik zawiera port i wage dla polaczenia (i,j) klucz: (i,j) warosc: (waga,port)
        if conf.RoutingAlgo==1:
            self.Algo=DWAlgo(conf.CAP,conf.FlowTimeOut,conf.NS)
        elif  conf.RoutingAlgo==2:
            self.Algo=RnnAlgo(conf.CAP,conf.FlowTimeOut,conf.NS) # inicjalizacja aalgorytmu
        else:
            self.Algo=None # conf.RoutingAlgo=0
        if self.Algo!=None:
            print ("******************************")
            print("   ",self.Algo.getAlgoName()) #
            print ("******************************")
        else:
            print ("******************************")
            print('    No weigth Dijkstra (default)' )              
            print ("******************************")
    
# nie ma tablicy jest slownik
#node2nodes=[10] # liasta wezel  zawiera linki do pozostalych

#print node2nodes[11]
        self.dpaths=[] # tablica dpath (rozmiar=liczba switchy) eypelniana w topo_hostadd
                      #- umozliwia jednorazowo ustawic wszystkie flowy we wszystkich switchach -add_flow()
        self.list_links = []
        self.list_switches = []
        self.list_switches2 = []
        self.list_hosts = []
        self.raw_hosts = []
        self.mac_to_port = {}
        self.net=nx.DiGraph()
        self.mst=nx.Graph()
        self. AS_port=1 # polaczenie Swich-->AS
        self.NS=conf.NS #liczba switchy
        self.first=True # pierwsze wejscie
        self.startTime=time.time() # dla logera - startujemy o startTime
        print  ("Halo: tu konstruktor kontrolera   init() - ja wywoluje sie tylko raz")

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# pojawił się nowy host
    @set_ev_cls(event.EventHostAdd)
    def topo_hostadd(self, ev):
        #UWAGA nie wywoluje sie
        print  ("Halo: tu topo_hostadd() z kontrolera - wywolujemy sie tyle razy ile jest hostow ")
        sys.stdout.flush()
        #Tu usstawimy flowy
        host = ev.host
        datapath = get_datapath(self, host.port.dpid)
        self.dpaths.append(datapath)
        dpid = datapath.id
        parser = datapath.ofproto_parser
        # regula dla pakietu ktorego adres docelowy jest równy adresowi Asa przypietego do tego switcha (ostatnia stacja) :
        match = parser.OFPMatch(eth_dst=host.mac,ip_proto=17, udp_dst=conf.COPORT, eth_type=0x0800)  # pakiet COG - port 5007
        action = [parser.OFPActionOutput(self. AS_port)]  # Swich--->AS
        #*************************************************************
        #                SWITCH ---- port 1  -----------> AS
        #self.logger.info("TOPO_HOSTadd (add_flow) lokalny  mac=%s -> out_port %d", host.mac, self.AS_port)
        if conf.RoutingAlgo!= -1: # -1 to brak algorytmu tylko SP
            self.add_flow(datapath, conf.PRIOCOG, match, action) # ten flow wysyla pakiet ethernetowy ze switcha do sąsziednieg (zaprzyjaźnionego) AS -a port AS_port=1
            match = parser.OFPMatch(eth_dst=host.mac,ip_proto=17, udp_dst=conf.USPORT, eth_type=0x0800)  # pakiet USER - port 5008
            action = [parser.OFPActionOutput(self. AS_port)]  # Swich--->AS (zaprzyjazniony) 
            self.add_flow(datapath, conf.PRIOUS, match, action) 
        ########################################################
        # pakiety zdalne:
        start=dpid
        #dest=Asid=int((host.mac).split(':')[5],16)
        if conf.RoutingAlgo!= -1: # -1 to brak algorytmu tylko SP
            #createLinksDijkstra(conf.TOPO) # w pliku o nazwie TOPO (binarny) info o topologi i wagach NIe POTRZENE ???
            nearestNode,NS=nearestNodeDijkstra(start,self.NS,cp=conf.TOPO) 
            #^   wyznacza najblizszy swicz i port do niego dla 
            #    WSZYSTKICH wezlow docelowych od pozycji start (wagi=1)
            if NS<0 or NS!=self.NS:
                assert(0)
        #***********************************************************************************************
        #                SWITCH ----  posredni port -----------> AS DIJKSTRA bez wag
        #*************** USTAWIENI POCZATKOWE dla user USPORT oraz cog  COPORT
        if conf.RoutingAlgo!= -1: # -1 to brak algorytmu tylko SP
            for i in range(1,self.NS+1):
                mac=hid2mac(i) # bedzie dzialac do 254 hostow @TESTB - zmiana czytamy z mapy 
                if i==dpid:  # adres lokalny ustawiany wczesniej
                    continue
                inter_port=nearestNode[i][1] # port posredni do odleglego hosta
                #@INIT_FLOW Tu nalezy ustawic RnnPathSesignato.portMapPrev[start,i]=inter_port
                match = parser.OFPMatch(eth_dst=mac,ip_proto=17, udp_dst=conf.COPORT, eth_type=0x0800)  # pakiet COG - port 5007
                action = [parser.OFPActionOutput(inter_port)]  # Swich--->AS
                self.Algo.oldSettingsDim[dpid][i][0]=inter_port #Dijkstra bez wag dubler dla algorytmu Rnn
                #self.logger.info("TOPO_HOSTadd (add_flow) zdalny  mac=%s -> out_port %d", mac, inter_port)
                self.add_flow(datapath, conf.PRIOCOG, match, action) # ten flow wysyla pakiet ethernetowy ze switcha do sąsziednieg (zaprzyjaźnionego) AS -a 
                match = parser.OFPMatch(eth_dst=mac,ip_proto=17, udp_dst=conf.USPORT, eth_type=0x0800)  # pakiet USER - port 5008
                action = [parser.OFPActionOutput(inter_port)]  # Swich--->AS
                self.add_flow(datapath, conf.PRIOUS, match, action)   
        else:
            print ("******************************")
            print("ALERT:    Routing alg. supress: only SP flows are settings ")
            print ("******************************")
        #*************************************************************************************************
        #*************************************************************************************************
        #self.logger.info("%6d TOPO CHANGE - HOST ADD mac %s IPv4 %s port %s !!!", self.logcnt, host.mac, host.ipv4, str(host.port)); self.logcnt+=1
        self.list_hosts.append((host.mac, host.port.dpid, host.port.port_no))
        
        # INFO ZWROTNE DO CTRL !!!!!   port 5006
        match = parser.OFPMatch(ip_proto=17, udp_dst=5006, eth_type=0x0800) # IFORMACJA ZWROTNA do kontrolera od ASa :  dane o obciążeniu sieci, UDP (prot=17) ipv4 (etype=0x0800)
        action = [parser.OFPActionOutput(datapath.ofproto.OFPP_CONTROLLER)]
        #************************************************************************
        #self.logger.info("%6d sw%d:TOPO ACTION for HOST %s -> out_port %s", self.logcnt, dpid, host.mac, host.port.port_no); self.logcnt+=1
        self.add_flow(datapath, 60000, match, action) # priorytet 60000  TEN FLOW zwraca sie do kontrolera i rozpoczyna cala akcje USTAWIANIA FLOWOW systemu IF-CS
        #eth_dst="00:00:00:00:00:%x",13   # bedzie dzialac do 254 hostow  
        #NIE DZIALA
        self.net.add_node(host.mac)
        self.net.add_edge(host.mac, host.port.dpid)
        self.net.add_edge(host.port.dpid, host.mac, port=host.port.port_no)
        self.mac_to_port[host.port.dpid][host.mac] = host.port.port_no
        
        

    # główna funkcja - obsługa PacketIn
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        #print('gggggggggggggg   ',self.Algo.oldSettingsDim[1][3][0])
        #quit()
        if self.first:
            #print  ("pierwszy")
            self.first=False
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.info("packet truncated: only %s of %s bytes", ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        data=str(msg.data)
        
        #tutaj przyszedl pakiet z informacja o delayach: 
        dpid=datapath.id
        #print('packet in')
        #print('dpid=',dpid)
        #print('datapath=',datapath)
        
        pkt = packet.Packet(msg.data) # wycigniecie pakietu ip z pakietu openflow
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        print('eth=',eth,'dpid= ',dpid)
        if eth.ethertype == ether_types.ETH_TYPE_IP:
            proto_ipv4 = pkt.get_protocols(ipv4.ipv4)[0]
            print('ipv4',proto_ipv4)
        #print('dpath=',datapath)
        if data.find("$DELAY$")!=-1:  
             print('packet in 2')
             info=data.split("$DELAY$")[1].split(",") # rozdzielamy po $DELAY$ - obciecie naglowka, nastepnie po przecinku
             #^   [src,dst,time [ns], delay[ns] ] - time od STARTu ASow
             self.log.flush() #zapisuj natychmiast do loga
             src=int(info[0]);dst=int(info[1]);tim=float(info[2]);delay=float(info[3]) # odczytujemy dane ze splitowanego info
             #print('src=',src,'  dst=',dst,' time=',tim,' delay=',delay)
             if conf.TestMode==True : # rowne opoznienia dla testu
                delay=1.0
                if dpid==6 or dpid==7:  # obcizamy sztucznie 6 i 7 wezel
                    delay=2.5
             state=False # algorytm DA (default)
             if self.Algo!=None: #alg.  Dw,Rnn
                print('packet in 4')
                state=self.Algo.insertData(src,dst,tim,delay) # wstawiamy dane do algorytmu albo algorytm jest wywolany           
             if state : # algorytm Dw albo Rnn wywolany, MODYFIKUJEMY flowy dla pakietow USER : 
                print('packet in 3')
                name=str(self.Algo.getAlgoName())
                self.log.write("*Time=*%f Controller:  /Calling Process/ %s\n "  % (time.time()-self.startTime, name)  ) 
                print('    ******  try to mod flow: ',self.Algo.getAlgoName())
                for dp in self.dpaths:   
                    self.Algo.modFlows(dp,conf.PRIOUS,self.startTime,self.log,dport=conf.USPORT) # ustawia flowy dla aktualnego dpid: wszystkie pozostale NS -1 wezlow 
                return # Atencjone : sprawdzic czy dziala
                
        # Kod poniżej to osluga nietypowych pakietow lepiej NIE RUSZAC!!!!
        # zastosowany alg. Spaning Tree
        ofproto = datapath.ofproto 
        parser = datapath.ofproto_parser
        port_in = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        # rozpoznaj z czym mamy do czynienia
        # tu można dodać nowe protokoły, ale nie ruszać struktury
        proto_arp = None
        proto_ipv4 = None
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        elif eth.ethertype == ether_types.ETH_TYPE_IP:
            proto_ipv4 = pkt.get_protocols(ipv4.ipv4)[0]
            #self.logger.info("%6d sw%s:Eth/IP4 %s/%s", self.logcnt, dpid, eth, proto_ipv4); self.logcnt+=1
            # tu można rozpoznać protokół, port doeclowy itp i ustawić odpowiednie flagi (np. COP)

        elif eth.ethertype == ether_types.ETH_TYPE_ARP: #flowy wg. drzewa rozpinającego
            # arp obsługuje funkcja set_bcast_rules()
            proto_arp = pkt.get_protocols(arp.arp)
            #self.logger.info("%6d sw%s:Eth/ARP %s/%s", self.logcnt, dpid, eth, proto_arp); self.logcnt+=1
            if dst == "ff:ff:ff:ff:ff:ff": 
                self.set_bcast_rules(datapath, parser, msg)
                return # NIE OBSLUGUJEMY !!!!!!!!!!!!!
       #ETH_TYPE_IPV6:   DROP  
        elif eth.ethertype == ether_types.ETH_TYPE_IPV6: # flowy DROP 
            proto_ipv6 = pkt.get_protocols(ipv6.ipv6)
            port_in = msg.match['in_port']
            match = parser.OFPMatch(eth_dst=dst) # lepiej podac adres docelowy dst 
            actions = [] #DROP action
            self.add_flow(datapath, 300, match,actions)  #bez actions drop ?  , actions)
            return
            
        else:
            # nic takiego jeszcze się nie pojawiło, ale skaut jest gotowy
            proto_ipv4 = None # dummy operation
            #self.logger.info("%6d sw%s:Eth/OTHER %s TYPE %x", self.logcnt, dpid, eth, eth.ethertype); self.logcnt+=1

        # w każdy protokół jest w ramce ethernet - pobierz src i dst

        dst = eth.dst
        src = eth.src
       
        # Jeżeli mamy nowy adres src (nie istniejący wcześniej) może się zdarzyć, 
        # że zdarzenie EventNewHost pojawi się później niż pakiet - dlatego podstawową obsługę robimy tutaj
        # (w obsłudze EventNewHost niektóre rzeczy się powtarzają, bo jeżeli pojawi się zdarzenie to nie chcemy już wchodzić tutaj.)
        """
        if src not in self.net: # Learn it and link it

            self.list_hosts.append(src)
            #self.logger.info("%6d sw%d:ADD HOST %s lnk dpid:%d portno:%d", self.logcnt, dpid, src, dpid, port_in)

            match = parser.OFPMatch(eth_dst=src)
            action = [parser.OFPActionOutput(port_in)]
            #self.logger.info("%6d sw%d:ADD ACTION for HOST %s -> out_port %s", self.logcnt, dpid, src, port_in); self.logcnt+=1
            self.add_flow(datapath, 44444, match, action)

            #self.logger.debug("%6d sw%d:ADDING node %s", self.logcnt, dpid, str(src)); self.logcnt+=1
            self.net.add_node(src) # Add a node to the graph
            ##self.logger.debug ("sw%d:ADDING link %s <-> %d", dpid, str(src), dpid)
            self.net.add_edge(src,dpid) # Add a link from the node to it's edge switch
            self.net.add_edge(dpid,src,port=port_in)
            print('src=',src)
            print('dpid=',dpid)
            print('port_in=',port_in)
            self.mac_to_port[dpid][src] = port_in
            #self.logger.info ("%6d sw%d:ADDED node %s, sw %d port %d", self.logcnt, dpid, str(src), dpid, port_in); self.logcnt+=1

        """
        # przygotowujemy obsługę routingu
        # ten fragment modyfikujemy, inne tylko w ważnych przypadkach!!!

        match_proto = None
        match_udp_port = None
        action_out_port = None
        match = None

       
    @set_ev_cls(event.EventSwitchEnter)
    def topo_switchenter(self, ev):
        datapath = ev.switch.dp
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        #self.logger.info("%6d TOPO CHANGE - SWITCH %d ENTER!!!", self.logcnt, datapath.id); self.logcnt+=1
        #print('*CALL*:  topo_switchenter()')
        raw_switches = get_all_switch(self)
        self.list_switches = [switch.dp.id for switch in raw_switches]

        prev_sw = self.topo_no_sw
        self.topo_no_sw = len(raw_switches)
        if prev_sw != self.topo_no_sw:
            self.net.add_nodes_from(self.list_switches)


    # nowy link w sieci
    @set_ev_cls(event.EventLinkAdd)
    def topo_linkadd(self, ev):
        #print('*CALL*: topo_linkadd()')
        link = ev.link
        #self.logger.info("%6d TOPO CHANGE - LINK ADD from %d to %d  !!!", self.logcnt, link.src.dpid, link.dst.dpid); self.logcnt+=1
        self.mac_to_port.setdefault(link.src.dpid, {})
        self.mac_to_port[link.src.dpid][link.dst.dpid] = link.src.port_no
        self.list_links.append((link.src.dpid,link.dst.dpid,{'port':link.src.port_no}))
        self.net.add_edge(link.src.dpid, link.dst.dpid, port=link.src.port_no)
        
