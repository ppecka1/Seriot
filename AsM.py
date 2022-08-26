# testujemy git (4)
# Copyright (C) 2022 IITIS PAN ZMiOESK
# Copyright (C) 2022 Piotr Pecka 
# IF-CS V 1.0 Inteligent Flow Controlling  System  Copyright (C) 2022
# Based on RYU Controller
# piotr@iitis.pl 
# Agent zwiazany z Switchem: 4  watkowy (biblioteka  Process)
# CogSender - wysyla pakiety kognitywne do innnego As -a 
# CogRecv - odbiera pakiet Cog i wysyla informacje o obciazeniu do kontrolera
# CogUserSender
# CogUserRecv
# TEST na  MN :    mininet>  source init12.cli
#rewizja 2: git show  2 AsM.py
#git : git  add; git diff ; git comit   

# Piotr Pecka
import conf  # plik konfiguracyjny

from multiprocessing import Process
#import multiprocessing
import socket
import os
import sys
import time
#moje:
from  AsClasses import Connections # polaczenia do sasiednich portow
from Energy import Energy # odczyt pomiarow energi ze Sw  / Atencjone: from nazwa pliku import klasa 
#NS liczba Asow (hostow) czytana z pliku .picle wygenerow przez netgen 

#ATENCJONE :po kazdej zmianir na seriot(glowny host) nalezy przkopiowac plik AsM.py na switche seriot1, seriot2 .. 
# KOPIOWANIE: sh  scp.sh AsM.py

#UWAGA siec na test Band musi byc tak skofigurowana abu czesc IP_ADDR byla stala , a ostatni bajt zmienial sie od 1 do NS

#SendIntCog=100*MS# odstep czasu [US,MS] miedzy wysylanymi  pakietami Cognitywnymi 
#LS=20000# liczba serii
#STOP=1*MS # dla USER odstep czasu miedzy seriami 

#https://timber.io/blog/multiprocessing-vs-multithreading-in-python-what-you-need-to-know/
# ALERT:  "Since the processes don't share memory, they can't modify the same memory concurrently." 
#PAYLOAD = "\"%s , %f ,%d|%d , %f | %d , %f |\"" % (src,tim,dst,src,0,dst,delay)
COM=','

def CogSender(dpid,log,startTime,energy): # nadajnik pakietow Cog uzywa biblioteki  Process - nalezy przerobic na  thread aby mozna bylo uzyc wspolna pamiec 
    
    #start=time.time()
    log.write("*Time=*%f CogSender - aktivation\n  / ppid=%d, dpid=%d /\n" % (time.time()-startTime,os.getppid(),os.getpid())) # pid ojcow i dzieci 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP  lokalny soket  CogSender  o----->  CogRcv (zdalny soket)
    conn=Connections(dpid,conf.TOPO6) # objekt zwracajacy koelne polaczenia do sasiada
    #i=0   while i in range :  to niema sensu
    #for  k in range(0,LS): # LS liczba  serii docelowo: While True:
    while True:
        ene=energy.getEnergy()
        while True: # wyslalem do wszystkich sasiadow 
            x=conn.getNext() # zwraca kolejnego sasiada - mozliwa zmiana opcji na dowolnego hosta (przedefiniowanie klasy Connections)
            if x[0]== -1 : break # nie ma już sasiadow x[0] id sasiada (1..NS)
            adres=conf.IP_ADDR+str(x[0]) 
            #log.write("*Time=%f*  Sending Cog packet from %d to  %s\n" % (time.time()-startTime,dpid,adres))
            time.sleep(conf.SendIntCog) # co SendIntCog  ms wysylamy pakiet COG
            ##tim=time.time_ns() #aktualny czas w nano sekundach python 7
            tim=time.time()
            msg = "%d, %d, %f, %f "% (dpid,tim,time.time()-startTime,ene) #  trojka:  src,time[ns], startTime[s]  / dpid nadaje do x[0];   w x[]1] nr portu
            log.write(msg)
            msg=bytes(msg,"ascii")
            #print ('wysylam')
            try:
                sock.sendto(msg, (adres, conf.COPORT)) # 2 parametr to para: (ip,port))
            except:
                print("An exception occurred",adres)
                #quit()
          
            # pakiety UDP mozna wysylac pod dowolny  nie istniejacy adres IP - bledu nie bedzie!
    # po wyslaniu LS serii zamykamy biznes
    time.sleep(33) # czekamy az dojda ostatnie pakiety w przypadku duzego ruchu
    for i in range (1,conn.getNS()+1):# po wyslaniu serii (LS) zamykamy biznes
        end=bytes("$END$\n","ascii") # znacznik konca $END$
        sock.sendto(end, (conf.IP_ADDR+str(i), conf.COPORT)) #konczymy impreze
    log.close() # zamykamy logi - aby byly kompletne 
   
  
def CogRecv(dpid,log,startTime): # odbiornik pakietow Cog
            log.write("*Time=*%f CogRecv - aktivation\n  / ppid=%d, dpid=%d /\n" % 
            (time.time()-startTime,os.getppid(),os.getpid()))
            sock2Controler = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # gniazdo do kotrolera
            sockR = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # przez to gniazdo wchodza pakiety
            sockR1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # przez to gniazdo wchodza pakiety
            ############
            UDP_IP="0.0.0.0" # musi nasluciwac dla wszystkich ! 
            sockR.bind((UDP_IP, conf.COPORT)) # podpiecie gniazda
            #sockR1.bind((UDP_IP, 5678)) # podpiecie gniazda
            delayOld=0 # 
            while True: # szacunkowa liczba iteracji: LS*liczba sasiadow
                data, addr = sockR.recvfrom(conf.BUFSIZE) # odbieranie od addr (adres, nr portu nadajnika)
                #tim=time.time_ns() # odczyt aktualnego czasu zaraz po odebraniu wersja python 7
                tim=time.time()
                #print ('odbieram')
                msg=str(data,"ascii")
                if msg.find("$END$")!=-1:  
                    break # konczymy jezeli Sender  wysle "$END$"
                sendTime=int(msg.split(",")[1]) # czas nadania pakietu przez Sender [ns] od 1970 roku
                src=(msg.split(",")[0]) # id switcha  ktorego przyszla wiadomosc ATENCJONE:nie optymalne za duzo splitow ale tu niema to znaczenia
                AT=float((msg.split(",")[2])) # czas w [s] nadania wiadomosci
                ene=float((msg.split(",")[3]))
                if str(addr[0].split(".")[3])!=src:
                     log.write("*Time=*%f CogRecv ERROR: invalid source addres: %s %s\n" % (time.time()-startTime,src,str(addr[0])))
                delay=tim-sendTime # src,time,dst   delay: opznienie miedzy wezlami (opt. sasiednimi)
                #print ("Delta",delay-delayOld) # Musi byc mapa
                #if (delay-delayOld)<DELTA: continue #nie informujemy kotrolera
                delayOld=delay
                if delay<0:
                    delay= -delay
                    log.write("*Time=*%f WARNING: CogRecv  <NEGATIVE TIME> %s \n" % (time.time()-startTime,addr))
                
                #ATENCJONE :po kazdej zmianie na seriot(glowny host) nalezy przkopiowac plik AsM.py na switche seriot1, seriot2 .. 
                #energy=0.9
                log.write("*Time=*%f CogRecv - receiving  COG packet from %s delay[NS]=%d ENERGY=%f\n"
                 % (time.time()-startTime,addr,delay,ene))
                #DT=sendTime-int(startTime*1000*1000*1000) # czas  nadania pakietu przez Sender [ns]  od uruchomienia AS-ow 
                #DT=int(startTime*1000*1000*1000)
                #print(DT," " , sendTime)
                #AT=sendTime/1000-startTime*1000000# startTime czas od startu generatorow ruch w ulamkach [s] zamieniamy na [us]
                                                    # sendTime czas nadani w us zamieniamy na us
                msg="$DELAY$ "+src+COM+str(dpid)+COM+str(AT)+COM+str(delay)+COM # nowy msg: $DELAY$ src, dst, DT, delay
                sock2Controler.sendto(bytes(msg,"ascii"),( str(addr[0]), conf.UDP_CTRL)) # do kontrolera poprzez adres nadawcy
            log.close()    

            """sendTime=int(msg.split(",")[1]) # czas nadania pakietu przez Sender [ns] od 1970 roku
            src=(msg.split(",")[0]) # id switcha  ktorego przyszla wiadomosc
            AT=float((msg.split(",")[2])) # czas w [s] nadania wiadomosci
            if str(addr[0].split(".")[3])!=src:
                 log.write("*Time=*%f CogRecv ERROR: invalid source addres: %s %s\n" % (time.time()-startTime,src,str(addr[0])))
            """
#sudo  ovs-appctl ofproto/trace s2  in_port=3,tcp,nw_src=10.0.0.2,tcp_dst=2

if __name__ == '__main__': 

    myId=int(sys.argv[1]) # dpid : id Agena : 1..NS
    
    logFileName="./Logs/logAsMRcvCog"+conf.IP_ADDR+str(myId)+".txt"
    if os.path.exists(logFileName):
        os.remove(logFileName)
    log1 = open(logFileName,"w")
    
    logFileName="./Logs/logAsMSenderCog"+conf.IP_ADDR+str(myId)+".txt"
    if os.path.exists(logFileName):
        os.remove(logFileName)
    log2 = open(logFileName,"w")
    
   
    energy=Energy() # pomiar energi z Sw 
    startTime=time.time() # cas w [s] floating point 
    # kognitywne
    pRcv  = Process(target=CogRecv, args=(myId,log1,startTime,))
    pRcv.start() # sem.value nie dziala!!!  trzeba wystartowc watek odbierajacy Rcv w  pierwszej kolejnosci
   
    pSender = Process(target=CogSender, args=(myId,log2,startTime,energy,))
    pSender.start() # sender moze juz nadawac 
    #pUserRcv=Process(target= UserRcv, args=(myId,log3,startTime,))
    #pUserRcv.start()
   

