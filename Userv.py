import sys
import os
import socket
import time
# moje:
COM=','
import conf

IP_ADDR="10.0.1." # na test bandzie  zmienic MAX liczba wezlow: 0xFF-1 :ostatni bajt
def UserRcv(dpid,log): # odbiornik pakietow Cog
            #if dpid!=12: return
            sockR = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # przez to gniazdo wchodza pakiety
            UDP_IP="0.0.0.0" # musi nasluciwac dla wszystkich ! 
            #UDP_IP="10.0.0."+str(dpid)
            sockR.bind((UDP_IP, conf.USPORT)) # podpiecie gniazda
            startTime=time.time()
            while True: # szacunkowa liczba iteracji: LS*liczba sasiadow
                data, addr = sockR.recvfrom(conf.BUFSIZE) # odbieranie od addr (adres, nr portu nadajnika)
                tim=time.time() # odczyt aktualnego czasu zaraz po odebraniu
                msg=str(data,"ascii") # 
                sendTime=float(msg.split(COM)[1]) #czas nadania
                delay=time.time()-sendTime
                log.write("*Time=*%f CogRecv - receiving  COG packet from %s   delay[Sec]=%f\n"
                % (time.time()-startTime,addr,delay)) # addr (host,temporary port)
                print ("delay time:",delay,'from: ' ,addr) 
                if msg.find("END")!=-1:  
                    break # konczymy jezeli Sender  wysle "$END$"
            
             

                #print ("userRcv: "+str(dpid)," ",msg,' ',tim)
                #sys.stdout.flush()
dpid=sys.argv[1]
logFileName="./Logs/logRcvUserPacketAgent-"+conf.IP_ADDR+str(dpid)+".txt"
if os.path.exists(logFileName):
    os.remove(logFileName)
log = open(logFileName,"w")


UserRcv(dpid,log)
log.close()


#log.write("*Time=*%f CogRecv - receiving  COG packet from %s delay[Sec]=%f ENERGY=%f\n"
#                 % (time.time()-startTime,addr,delay,ene))


