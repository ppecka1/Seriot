import subprocess
import sys
import pickle
from random import randint
from util import hid2mac #dziala tylko fla adresu:
#MAC="00:00:00:00:00:" # Attencjone: przy przenoszeniu trzeba mapowac !!!

# podajemy 2 
# format:  cookie=0x0, duration=6216.159s, table=0, n_packets=0, n_bytes=0, priority=58888,udp,dl_dst=00:00:00:00:00:04,tp_dst=5008 actions=output:1
#cmd:   sudo ovs-ofctl  -O OpenFlow13 dump-flows s4 grep 5008
#V wczytanie informacji o flowach dla wszystkich wezlow
with open('connections12mesh.pickle', 'rb') as handle:
     edges = pickle.load(handle) #src,dest,cost,ingrest_port 
NS=edges[len(edges)-1][0] # liczba wezlow
nodes= [ "" for i in range(NS+1)] # indexujemy od 1   , ostatni element (NS,0,0,0) nie uzywany

src=int(sys.argv[1])
dst=int(sys.argv[2])
uport=int(sys.argv[3]) #udp port dla flow-ow
for i in range(1,NS+1):
    cmd="sudo ovs-ofctl  -O OpenFlow13 dump-flows s%d | grep %d"%(i,uport)
    nodes[i]=subprocess.check_output(cmd ,  shell = True)


def mapSrcPort2Nearest(edges): # tworzy mape sasiednich wezlow
    srcPort2Nearest={}
    for x in  edges:
        srcPort2Nearest[(x[0],x[3])]=x[1]  # x[0] node, ,x[3] nr portu do sasiada x[1]
    return srcPort2Nearest
srcPort2Nearest=mapSrcPort2Nearest(edges)
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
