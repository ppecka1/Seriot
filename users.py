from multiprocessing import Process
#import multiprocessing
import socket
import os
import sys
import time
import subprocess

# Moje:
import conf

#IP_ADDR="10.0.0."
NaS=0.000000001 # nano sekunda
US=0.000001 # mikro sekunda
MS=0.001 
SEC=1.0
COM=','
#BUFSIZE=1024 # bufor odbiornika udp 
#UDP_USER=5008
#NS=12
#NP=4000000 # liczba pakietow
#####
#SendIntUser=0.01*MS# odstep czasu [US,MS] miedzy wysylanymi  pakietami
def UserSender(dst,log,startTime,NS=6): # nadajnik pakietow USER 
    # quit()
    #print ("sender:",dpid)
    adres=conf.IP_ADDR+str(dst)
    cmd="ifconfig  | grep \"inet 10\" | cut -d \":\" -f 2"
    myIp=subprocess.check_output(cmd ,  shell = True)
    myIp=str(myIp).split("inet")[1] #
    myIp=str(myIp).split("netmask")[0] #
    #print(str(ip))
    #adres=IP_ADDR+str(12)
    """if dpid==1: # 1-->12 #krzyzowy ogien
        adres=IP_ADDR+str(12) 
        print (dpid)
    if dpid==2: # 1-->12 #krzyzowy ogien
        adres=IP_ADDR+str(12) 
    elif dpid==9: #12-->1
        adres=IP_ADDR+str(12)
    elif dpid==5: #12-->1
        adres=IP_ADDR+str(12)"""
    #elif dpid==9: #2-->10
    #   adres=IP_ADDR+str(4) 
    #elif dpid==10: #10-->2
    #adres=IP_ADDR+str(2)
    #else: return # inne akcje pomijamy
    myPid=os.getpid()
    print("Sender:",str(myIp))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP  lokalny soket  Sender  o-----> Rcv (zdalny soket)
    for i in range(0,conf.NP):
        msg="User sender"+COM+str(myIp)+COM+"Send time: "+str(time.time())#_ns())
        #msg="$END$"
        msg=bytes(msg,"ascii") #bez tego wyrzyca wyjątki
        #print("sender:",myPid)
        try:
            sock.sendto(msg, (adres, conf.USPORT)) # 2 parametr to para: (ip,port))
        except:
            print("An exception occurred",adres)
        time.sleep(conf.SendIntUser) 
    print('SLeep')
    time.sleep(5*3600) 
    print('End')
    #msg="$END$"
    #msg=bytes(msg,"ascii")
    #sock.sendto(msg, (adres, UDP_USER)) 

                #delay=tim-sendTime # src,time,dst   delay: opznienie miedzy wezlami (opt. sasiednimi)
                #print ("Delta",delay-delayOld) Musi byc mapa
                #if (delay-delayOld)<DELTA: continue #nie informujemy kotrolera
                #log.write("*Time=*%f CogRecv - receiving  COG packet from %s delay[NS]=%d\n" % (time.time()-startTime,addr,delay))
                #DT=sendTime-int(startTime*1000*1000*1000) # czas  nadania pakietu przez Sender [ns]  od uruchomienia AS-ow 
                #DT=int(startTime*1000*1000*1000)mininet> h7  python3 users.py 3

                #print(DT," " , sendTime)
                #AT=sendTime/1000-startTime*1000000# startTime czas od startu generatorow ruch w ulamkach [s] zamieniamy na [us]
                # sendTime czas nadani w us zamieniamy na us
            #log.close()    
if __name__ == '__main__': 
    # podajemy adres zrodla jako argument , cel  ustawiamy w   UserSender(dst,log,startTime,NS=6)
    dst=int(sys.argv[1]) # dpid : id Agena : 1..NS
    
    
    # user
    startTime=time.time() # cas w [s] floating point 
    log3=None
    #pSndUser=Process(target=UserSender, args=(dst,log3,startTime,))
    #pSndUser.start()
    UserSender(dst,log3,startTime)
    log3=None
    #pRcvUser=Process(target=UserRcv, args=(myId,log3,startTime,))
    #pRcvUser.start()
    
    
    #pSndUser.join()
    #pRcvUser.join()

