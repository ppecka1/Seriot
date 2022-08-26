import pickle
class Connections:  # polaczenie do sasiednich wezlow z dpid do id przez port
     def __init__(self,dpid,edges=[]): # dpid id wezla dla ktorego znajdujemy polaczenia
         self.edges=edges            
         self.conn=[] #sasiedzi
         self.nxt=0
         self.dpid=dpid
         for x in self.edges:  # x[0] - src ; x[1] - dst ; x[2] - waga; x[3] - port
             if x[1]==x[2]==x[3]==0 : continue # pomijamy element (NS,0,0,0) na koncu zbioru edges
             if x[0]== dpid:  # zapisujemy do tablicy conn polaczenia do sasiadow 
                 self.conn.append((x[1],x[3])) # dodajemy id sasiada 10.0.0.id oraz numer portu 
     def getNS(self): # zwraca liczbe wezlow sieci 
         return self.edges[len(self.edges)-1][0] # ostatni element  0 pozycja to rozmiar: [NS,0,0,0] od 1 do NS 
     def getNext(self): # Zwraca (id,port)
        # nie da sie f(SELF,...) to ERROR: takes 0 positional arguments but 1 was given
        if self.nxt<len(self.conn):
            x=self.conn[self.nxt]
            self.nxt+=1   
            #print (self.dpid,"---->",x)
            return x
        self.nxt=0  # zerujemy id polaczenia dla nastepnego przepytywania
        #return 1
        #print("ASM: nastepny")
        return -1,-1 # znacznik konca polaczen
#test
# polaczenie dla 6 -ego wezla:
"""
topo6=[(1, 2, 1, 1), (1,3,1,2),(2,1,1,1),(2,4,1,2),(3,1,1,1),(3,4,1,2),(3,5,1,3),
    (4,2,1,1),(4,3,1,2),(4,6,1,3),(5,3,1,1),(5,6,1,2),(6,4,1,1),(6,5,1,2),(6,0,0,0)]

con=Connections(1,topo6)

while True:
    x= con.getNext()
    print( x)
    if x==(-1,-1): break
    
#print (x)
print ("liczba wezlow:")
print (con.getNS())
"""
           
           
