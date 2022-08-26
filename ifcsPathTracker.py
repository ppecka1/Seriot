import subprocess
import sys
import pickle
from random import randint
from util import hid2mac #dziala tylko fla adresu: 
from ifcsPathTracker2d import mapSrcPort2Nearest,getNearestNode
#getNearestNode(srcPort2Nearest,node,port): # zwraca wezel sasiada node na podstawie portu  port
#MAC="00:00:00:00:00:" # Attencjone: przy przenoszeniu trzeba mapowac !!!

# podajemy 2 
# format:  cookie=0x0, duration=6216.159s, table=0, n_packets=0, n_bytes=0, priority=58888,udp,dl_dst=00:00:00:00:00:04,tp_dst=5008 actions=output:1
#cmd:   sudo ovs-ofctl  -O OpenFlow13 dump-flows s4 grep 5008
#V wczytanie informacji o flowach dla wszystkich wezlow
with open('connections12mesh.pickle', 'rb') as handle:
     edges = pickle.load(handle) #src,dest,cost,ingrest_port 
NS=edges[len(edges)-1][0] # liczba wezlow
nodes= [ "" for i in range(NS+1)] # indexujemy od 1   , ostatni element (NS,0,0,0) nie uzywany
nodes3d = [[[-1 for k in range(NS+1)] for j in range(NS+1)] for i in range(NS+1)]  # [dpid][dst][,src]

#src=int(sys.argv[1])
#dst=int(sys.argv[2])
#uport=int(sys.argv[3]) #udp port dla flow-ow
uport_prior=5008
uport_prior=58889 #filrujemy wg. portu albo priorytetu
start=int(sys.argv[1])
stop=int(sys.argv[2])
uport_prior=int(sys.argv[3])
with open('connections12mesh.pickle', 'rb') as handle:
     edges = pickle.load(handle) #src,dest,cost,ingrest_port 
NS=edges[len(edges)-1][0] # liczba wezlow
srcPort2Nearest=mapSrcPort2Nearest(edges)
for dpid_ in range(1,NS+1):
    cmd="sudo ovs-ofctl  -O OpenFlow13 dump-flows s%d | grep %d"%(dpid_,uport_prior)
    nodes3d[dpid_][0][0]=subprocess.check_output(cmd ,  shell = True) 
#print(nodes3d[1][0][0])
#print('-----------------------------------------------')
#print(nodes3d[1][0][0])
#NS=12
for dpid_ in range(1,NS+1):
    node=nodes3d[dpid_][0][0]
    node=str(node,"ascii")
    pos=0
    #print (node)
    
    begin=0
    #end=len(node)
    #print (end) 
    #quit()
    while True:
        if begin >=end: break
        pos_src=node.find('dl_src=',begin,end)      
        src=node[pos_src:pos_src+24]  
        #if pos_src== -1: break
        pos_dst=node.find('dl_dst=',begin,end)  
        dst=node[pos_dst:pos_dst+24]
        pos_output=node.find('output:',begin,end)  
        output=node[pos_output:pos_output+10]
        ds=(pos_output+10-begin)
        #pos_src+=pos_output
        src=src.split(':')[5];src=int(src,16)
        dst=dst.split(':')[5];dst=int(dst,16)
        output=output.split(':')[1];output=int(output)
        nodes3d[dpid_][dst][src]=(output,-8)
        #print(src,dst,output)
        begin+=ds
#print(nodes3d)
print('Start node:',start)
dpid=start
while True:
    nextNodePort=nodes3d[dpid][stop][start]
    if nextNodePort== -1: break; print('no passage !')
    dpid=getNearestNode(srcPort2Nearest,doid,nextNodePort)  # zwraca wezel sasiada node na podstawie portu  port
    print('<-- ', dpid ,'-->')
    if dpid==stop: break; print('End node:,',stop)


#print (start)
## GO from start to stop
#src=start
#dst=stop
#while True:
#    step=
"""
for dpid_ in range(1,NS+1):
    for dpid_ in range(1,NS+1):
    cmd="sudo ovs-ofctl  -O OpenFlow13 dump-flows s%d | grep %d"%(i,uport)
    nodes3d[dpid_][0][0]=subprocess.check_output(cmd ,  shell = True)

def mapSrcPort2Nearest(): # tworzy mape sasiednich wezlow
    srcPort2Nearest={}
    for x in  edges:
        srcPort2Nearest[(x[0],x[3])]=x[1]  # x[0] node, ,x[3] nr portu do sasiada x[1]
    return srcPort2Nearest
srcPort2Nearest=mapSrcPort2Nearest()
#print(srcPort2Nearest)
#print(srcPort2Nearest)
if src==dst: # nie ma co przeszukiwac 
    print(src,"-->",dst)
    quit()
def getNearestNode(srcPort2Nearest,node,port): # zwraca wezel sasiada node na podstawie portu  port
    return srcPort2Nearest[node,port]
n=src #node poczatkowy 1..12(N)
print ("Start node:",src)
while True:
    node=str(nodes[n],"ascii")
    if n==dst:
        print("End node:",n);break #Doszlismy do konca grafu przeszukiwan
    else:
        print("<--",n,"-->")
    pos=node.find(hid2mac(dst))
    if pos== -1: assert(0)
    port=int(node[pos:].split("output:")[1][0:2]) # port sasiada 
    #print ("port=",port)
    n=getNearestNode(srcPort2Nearest,n,port) #zwraca sasiada na podstawie nr portu
   
        
        
    
    
    
    
quit()
#sudo ovs-ofctl  -O OpenFlow13 dump-flows s4 grep 5008

#res=subprocess.check_output(['ls', '-l']) # zapisuje do res wynik polecenia ls -l
#res=str(res,'ascii') # bajty zamienia na stringi
#res=res.split("\n") # rodzela string na liste(tablice) stringow odzielonych znakiem nowej linii
#print(nodes[2].find("00:00:00:00:00:01"))
#string=str(nodes[1],"ascii")
node=str(nodes[1],"ascii")
pos=node.find(MAC+"07")
port=node[pos:].split("output:")
print (int(port[1][0:2])) # nr portow  do FF albo do 99 zalezy czy szesnastkowo czy nie
#print(str(nodes[2],"ascii")) # wyswietla 5 linie
"""
