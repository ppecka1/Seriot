import sys
import os
import socket
import time
# moje:
import conf

#IP_ADDR="10.0.0." # na test bandzie  zmienic MAX liczba wezlow: 0xFF-1 :ostatni bajt
def UserRcv(dpid,log): # odbiornik pakietow Cog
            #if dpid!=12: return
            sockR = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # przez to gniazdo wchodza pakiety
            UDP_IP="0.0.0.0" # musi nasluciwac dla wszystkich ! 
            #UDP_IP="10.0.0."+str(dpid)
            sockR.bind((UDP_IP, conf.USPORT)) # podpiecie gniazda
            while True: # szacunkowa liczba iteracji: LS*liczba sasiadow
                data, addr = sockR.recvfrom(conf.BUFSIZE) # odbieranie od addr (adres, nr portu nadajnika)
                tim=time.time_ns() # odczyt aktualnego czasu zaraz po odebraniu
                msg=str(data,"ascii") # 
                print ("rcv",msg)
                if msg.find("$END$")!=-1:  
                    break # konczymy jezeli Sender  wysle "$END$"
                print ("userRcv: "+str(dpid)," ",msg)
                sys.stdout.flush()
myId=sys.argv[1]
logFileName="./Logs/logAsMRcvUser"+conf.IP_ADDR+str(myId)+".txt"
if os.path.exists(logFileName):
    os.remove(logFileName)
log = open(logFileName,"w")

UserRcv(myId,log)
