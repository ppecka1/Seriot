# LAUNCH: netgen2.py>netg.py   (netg.py is included by mynet2.py)
# generates file with topology for servers:   connections.pickle
#
from  random import randint 
import sys
import pickle
#print 0 % 8,1%8,8%2
X=4
Y=3
NS=X*Y# liczba switchy i hostow  :  werjsja Test
M=2# srednia liczba polaczen
#NS=4# liczba switchy i hostow :  wersja robocza 
#M=1# srednia liczba polaczen
SKIP=1 # no mtxCheker
P=100 #prawdopod polaczenia w
sw=[2 for i in xrange(NS)] # zajete numery portow: od 2 bo najpierw ida asy
dh = [1 for i in xrange(NS)] # zajete numery portow
matrix = [[]] # macierz polaczen w jednym kierunku
#[[0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]]
#    sw1   <==> sw2,sw3         ............................                        sw5<==>6      sw6 (brak polaczen) 
def mtxGenSnake(matrix,ns,m): #iteracyjny
    matrix = [[0 for i in xrange(ns)] for i in xrange(ns)]  # od 0 do ns -1
    for i in xrange(0,ns-m):
        for j in xrange(0,m):
            p=randint(1,100) #element losowosci
            if p<=P:
                matrix[i][i+j+1]=1
    return matrix
X=4
Y=3  
NS=X*Y
def mtxGenMesh(matrix, X,Y): #i siatka:   X na Y ;  N*M wezlow
    ns=X*Y;
    matrix = [[0 for i in xrange(ns)] for i in xrange(ns)]  # od 0 do ns -1
    for i in xrange(ns):
        p=randint(1,100)
        if p<=P:
            if  i<(ns-1) and  ((i+1) % (Y+1)) !=0: #  ostatnia kolumna nie ma sasiada z prawej strony 
                #print i+1," ",i+2  
                matrix[i][i+1]=1     
        if  i<((X-1)*Y-1): #  ostatni wiersz nie ma sasiada na dole 
            #print i,i+Y+1
            #print i+1,i+Y+2
            matrix[i][i+Y+1]=1    
            #print i+1,i+Y+2
            #print "---------------------"    
             
    return matrix
#print matrix
#mtxGen=mtxGenSnake # mozna wybrac algorytm generacji na podstawie macierzy zero jedynkowej 
#matrix=mtxGenSnake(matrix,NS,M)
matrix=mtxGenMesh(matrix,X,Y)
#print matrix
dijkstra=[(1, 2, 1, 1), (2, 1, 1, 1), (2, 3, 1, 2), (3, 2, 1, 1),  (3 , 1, 1,2), (1, 3, 1, 2),(3, 0, 0, 0)] # zrodlo, (dpid) cel,waga,port) 
def netGen(matrix,ns):
  #dijkstra="    edges = [\n"
  stri="# Add hosts and switches\n" # Topologia dla Minineta
  stri+="from mininet.topolib import Topo\n"
  stri+="class Project( Topo ):\n"
  stri+="    def __init__( self ):\n" 
  stri+="        Topo.__init__( self )"
  stri+="\n      # Add hosts and switches\n\n"  
  for i in xrange(ns):
    stri+="        Sw"+str(i+1)+" = "+"self.addSwitch( " +"'s"+str(i+1)+"' )\n"  
  for i in xrange(ns):
    stri+="        As"+str(i+1)+" = "+"self.addHost( " +"'h"+str(i+1)+"' )\n"   
  stri+="\n      # Add As <-------> Sw  links\n\n" 
  for i in xrange(ns):
    stri+="        self.addLink( "+"Sw"+str(i+1)+","+"As"+str(i+1)+","+str(1)+","+str(1)+ " )\n"
  stri+="\n      # Add links\n\n"  
  dijkstra=[] # **************  TUTAJ tworzymy topologe zapisana w pliku picle **********
  for i in xrange(ns):
    for j in xrange(i+1,ns):
       if matrix[i][j]==1:
        element=(i+1,j+1,1,sw[i]) # 10.0.i+1 is conected to 10.0.j+1 
        dijkstra.append(element)
        element=(j+1,i+1,1,sw[j]) # 10.0.j+1 is conected to 10.0.0.i+1    ( 2 directions link ) , weight of node =1, ingress port
        dijkstra.append(element)
        stri+="        self.addLink( "+"Sw"+str(i+1)+","+"Sw"+str(j+1)+","+str(sw[i])+","+str(sw[j])+ " )\n"
        sw[i]+=1
        sw[j]+=1
  
  stri+="        return\n"
  stri+="topos = { 'project': ( lambda: Project() )}\n"
  return stri,dijkstra

  




x,dijkstra=netGen(matrix,NS)
element=(NS,0,0,0) # append number of switches: element[0]
dijkstra.append(element)
f= open("connections.txt","w")
with open('connections.pickle', 'wb') as handle:
      pickle.dump(dijkstra, handle, protocol=pickle.HIGHEST_PROTOCOL)
ns=NS   
print x
f.write("%s\n" %str(dijkstra))
print "#########################"
print dijkstra
