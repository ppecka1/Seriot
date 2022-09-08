# Copyright (C) 2021 IITIS PAN
# Copyright (C) 2021  Piotr Pecka 
# Piotr Pecka:  piotr@iitis.pl ZmioesK
# kontroler dla Test Bed
# Atencjone odpalamy kontroler:
#seriot@seriot:~/ryu$  PYHTONPATH=. ryu-manager  --observe-links ryu/app/gui_topology/gui_topology.py ryu/app/simple_switch_13.py
# wczesniej czystka: kip ,def (aliasy w seriot@seriot:~/ryu/ryu/app kasuje demony i usuwa flowy)
# odpalenie pakietw cog: asm (alias sh AsM.sh dpid)
# wyswietlenie flowow (alias dum;  dumpfall.sh )
# odpalenie odbiornikow (demonow) pakietow USER:   Userv.sh
# wyslanie pakietu (strumienia  pakietow - zmiana kodu w users.py) do odbiornikow (demonow) pakietow USER: users.py  
import conf

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
#dodane:
import time
import os
from ryu.topology import event
from topo_dijkstra import nearestNodeDijkstra 
from topo_dijkstra import createLinksDijkstra

from  RoutingAlgoInterface import RnnAlgo
from  RoutingAlgoInterface import DWAlgo
# wazne komendy:
#sudo tshark -i br0
#arp
#ip a
#ssh seriot1 sudo ovs-ofctl dump-flows br0 
# geany plugin manager : addons - podswietla wszystkie wystapienia 
#
class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        logFileName="./Logs/logController.txt"
        if os.path.exists(logFileName):
            os.remove(logFileName)
        self.log = open(logFileName,"w")
        self.mac_to_port = {}
        self.nodes_dpids={}
        self.NS=6 # 6 wezlow
        #self.topo6=conf.TOPO6 # dla test bed 
        self.edges=conf.edges6
        #polecenie maci.sh: hosty TestBeda
        self.MACS=conf.MACS
        #sid= dpid-1 if dpid==7 else dpid # Uwaga switch 6 ma numer 7 
        #self.ustaw_flow=True
        if conf.RoutingAlgo==1:
            self.Algo=DWAlgo(conf.CAP,conf.FlowTimeOut,conf.NS)
        elif  conf.RoutingAlgo==2:
            #(self,CAP,Tout=1,NS=12,topo=conf.TOPO)
            self.Algo=RnnAlgo(CAP=conf.CAP,Tout=conf.FlowTimeOut,NS=self.NS,edges=self.edges) # inicjalizacja aalgorytmu 
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
        self.startTime=time.time()

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase 
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        data=str(msg.data)
        datapath = msg.datapath    
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port'] # skad przyszedl nie uzywane
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src 
        dpid=datapath.id
        # $DELAY przychodzi za As-a 
        if data.find("$DELAY$")!=-1:
            info=data.split("$DELAY$")[1].split(",")
            src=int(info[0]);dst=int(info[1]);tim=float(info[2]);delay=float(info[3])
            #print('(src dst) ',src,dst,' time=',tim,' delay=',delay)
            if conf.TestMode==True : # rowne opoznienia dla testu
                delay=1.0
                if dpid==3:  # obcizamy sztucznie 3 wezel
                    delay=2.5
            state=False # algorytm DA (default)
            if self.Algo!=None: #alg.  Dw,Rnn
                #print('packet in 4')
                state=self.Algo.insertData(src,dst,tim,delay) # wstawiamy dane do algorytmu albo algorytm jest wywolany           
            if state : # algorytm Dw albo Rnn wywolany, MODYFIKUJEMY flowy dla pakietow USER : 
                #print('packet in 3')
                name=str(self.Algo.getAlgoName())
                #self.log.write("*Time=*%f Controller:  /Calling Process/ %s\n "  % (time.time()-self.startTime, name)  ) 
                print('    ******  try to mod flow: ',self.Algo.getAlgoName())
                #for dp in self.dpaths:   # dla Mininet
                for dp in self.nodes_dpids: # dla TestBed Atencjone nodes_dpids[dp] to datapath ustawiamy na kazdym z nich NS-1 flowow (DW) albo (NS-1)^2 flowow
                    self.Algo.modFlows(self.nodes_dpids[dp],conf.PRIOUS,self.startTime,self.log,dport=conf.USPORT) # ustawia flowy dla aktualnego dpid: wszystkie pozostale NS -1 wezlow 
                return # Atencjone : sprawdzic czy dziala
        #print('packet in:  ',src,'    ',dst)
        if (dst == 'ff:ff:ff:ff:ff:ff'): #statycznie przydzielone arp-y /etc/ethers 
            #print('_packet_in_handler: dpid=',dpid,'  src=',src,'   dst=',dst)
            return # odrzucamy arpy
        #Atencjone flowy pocztkowe wymusic uzywajac skryptu pingall.sh
        if dpid not in self.nodes_dpids: # ATENCJONE: tu usawia sie flowy poczatkowe:  DA oraz info zwrotne do KONTROLERA
            # @ATENCJONE@ tu nalezy zaincjowac self.newSettingsDim[dpid][dst_][src_] dla ALGO DW !!!!!!!!!!!!!
            self.nodes_dpids[dpid]=datapath # nodes_dpids mamy skompletowane wszystkie DATAPATH 
            start=dpid
            #print('ustawiam flow dla',dpid,'  ',len( self.nodes_dpids))
            nearestNode,NS=nearestNodeDijkstra(start,self.NS,edges=self.edges) # ostatni parametr to lista czworek - topologia w formacie python
            if NS<0 or NS!=self.NS:
                assert(0)
            macSrc=self.MACS[dpid]
            for i in range(1,self.NS+1):
                macDst=self.MACS[i] # hid2mac()
                if i==dpid:  # adres lokalny ustawiany wczesniej
                    #if RoutingAlgo==1:  # ustawienie poczatjowych flowow TYLKO dla DwAlgo
                    #self.Algo.setWeiht() #setWeight(self,i,j,w): # ustawiamy wage na krawedzi i -----> j TYLKO dla DW - Rnn potrzebuje src i dst
                        
                    match = parser.OFPMatch(eth_dst=macDst) 
                    action = [parser.OFPActionOutput(ofproto.OFPP_LOCAL)]  # Swich--->AS LOCAL adres !!!
                    self.add_flow(datapath, 12345, match, action)
                    #self.add_flow(datapath, 6, match, action) 
                    continue
                inter_port=nearestNode[i][1]
                if conf.RoutingAlgo==1:  # INCICJACJa newSettingsDim[dpid][dst_][src_] dla DW !!!!!!!!!!!!!!!!!!!!!!!!!!
                    self.Algo.newSettingsDim[dpid][i][0]=inter_port # dst=1, src=0 nie uzywamy d DW !!!!
                    #self.Algo.oldSettingsDim[dpid][i][0]=inter_port
                print('iport=',inter_port)
                match = parser.OFPMatch(eth_dst=macDst) 
                action = [parser.OFPActionOutput(inter_port)]  # Swich--->AS
                self.add_flow(datapath, 12345, match, action) 
                ###### inormacje od AS - ow
                match = parser.OFPMatch(ip_proto=17, udp_dst=5006, eth_type=0x0800) # IFORMACJA ZWROTNA do kontrolera od ASa :  dane o obciążeniu sieci, UDP (prot=17) ipv4 (etype=0x0800)
                action = [parser.OFPActionOutput(datapath.ofproto.OFPP_CONTROLLER)]
                #************************************************************************
                #self.logger.info("%6d sw%d:TOPO ACTION for HOST %s -> out_port %s", self.logcnt, dpid, host.mac, host.port.port_no); self.logcnt+=1
                self.add_flow(datapath, 60000, match, action) 
        """
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        for i in range(1,self.NS+1):
            for j in range(1,self.NS+1):
                print(self.Algo.newSettingsDim[i][j][0], end =" |") 
            print
        """
               
        return 
        
        
       
