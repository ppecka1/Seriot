# Copyright (C) 2021 IITIS PAN
# Copyright (C) 2021 Mateusz Nowak
# & Piotr Pecka:  piotr@iitis.pl ZmioesK
# kontroler dla Test Bed
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
from ryu.topology import event
from topo_dijkstra import nearestNodeDijkstra 
from topo_dijkstra import createLinksDijkstra

# wazne komendy:
#sudo tshark -i br0
#arp
class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.nodes_dpids={}
        self.NS=6 # 6 wezlow
        self.topo6=conf.TOPO6 # dla test bed 
        #polecenie maci.sh: hosty TestBeda
        self.MACS=conf.MACS
        #sid= dpid-1 if dpid==7 else dpid # Uwaga switch 6 ma numer 7 
        self.ustaw_flow=True


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
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src 
        dpid=datapath.id
        if data.find("$DELAY$")!=-1:
            info=data.split("$DELAY$")[1].split(",")
            src=int(info[0]);dst=int(info[1]);tim=float(info[2]);delay=float(info[3])
            print('src=',src,'  dst=',dst,' time=',tim,' delay=',delay)
        #print('packet in:  ',src,'    ',dst)
        if (dst != 'ff:ff:ff:ff:ff:ff'): 
            #print('_packet_in_handler: dpid=',dpid,'  src=',src,'   dst=',dst)
            pass
            
        else:  # tu nie wchodzi nie trzeba DROPowac ARPy wylaczone
            #match = parser.OFPMatch(eth_dst=dst) # lepiej podac adres docelowy dst 
            #actions = [] #DROP action
            #self.add_flow(datapath, 300, match,actions)
            #print('ff:ff  in')
            return
            
        if dpid not in self.nodes_dpids: # tu usawia sie flowy poczatkowe DA info zwrotne do KONTROLERA
            self.nodes_dpids[dpid]=datapath
            start=dpid
            #print('ustawiam flow dla',dpid,'  ',len( self.nodes_dpids))
            nearestNode,NS=nearestNodeDijkstra(start,self.NS,self.topo6) # ostatni parametr to lista czworek 
            if NS<0 or NS!=self.NS:
                assert(0)
            macSrc=self.MACS[dpid]
            for i in range(1,self.NS+1):
                macDst=self.MACS[i] # hid2mac()
                if i==dpid:  # adres lokalny ustawiany wczesniej
                    match = parser.OFPMatch(eth_dst=macDst) 
                    action = [parser.OFPActionOutput(ofproto.OFPP_LOCAL)]  # Swich--->AS
                    self.add_flow(datapath, 12345, match, action)
                    #self.add_flow(datapath, 6, match, action) 
                    continue
                inter_port=nearestNode[i][1]
                #inter_port=4  # FALSZYWY port do testow
                #print('node ',macSrc,' to ',macDst,'port ',inter_port)
                #match = parser.OFPMatch(eth_dst=mac,ip_proto=17, udp_dst=conf.USPORT, eth_type=0x0800)  # pakiet USER - port 5008
                #match = parser.OFPMatch(eth_src=macSrc,eth_dst=macDst) 
                match = parser.OFPMatch(eth_dst=macDst) 
                action = [parser.OFPActionOutput(inter_port)]  # Swich--->AS
                self.add_flow(datapath, 12345, match, action) 
                ###### inormacje od AS - ow
                match = parser.OFPMatch(ip_proto=17, udp_dst=5006, eth_type=0x0800) # IFORMACJA ZWROTNA do kontrolera od ASa :  dane o obciążeniu sieci, UDP (prot=17) ipv4 (etype=0x0800)
                action = [parser.OFPActionOutput(datapath.ofproto.OFPP_CONTROLLER)]
                #************************************************************************
                #self.logger.info("%6d sw%d:TOPO ACTION for HOST %s -> out_port %s", self.logcnt, dpid, host.mac, host.port.port_no); self.logcnt+=1
                self.add_flow(datapath, 60000, match, action) 
                #dpid = format(datapath.id, "d").zfill(16) # wypelnia zerami 000000000000000id
                #self.mac_to_port.setdefault(dpid, {})
        """
        if (len( self.nodes_dpids)==self.NS) and (self.ustaw_flow):
            print('ustawiam flowy')
            start=dpid
            createLinksDijkstra(conf.TOPO) # w pliku o nazwie TOPO (binarny) info o topologi i wagach
            nearestNode,NS=nearestNodeDijkstra(start,self.NS,cp=conf.TOPO) 
            self.ustaw_flow=False # wszystkie podstawowe flowy zostaly ustawione: alg DA 
            
        """    
        #self.logger.info("packet in %s %s %s %s %s", dpid, src, dst, in_port, eth.ethertype)

        # learn a mac address to avoid FLOOD next time.
        
        return 
        
        
       
