""" Collector of Loads in Network; Alghorithms of  routing interface; Flows Setter :
# dziedzicza z niego : DwAlgo i RnnAlgo 
# pyflakes program.py- sprawdza skladnie""" 
# Copyright (C) 2022 IITIS PAN ZMiOESK
# Copyright (C) 2022 Piotr Pecka 
# IF-CS V 1.0 Inteligent Flow Controlling  System  Copyright (C) 2022
""""""""""""""""""""""""""""""""""""
############
#  sudo ovs-ofctl  dump-flows s1  SPRAWDZA FLOWE 

# IF-CS V 1.0 Inteligent Flow Controlling  System for SDN networks  Copyright (C) 2022
#Github robic:  gip  push  *
# na nstronie gi laba mamy w historii

# Piotr Pecka 
import conf
#CAP=100 # pojemnosc zgloszen pakietow kognitywnych - po przekroczeniu - wywolania alg. Routingu
import time,sys
import random
import signal # timeout dla algorytmow ustawiania flowow
from util import hid2mac # f. zamienia dpid na macc adres
from topo_dijkstra import nearestNodeDijkstra 
from topo_dijkstra import createLinksDijkstra 
import pickle
#from ryu.base import app_manager # ustawianie flow-ow
# ATENCJONE pamietaj o blokowanych portach: bash$:  netstat -tuple
# zrobic pkill java
# pyflake plik.py - sprawdz skladnie ********
from abc import ABC, abstractmethod  # pythonowa klasa ABC (Abstract Base Class)
#IP_ADDR="10.0.0."
COM=","
EOL="\n"
#TOPO="connections12mesh.pickle" # plik binarny z topolagia sieci dla alg routingu : plik topo_dijkstra.py
#V musi by: CO (klasa)  i SKAD (nazwa pliku)

""" Klasa bazowa dla wszystkich algorytmow routingu"
"""
import random #do testow
#import conf  # plik konfiguracyjny'
class RoutingAlgoInterface(ABC):  # ATENCJONE: nie potrzebne wystarczylo zwykle dziedziczenie- obiekt statyczny 
    def __init__(self,CAP,Tout,NS,f3d): # maksymalny rozmiar (CAPacity) kolekcji po ktorej wywolywany jest wybrany algorytm 
        self.f3d=f3d
        self.CAP=CAP
        self.Tout=Tout # alarm po Tout sekundach
        self.NS=NS
        self.MACS=conf.MACS # dla TestBed zamiast hid2mac
        self.size=0 # aktualny rozmiar kolekcji
        self.TimeOut=False # ustawiany przez sygnal ALARM (Linux/Unix)
        signal.signal(signal.SIGALRM, self.alarm)
        signal.alarm(Tout) # czas alarmu
        # tablice wypelnione -1 ; na poczatku musi byc DA w oldSettingsDim MiniNet
        # Tablice numerow portow !!! port[dpid,src,dst] dla Rnn port[dpid,dst] @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
        # To niema nic wspolnego z wagami !!!!!!!!!!!!!!!!!!!!! wykrywa sie gdzie zmienil sie port:
        # range(NS+1) od 0 do NS+1 =  range(0,NS+1)
        self.oldSettingsDim = [[[-1 for k in range(NS+1)] for j in range(NS+1)] for i in range(NS+1)] # 3 wymiarowa tablica dynamiczna dla Rnn dla DW wyorzystujemy 2 wymiary
        self.newSettingsDim = [[[-1 for k in range(NS+1)] for j in range(NS+1)] for i in range(NS+1)] # jezeli port(src,dpid) -zalezy odL
        #  ???? Test Bed wypelnimy 1-ynkami
        #self.oldSettingsDim = [[[1 for k in range(NS+1)] for j in range(NS+1)] for i in range(NS+1)] # 3 wymiarowa tablica dynamiczna dla Rnn dla DW wyorzystujemy 2 wymiary
        #self.newSettingsDim = [[[1 for k in range(NS+1)] for j in range(NS+1)] for i in range(NS+1)] # jezeli port(src,dpid) -zalezy odL
       
        #^^^  dla DW ustawimay 1 - wszystkie wagi takie same
    def alarm(self,num,fr): # zastapic sygnalem na threadzie bo dziala tylko z rozdzielczoscia sekunda
        self.TimeOut=True  # alarm wylaczony
        print(" *********** ALERT  ***********")
        signal.alarm(self.Tout)
 
    @abstractmethod # insertData - jest abstrakcyjna - naglowek taki sam dla wszystkich algorytmow
    def insertData(self,src=0,dst=0,tim=0,delay=0): pass # f. wirtualna - dane wejsciowe dla dowolnego algo: Rnn, DW
    @abstractmethod
    def getAlgoName(self): pass
    def enable(self): # wywolywne prze f. run() - klasa podrzedna dolaczonego algorytmu; sprawdza czy mozna wywolac algo.
        if (self.TimeOut==True and self.size>0 ) or (self.size>=self.CAP) : #zezwolenie na uruchomienia algorytmu 1 raz dla wszystkich dpid!!!  - 
            self.TimeOut=False  #czekamy na nastepny timeout 
            #self.settingsState[dpid]==False # dla tego dpid ustawiono juz flow czekamy na nastepne zapelnienie sie bufora lub timeout
            #print("Flow Setting Enable:"," rozmiar kolekcji: ",self.size)
            self.size=0 # kolekcja danych pusta czekamy  na zapelnienie
            return True
        else:
            return False
  
    #V wypelniamy na podstawie NewSettings dla jednego datapath : wywoluje klas podrzedna 
    #V Kotroler wywoluje alg.modFlow()
    #V modyfikuje flowy dla pakietow USER 
    def modFlows(self,datapath, priority,tims,log,dport): # wywoluje switch o id datapath.id tims - to  czas startu kontrolera
        # Tu trzeba wywolac dla wszyskich dpid   !!!!
        # dla DW tylko dst sie liczy dla Rnn src ids !!!
        # czestosc wywolania odwrotnie proporcjonalna do conf.CAP i conf.FlowTimeOut
        #print ('old settings=',self.oldSettingsDim,'modFlows() callefrom simple_switch_13()')
        #print ('NEW settings=',self.newSettingsDim,'modFlows() callefrom simple_switch_13()')  
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid=datapath.id  # for datapath in self.dpaths: tablica datapaths w  konstr klasy SimpleSwitch13
        #V Tablica .settingsState jest ustawiona na True w klasie dziedziczacej obslugujacej konkretny algorytm f.  insertData()
        #if  self.settingsState[datapath.id]==False: return False #  niema nowych ustawien  co ustawiac
        #assert 0
        if self.f3d: # dla Rnn
            start=1;rang=self.NS+1
        else:
            start=0;rang=1 # dla Dijkstry - nie zalezy od historii przybycia do węzła
        for src_ in range(start,rang):
            for dst_ in range(start,self.NS+1): 
                newPort=self.newSettingsDim[dpid][dst_][src_] #@@ATENCJONE !!! Tu byl BLAD w porow z org (mial byc newSttingsDim zamiast OldSettingsDim!!!
                #print('newPort=',newPort)
                if newPort!=self.oldSettingsDim[dpid][dst_][src_]: #and newPort!=-1 :
                    if newPort== -1: # dajemy dijkstre bez wag
                        assert 0
                    #print('gggg=',self.oldSettingsDim[dpid][dst_][0])
                    #p=random.random()
                    #p=2
                    #if p<0.9:
                    #print(' ***Fix Rnn *****')
                    #newPort=self.oldSettingsDim[dpid][dst_][0] # losowo naprawiamy blad Rnn wpisujac port z alg. DA (dane w wymiarze 0 )
                    self.oldSettingsDim[dpid][dst_][src_]=newPort
                    self.newSettingsDim[dpid][dst_][src_]=newPort
                    print("ustawiam/mod flow: ",dpid,"  ---> ",dst_, "zmieniam port z  " ,self.oldSettingsDim[dpid][dst_][src_], "na: ",newPort ,'    src=' ,   src_)
                    sys.stdout.flush()
                    if newPort==-1:
                        print('zly port')
                        return
                    if dst_==dpid: continue #pakiet jest juz na miejscu - wyslanie na port 1 czyli do hosta 
                    actions = [parser.OFPActionOutput(newPort)]
                    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
                    mac_dst=self.MACS[dst_] # dla mininet:  hid2mac(dst_) # Atencjone: przy test band trzeba mapowac
                    mac_src=self.MACS[src_] # hid2mac(src_)
                    #hid2mac(3,4) nie dziala przeciazenie funkcjiw pythonie 
                    if self.f3d:
                        match = parser.OFPMatch(eth_src=mac_src,eth_dst=mac_dst,ip_proto=17, udp_dst=dport, eth_type=0x0800) #flowy (dpid,src,dst)
                    else:
                        match = parser.OFPMatch(eth_dst=mac_dst,ip_proto=17, udp_dst=dport, eth_type=0x0800)#flowy (dpid,dst)
                    mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst) #dajemy wiekszy priorytet
                    datapath.send_msg(mod) # Tujest blad - port = -1
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                    #self.oldSettingsDim[dpid][y][z]=newPort #  aktualizacja tablicy flow
        #self.settingsState[dpid]=False # na True  bedzie zmieniac alg routingu jak znajdzie zmiane
      
        
        return True # ustawiono flowy      
       

"""
    Algorytm Rnn
"""
from  rnnLib import RnnPathDesignator # parsuje info o portach (json) 
from  rnnLib import PayloadInfoSender # komunikuje sie z Rnn (wysyla info o obciazeniach i odbiera dane o portach (json))


    
class RnnAlgo(RoutingAlgoInterface):
    #V Max dlugosc kolekcji CAP; time out Tout[s],NC- liczba switchy,alg Rnn nasluchuje na port= i host= 
    def __init__(self,CAP=10,Tout=1,NS=12,host="127.0.0.1",port=9999):
        super().__init__(CAP,Tout,NS,f3d=True) # wywolanie konstuktora w klasie nadrzednej #f3d=False  ustawia sie NSx(NS-1) flowow (dpid,src, dst) dla kazdego switcha
        self.pis=PayloadInfoSender(host,port) # wysyla do modulu Rnn dane (osobny proces Java)
        self.PACKET="" #""" json format: {  "payload": .......,  }"""
        self.PAYLOADS="" # tu gromadzimy payloady
        #^ dane gromadzimy w info (+) do momentu zapelnienienia kolekcji: (CAPAC, lub odebrania sygnalu TomeOut
    def getAlgoName(self): return "Rnn Algo (Java Sover)"
    def getPort(self,x,y): return 
    def insertData(self,src=0,dst=0,tim=0,delay=0): # od ASow otrzymuje 
        #msg="$DELAY$ "+src+COM+str(dpid)+COM+str(DT)+COM+str(delay) # nowy msg: $DELAY$ src, dst, DT, delay
        """ Function doc """
        self.PAYLOAD = "\"%d , %f ,%d|%d , %f | %d , %f |\"" % (src,tim,dst,src,tim,dst,delay)
        #print ("enable=False")
        if not self.enable(): # jeszcze nie wysylamy do Rnn - gromadzimy payload-y dodajac przecinek COM na koniec  V
            self.PAYLOADS+="{\"payload\": "+self.PAYLOAD +", \"srcHost\": %d ,\"dstHost\": %d,\"time\": %f }" % (src,dst,tim) +COM
            self.size+=1 # aktualny rozmiar kolekcji zwiekszmy o jeden - def w klasie bazowej
            return False # kompletujemy dane bez wywolania algorymu
        else:  #wywolujemy algorytm Rnn # ATENCJONE: ostatni PAYLOAD bez przecnika: 
            #print ("*wywolujemy alg Rnn")
            self.PAYLOADS+="{\"payload\": "+self.PAYLOAD +", \"srcHost\": %d ,\"dstHost\": %d,\"time\": %f }" % (src,dst,tim) 
            self.PACKETS="\"packets\":[ " +  self.PAYLOADS +']' # dodajemy naglowki
            self.INFO="{\"information\":{" +self.PACKETS + "}}" # dodajemy naglowki - gotowy do wyslania 
            self.PAYLOADS="" # czyscimy kolekcje dla nastepnej serii
            paths=self.pis.send2Rnn(self.INFO) #"""  json:  {  "paths":[ { "nodes":[{ "output port": 2, "device id":1}  .................. """
            #sys.stderr.write(self.INFO)
            #sys.stderr.write('----------------------------')
            #sys.stderr.write(paths)
            #V dekodujemy porty na podstawie stringu paths
            ports=RnnPathDesignator(paths) # parsujemy , w ports baza portow
            for src_ in range(1,self.NS+1):
                for dpid_ in range(1,self.NS+1): # po wszystkich hostach x i  polaczeniach y do innych
                    for dst_ in range(1,self.NS+1):
                        #getPort(self,dpid,src,dst):
                        #if x==y: continue # polaczenie docelowe - port ustawiony na 1 
                        port=ports.getPort(dpid_,src_,dst_) # jestem w x - polacenie do y  ; z  -bierzacy odwiedzany wezel
                        #if port!= -1: continue
                        #getPort(x,z,y):  z(src) 1..NS
                        if port!=self.oldSettingsDim[dpid_][dst_][src_]: # sygnalizujemy  roznice w portach dla datapath.id= x
                            #self.settingsState[x]=True
                            #V przy ustwaianiu flow, jeszcze raz bedziemy sprawdzac ta roznice aby ustawic flow dla danego datapath.id
                            #V poniewaz ustawianie wymuszane jest przez regule CONTROLL z kontrolera.
                            if port!= -1: #Atencjone moga byc nie wszystkie ustawione 
                                self.newSettingsDim[dpid_][dst_][src_]=port #wpisujemy nowo ustawiony  port
            return True # algorytm wywolany TimeOtu albo przekroczone CAP 
"""
    Algorytm DW
"""
#class RnnAlgo(RoutingAlgoInterface):
#    #V Max dlugosc kolekcji CAP; time out Tout[s],NC- liczba switchy,alg Rnn nasluchuje na port= i host= 
#    def __init__(self,CAP=10,Tout=1,NS=12,host="127.0.0.1",port=9999):
class DWAlgo(RoutingAlgoInterface):
    def __init__(self,CAP,Tout=1,NS=12,topo=conf.TOPO):
        super().__init__(conf.CAP,Tout,NS,f3d=False)  #f3d=False  ustawia sie NS flowow (dpid,dst) dla kazdego switcha
        #TOPO="connections12mesh.pickle" # plik binarny z topolagia sieci dla alg routingu
        #nearestNode,NS=nearestNodeDijkstra(dpid,self.NS,edges[..]) - znajduje najblizszy wezel,wywolujemy RAZ 
        #inter_port=nearestNode[x][1] # port posredni do odleglego hosta x
        #edges=[(1, 2, 1, 1), (2, 1, 1, 1), (2, 3, 1, 2), (3, 2, 1, 1),  (3 , 1, 1,2), (1, 3, 1, 2),(3, 0, 0, 0)] - siec 3 wezlow 
        self.edges=[]
        self.edgesCopy=[]
        self.sizeOfEdges=0
        self.ALFA=conf.ALFA #(1-alfa)old+alfa(old)  wspolczynnik sredniej wazonej MUSI byc w przedziale  (0,1)
        try:  
            with open(topo, 'rb') as handle:   #  topo:  plik z topologia typ  pickle 
                #self.edgesCopy=self.edges = pickle.load(handle) # Atencjone: Copy pokazuje na to samo miejsce w pamieci 
                #defaultowe ustawienie grafu na podstawie topologii, modyfikujemy  edges[i][2]
                self.edges= pickle.load(handle)
                self.sizeOfEdges=len(self.edges)
                handle.close()
            with open(topo, 'rb') as handle:
                self.edgesCopy= pickle.load(handle)
                handle.close()
        except:
            assert False 
        #print("type=",type(self.edges).__name__)
    def getAlgoName(self): return "Dijkstra with waigth DW"
    def getEdges(self):  return self.edges # dla zewnetrnej funkcji nearestNodeDijkstra
   
    
    def setWeight(self,i,j,w): # ustawiamy wage na krawedzi i -----> j TYLKO dla DW - Rnn potrzebuje src i dst
        for k in range(0,len(self.edges)-2): # len() -liczba polaczen 
            if  i==j:continue # polaczenie do samego siebie pomijamy
            if self.edges[k][0]==i and self.edges[k][1]==j: #ATTENCJONE :  wyszukiwanie liniowe !!! REFERENCJA i Clonowanie latwo w pytonie pomylic
                x=self.edges[k]
                y = list(x)
                y[2] = w*(1-self.ALFA)+y[2]*self.ALFA #self.edges[k][2]=w #modyfikujemy wezel - w ten sposob nie dziala!
                x = tuple(y) # 
                self.edges[k]=x
                size2=len(self.edges)
        #if(len(self.edges)!=len(self.edgesCopy)): #ATTENCJONE :  wyszukiwanie liniowe !!! REFERENCJA i Clonowanie latwo w pytonie pomylic
         
   
        
                
    def insertData(self,src=0,dst=0,tim=None,delay=0): # f. wirtualna 
        if not self.enable(): # jeszcze nie wywolujemy alg. DW do Rnn - gromadzimy payload-y dodajac przecinek COM na koniec  V
            self.setWeight(src,dst,delay) # ustawiamy wage
            #print("notdw ")
            self.size+=1 # zwiekszamy liczbe zgloszen delayow
            return False # kompletujemy dane bez wywolania algorymu
        else: # wywolujemy alg. DW
            #print ("dw is calling")
            try: 
                for x in range(1,self.NS+1): # po wszystkich hostach x i  polaczeniach y do innych
                    nearestNode,NS=nearestNodeDijkstra(x,self.NS,self.edges) # tu JEST  WINNY zmniejszaniu sie edges
                    for y in range(1,self.NS+1):
                        if x==y: continue
                        port=nearestNode[y][1] # jestem w x - polaczenie do y # jestem w x - polacenie do y 
                        if port!=self.oldSettingsDim[x][y][0]: # sygnalizujemy  roznice w portach dla datapath.id= x
                            #self.settingsState[x]=True
                            #V przy ustwaianiu flow, jeszcze raz bedziemy sprawdzac ta roznice aby ustawic flow dla danego datapath.id
                            #V poniewaz ustawianie wymuszane jest przez regule CONTROLL z kontrolera.
                            self.newSettingsDim[x][y][0]=port #wpisujemy nowo ustawiony  port , z=0 dla Dijkstry nie zalezy od staru (historii)
                                                             #tylko biezaca pozycja x  sie liczy i dest. y
                            #print('zmienil sie port',self.oldSettingsDim[x][y],'------->',port)
                return True
            except KeyError as e:
                #return False
                print( 'KeyError - reason "%s   ' % str(e))
                print('len=',len(self.edges))
                print('lenCopy=',len(self.edgesCopy))
                print('x=',x)
                print('y=',y)
                return True # algorytm wywolany TimeOtu albo przekroczone CAP 
        
"""
    Algorytm DW default - klasa nic nie robi wyykorzystuje ustawienia kontrolera
"""               
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
