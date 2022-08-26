# dla algorytmu RNN
""" parser portow: tworzymy obiekt RnnPathDesignator(path_json) , path_json - odpowiedz od Rnn  (java - przez socket); uzywamy metody getPort() 
""" 
import json
EOL="\n"
class RnnPathDesignator:  
    def __init__(self, paths):  #Omnetpp c++ getPathsJson(string paths);
        self.paths= json.loads(paths)
        self.sid=self.src=self.dst=-666
        self.portMap={} # slownik: klucz: (sid,src,dst)  ; sid:  "device id"  /  wartosc: nr portu 
        #self.portMapPrev={} tu zapisujemy pocztkowe ustawienia z dijkstry  (src,dest) for for...
        self.convPaths2porty()#wywolanie f. prywatnej parsujacej
        #
        # ZMODYFIKOWAC: convPaths2porty() (update) tak aby getPort zwracal -1 gdy port sie nie zmieni
    #def updatePaths2porty(self): 
    def convPaths2porty(self): # f. pomocnicza zamienia odp. z Rnn (paths.json) do slownika porty
        nodes=self.paths['paths']
        for i in nodes:    # idziemy po nodes[] 
            src=int(i['src']) #
            dst=int(i['dst']) #
            x=i['nodes'] 
            #print (x) # w x ('output port'  oraz 'device id')
            for j in x:
                dpid=int(j['device id']) # identyfikator wezla dla ktorego ustawiamy sciezki 
                port=int(j['output port']) # numer portu
                #print (dpid,src,dst,port)
                if (dpid,src,dst) not  in self.portMap:
                    self.portMap[(dpid,src,dst)]=port # zapisanie do mapy znacznie przyspieszy
                else:
                    print('portmap=',port)
                    assert(0) # self.portMap[(dpid,src,dst)]=  -2 (-1 inicalizacja)
    def getPort(self,dpid,src,dst): # dla uzytkownika  UWAGA: na drodze od src do dst sprawdzamy dpid: portMap[(dpid,src,dst)] 
                                #jezeli port<> -1 to to weze dpid jest na sciezce src-dst
        if (dpid,src,dst)   in self.portMap:
            return self.portMap[(dpid,src,dst)]# odczyt z mapy nr portu (dpid,dpid,dst) sprawdzamy w portMapPrev czy sie zmienil
            # jak sie zmienil wpisz do portMapPrev
        else:
            #assert(False)
            return -1 # -1 zwracamy gdy sie nie zmienil lub niema w portMap

"""obiekt komunikacyjny z RnnJava dla Rnn Algo    
"""
import os
import socket
import time

class PayloadInfoSender:
# tworzymy obiekt RnnPathDesignator(path_json) , path_json - odpowiedz od Rnn  (java - przez socket); uzywamy metody getPort() 
#Omnetpp c++ getPathsJson(string paths);
    def __init__(self,host="127.0.0.1",port=9999):  #Omnetpp c++ getPathsJson(string paths);
        #os.system("pkill java") #ubijam proces javy w najprostszy spososob
        #os.system("export RNN=$HOME");
        #os.system("$HOME/mininet/Rnn/Tmp/java  org.iitis.InformationFeeder topo12.json pipe ")
        #V Tu wywolujemy serwer RNN defaltowy plik: topo12.json 
        #os.system("cd  ~/mininet/Rnn/Tmp; java  org.iitis.InformationFeeder  topo12.json pipe >/dev/null& ")
        try:
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while self.sock.connect_ex((host, port)): # czekamy na Rnn Java sever
                time.sleep(0.1)
        except:
            pass
           
            
    def send2Rnn(self,msg): # 
        msg_bytes = bytes(msg+EOL,'ascii')
        data = ""
        self.sock.send(msg_bytes)
        data = ""
        #print("wysylam ",msg)
        while True:
            chunk=self.sock.recv(8*1024) #recv(1024)
            chunk=str(chunk,'UTF-8')
            data+=chunk
            if chunk.find("}]}")!=-1: #  znaleziono  znacznik konca danych 
                break
        #print(data) tu jes ok
        return data #zwraca dane dla
    def __del__(self):
        print ("Zamykam polaczenie")
        os.system("pkill java") #ubijam proces w najprostszy spososob
        self.sock.close()    
