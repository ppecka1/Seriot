import socket
import sys
import time
COM=','
if len(sys.argv)!=4:
    print('*********  Send one packet/call: udp_cli1 dpid port text')
    quit()

hname=socket.gethostname()

dpid=str(sys.argv[1])
UDP_IP = "10.0.1."+str(dpid)
#UDP_IP = "127.0.0."+dpid  #=1 - localhost
UDP_PORT = int(sys.argv[2])
#MESSAGE = b"Hello, World!" 
string =str(sys.argv[3])
string='From:'+dpid+COM+str(time.time())+COM+string
MESSAGE = string.encode(encoding='UTF-8')
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
#print("message: %s " % MESSAGE+'from '+str(hname))
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
