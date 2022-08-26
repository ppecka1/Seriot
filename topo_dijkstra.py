import sys 
import os
import socket 
import pickle
import struct
import time
from collections import defaultdict
from heapq import *
#UDP_IP = "0.0.0.0"
#UDP_PORT = 5005
#MY_IP = sys.argv[1] # self address  10.0.0.x
#MY_ID = int(MY_IP.split('.')[3])  # MY_ID=x
#NEXT_NODE_IP =""      #adres najblizszego wezla DH
#NS=12 #number of nodes
#sock = socket.socket(socket.AF_INET, # Internet
#socket.SOCK_DGRAM) # UDP socket.SOCK_DGRAM
#sock.bind((UDP_IP, UDP_PORT))
#raport= open("a.log","w") #log file: 10.0.0.x.log
#ovs-ofctl add-flow s_i dl_type=0x0800,nw_proto=17,tp_dst=5005,actions=mod_nw_src:10.0.0.i,controller,max(pol)

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c,w in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return  ( cost,path) #return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next 
                    heappush(q, (next, v2, path))

    return  -1,[] 
###########################

def setFlowTable(nearestNode,NS=3): # NIE UZYWANE  !!!!
  cmd1=""
  cmd2=""
  for i in xrange(1,NS+1):
    cmd1="sudo ovs-ofctl add-flow "+"s"+str(MY_ID)+" dl_type=2048,nw_dst=10.0.0."+str(i)+",actions=output:"+str(nearestNode[i][1])
    #print cmd1
    cmd2="sudo ovs-ofctl add-flow "+"s"+str(MY_ID)+" dl_type=2054,nw_dst=10.0.0."+str(i)+",actions=output:"+str(nearestNode[i][1])
    os.system( cmd1);
    os.system( cmd2);
    pass
###########################

def nearestNodeDijkstra(MY_ID,   NS=3,     edges=[],  cp="connections.pickle"): # acording Dijkstra algorithm
# zwraca mape najjblizszego wezla i portu  od punktu MY_ID (start) do pozostalych NS wezlow
# eges: tablica (NIE MAPA !!!) z polaczeniami wagami i portami
# UWAGA:  WYSOCE Nie  optymalne za kazdym razem wczytuje topologie z sieci i znajduje wszystkie sciezki z punktu  MY_ID do dst
#  zraca nr.  Swicza i port wyjsciowy, port =1 to polaczenie do As
#element=(j+1,i+1,1,sw[j]) # 10.0.j+1 is conected to 10.0.0.i+1    ( 2 directions link ) , weight of node =1, ingress port
  nearestNode={-1:[-1,-1]} # target distant  node (key) : [ nearest indirect node , ingrees port] (val)/ struct: DICTONARY 
  #if MY_ID==dest: # sciezka do siebie
  #    return 1,-1 # port , kod informacyjny 
  #nearestNode,NS=nearestNodeDijkstra(x,   self.NS,   self.edges)  # TAK sie wywoluje po wczytaniu edges z pliku edges != []
  
  if edges!=[]: # podajem edges jako parametr NIE otwiera pliku pickle
    pass
  elif NS==3: # siec testowa:  s1->s2->s3->s1
    edges=[(1, 2, 1, 1), (2, 1, 1, 1), (2, 3, 1, 2), (3, 2, 1, 1),  (3 , 1, 1,2), (1, 3, 1, 2),(3, 0, 0, 0)] # zrodlo, (dpid) cel,waga,port)
  else:
      try:  
          with open(cp, 'rb') as handle:   # w TYM PLIKU mamy topologie wygenerowane przez netgen2.py
              edges = pickle.load(handle) #src,dest,cost,ingrest_port 
              handle.close()
      except:
          assert False
  NS=edges[len(edges)-1][0] # read NS: last element in connections.pickle file /struct: DYNAMIC ARRAY of STATIC ARRAY,dim=NZ 5 
                            # [src,dest,cost,ingrest_port] cost=1 
                            # NZ - number of connections (number of no zero elements in connection array): file netgen2.py
  #del edges[len(edges)-1] # CO ZA KRETYN TO WPisal   remove NS info from table
  #print('DijstraEdges',edges)
  for i in range(1,NS+1):  # all switches: 10.0.0.i,   i in range from 1 to number of nodes (NS)
    if i==MY_ID:
      continue
    l,x=dijkstra(edges, MY_ID, i) #src,dest. distant node ; l: cost x: path to distant node / struct: LINKED  LIST
    if l==-1:
      #raport.write("ERROR: Cycles in graph\n")
      return -2,-2             # cycles in the graph (connection not possible)
      
    w=x                     #head of linked list
    while (w[1])[1]!=():    # while(w->next != NULL)  // get one before last element of linked list
      w=w[1]                # w=w->next
                            # in w[0] ID of nearest neighboring node
    nearestNode[i]=[w[0],-1]   #  in w[0] ID of nearest neighboring node
  for i in range(1,NS+1): # set ingress ports :  
    #if edges[i][0]==MY_ID: # My conection from self to any host
    if i==MY_ID: #skip self
      continue
    k=0
    for j in range(0,len(edges)):
      if edges[j][0]==MY_ID: #skip self
        k+=1 # count number of connections: ingress port for souce node = k+1
      if edges[j][0]==MY_ID and nearestNode[i][0]==edges[j][1]: # My conection from self to nearest host    
        ingressPort= edges[j][3] # read ingress port from  edges table
        tmp=nearestNode[i]
        tmp[1]=ingressPort 
        nearestNode[i]=tmp #update
    nearestNode[MY_ID]=[MY_ID,k+1] # set ingress port for souce node
  
# zwraca mape najjblizszego wezla i portu  od punktu MY_ID (start) do pozostalych NS wezlow
  return nearestNode,NS  # {key=dest. distant node ,val= (nearest neighboring node ,ingress port ) / struct: DICTONARY 

def createLinksDijkstra(plik="connections12mesh.pickle",edges=[]): # topologia dla alg. Dijkstry w postaci MAPY  - wywolujemy raz w konstruktorze kontrolera
    if edges==[]:
        try:
            with open(plik,'rb') as handle:   # w TYM PLIKU mamy topologie wygenerowane przez netgen2.py
        #  [(1, 2, 1, 2), (2, 1, 1, 2), (1, 5, 1, 3), (5, 1, 1, 2)...] i-node,j-node,waga,port  (i =1 .. NS;j=1..NS) 1: 10.0.0.1 ; 2- 10.0.02 ..)
        #  Na test bedzie: mapa zamieniajaca MAC ma na id 
                edges = pickle.load(handle) #src,dest,cost,ingrest_port    
        except:
            assert False
        
    NS=edges[len(edges)-1][0] 
    c=0
    mapaDijkstra = {} #slownik
    for x in edges:
        mapaDijkstra[(x[0],x[1])]=(x[2],x[3]) # klucz: link i do j ; wartosc waga, port
        c+=1
    return mapaDijkstra,c-1  #lmodyfikacjainksDijkstra[i,j]=(waga,,port) 
def getLinkDijkstra(i,j,mapaDijkstra): # zwraca [waga,port] dla polaczenia i do j . 
    if (i,j) in mapaDijkstra:
        return  mapaDijkstra[i,j]
    else:
        return [] # niema takiego linku 
def setWeightDijkstra(i,j,waga,mapaDijkstra): # ustawiamy wage, port sie NIGDY nie zmienia ! - wywolywane przez kontroler po zmianie obciazenia sieci
    if (i,j) in mapaDijkstra:
        x=mapaDijkstra[i,j]
        mapaDijkstra[i,j]=(waga,x[1]) # port zostaje
        return
    else:
        assert(0)  # niema takiego linku
def   map2tabDijkstra(mapa,ns):  # zwraca tablice  z wagami i portami dla alg. Dijksstry na podstawie mapy 
# mapa - mapa macierzy dla alg. Dijkstry wygenerowana na podstawie pliku connections:   createLinksDijkstra():
# funkcja zamienia mape na tablice dla algorytmu nearestNodeDijkstra
    tabDijkstra=[]
    for klucz in mapa:
        w=mapa[klucz]
        if w[0]==0 and w[1]==0:
            continue
        tabDijkstra.append((klucz[0],klucz[1],w[0],w[1])) #i-node,j-node,waga,port 
    tabDijkstra.append((ns,0,0,0)) # UWAGA: ten element musi byc na koncu tablicy: znacznik konca grafu
    return  tabDijkstra
def nbConn(edges,myId):
    lp=0
    for x in edges: # zliczamy liczbe polaczen z sasiadami
        #print x[0],x[1]
        if x[0]==myId:
            lp+=1
            #print x[1]," *" # x[0]  As --> x[1] sasiad
    return lp # 0 brak polaczen , blad
"""
##############   KOD TESTOWY    ################### 
nearestNode,NS= nearestNodeDijkstra(1, 12 ,edges=[],cp="connections.pickle")
print (nearestNode)
dest=7# CEL   podrozy 
#MY_IP = sys.argv[1] DOJSCIE Z MY_IP  do 10.0.0.dest    ; STARTUJEMY  z MY_IP
NEXT_NODE_IP="10.0.0."+str(nearestNode[int(dest)][0]) # dostajemy ID  NAJBLIZSZEGO  wezla na naszej sciezce 
print ("nastepny: ",NEXT_NODE_IP,"port=",nearestNode[int(dest)][1] )#  oraz nr PORTu
#setFlowTable(nearestNode) # !!!!!!!!!!!!!!!!!!!!!!!!!!!ODKOMENTOWAC  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
sys.exit()
"""

