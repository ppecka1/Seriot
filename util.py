def hid2mac(hid): # host id dla minineta - kocowka adresu mac
    mac="00:00:00:00:00:"+str(hex(hid))   # bedzie dzialac do 254 hostow
    if hid>253:
        assert(0)
    if hid > 15:
        return mac.replace("0x", "")
    else:
        return mac.replace("0x", "0")
#def hid2mac(hid,k): # host id dla minineta - kocowka adresu mac
#    print('mapowany',hid,k)
#print hid2Mac(0),hid2Mac(10),hid2Mac(16)
#mac="00:00:00:00:00:0f"
#print int((mac).split(':')[5],16)
""" slownik {} oparty jest na hash fun. oto test:
l = []
for x in range(0, 50):
    for y in range(0, 50):
        if hash((x,y)) in l:
            print "Fail: ", (x,y)
        l.append(hash((x,y)))
print "Test Finished"

nks = {} # dict 
links[(1, 2)] = (77,12,7)
links[(12, 2)] = 'x12d'
links[(3,2)] =  0.44 

if (1,2) in links:
    print 'tak'
else:
    print 'nie'
#print links[(1,2)]
#print links[(12,2)]
print "float  ",links[(3, 2)]
print "char  ",links[(12, 2)][3] # litera d
print "tab  ",links[(1, 2)][2] #  7
print len(links)
for x in links:
    print(x,links[x],len(x))
quit()
"""
