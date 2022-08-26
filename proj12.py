# Add hosts and switches
from mininet.topolib import Topo

#from mininet.net.Mininet import pingAll
class Project( Topo ):
    def __init__( self ):
        Topo.__init__( self )
      # Add hosts and switches

        Sw1 = self.addSwitch( 's1' )
        Sw2 = self.addSwitch( 's2' )
        Sw3 = self.addSwitch( 's3' )
        Sw4 = self.addSwitch( 's4' )
        Sw5 = self.addSwitch( 's5' )
        Sw6 = self.addSwitch( 's6' )
        Sw7 = self.addSwitch( 's7' )
        Sw8 = self.addSwitch( 's8' )
        Sw9 = self.addSwitch( 's9' )
        Sw10 = self.addSwitch( 's10' )
        Sw11 = self.addSwitch( 's11' )
        Sw12 = self.addSwitch( 's12' )
        As1 = self.addHost( 'h1' )
        As2 = self.addHost( 'h2' )
        As3 = self.addHost( 'h3' )
        As4 = self.addHost( 'h4' )
        As5 = self.addHost( 'h5' )
        As6 = self.addHost( 'h6' )
        As7 = self.addHost( 'h7' )
        As8 = self.addHost( 'h8' )
        As9 = self.addHost( 'h9' )
        As10 = self.addHost( 'h10' )
        As11 = self.addHost( 'h11' )
        As12 = self.addHost( 'h12' )

      # Add As <-------> Sw  links

        self.addLink( Sw1,As1,1,1 ) #10.0.0.1
        self.addLink( Sw2,As2,1,1 )
        self.addLink( Sw3,As3,1,1 )
        self.addLink( Sw4,As4,1,1 )
        self.addLink( Sw5,As5,1,1 )
        self.addLink( Sw6,As6,1,1 )
        self.addLink( Sw7,As7,1,1 )
        self.addLink( Sw8,As8,1,1 )
        self.addLink( Sw9,As9,1,1 )
        self.addLink( Sw10,As10,1,1 )
        self.addLink( Sw11,As11,1,1 )
        self.addLink( Sw12,As12,1,1 ) #10.0.0.12
        # pingujemy 

      # Add links
#
#links = get_link(self, dpid)
#for i in  range(0,len(links)):
#        for ln in links:    
#            print("SRC: ",ln.src.dpid, " port:", ln.src.port_no, "DST: ", ln.dst.dpid, " port:", ln.dst.port_no)
#    Link: Port<dpid=6, port_no=5(wyjscie) , LIVE> to Port<dpid=10, port_no=2, LIVE>
#         self.addLink( Sw6,Sw7,4,3 ):
#    Link: Port<dpid=6, port_no=4, LIVE> to Port<dpid=7, port_no=3, LIVE>

#     Link: Port<dpid=6, port_no=3, LIVE> to Port<dpid=5, port_no=3, LIVE>
#    Link: Port<dpid=6, port_no=2, LIVE> to Port<dpid=2, port_no=4, LIVE>

        self.addLink( Sw1,Sw2,2,2 )
        self.addLink( Sw1,Sw5,3,2 )
        self.addLink( Sw2,Sw3,3,2 )
        self.addLink( Sw2,Sw6,4,2 )
        self.addLink( Sw3,Sw4,3,2 )
        self.addLink( Sw3,Sw7,4,2 )
        self.addLink( Sw4,Sw8,3,2 )
        self.addLink( Sw5,Sw6,3,3 )
        self.addLink( Sw5,Sw9,4,2 )
        self.addLink( Sw6,Sw7,4,3 )
        self.addLink( Sw6,Sw10,5,2 )
        self.addLink( Sw7,Sw8,4,3 )
        self.addLink( Sw7,Sw11,5,2 )
        self.addLink( Sw8,Sw12,4,2 )
        self.addLink( Sw9,Sw10,3,3 )
        self.addLink( Sw10,Sw11,4,3 )
        self.addLink( Sw11,Sw12,4,3 )
        return
topos = { 'project': ( lambda: Project() )}

#########################
#(src,dest,waga,port) struktura do algorytmu Dijkstra; na koncu musi byc (ns,0,0,0) ns==id ostatniego swicza (zwykle)
#[(1, 2, 1, 2), (2, 1, 1, 2), (1, 5, 1, 3), (5, 1, 1, 2), (2, 3, 1, 3), (3, 2, 1, 2), (2, 6, 1, 4), (6, 2, 1, 2), (3, 4, 1, 3), (4, 3, 1, 2), (3, 7, 1, 4), (7, 3, 1, 2), (4, 8, 1, 3), (8, 4, 1, 2), (5, 6, 1, 3), (6, 5, 1, 3), (5, 9, 1, 4), (9, 5, 1, 2), (6, 7, 1, 4), (7, 6, 1, 3), (6, 10, 1, 5), (10, 6, 1, 2), (7, 8, 1, 4), (8, 7, 1, 3), (7, 11, 1, 5), (11, 7, 1, 2), (8, 12, 1, 4), (12, 8, 1, 2), (9, 10, 1, 3), (10, 9, 1, 3), (10, 11, 1, 4), (11, 10, 1, 3), (11, 12, 1, 4), (12, 11, 1, 3), (12, 0, 0, 0)]
