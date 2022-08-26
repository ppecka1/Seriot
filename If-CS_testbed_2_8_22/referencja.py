from copy import copy
t=[(1, 2, 1, 1), (1,3,1,2),(2,1,1,1),(2,4,1,2),(3,1,1,1),(3,4,1,2),(3,5,1,3),
        (4,2,1,1),(4,3,1,2),(4,6,1,3),(5,3,1,1),(5,6,1,2),(6,4,1,1),(6,5,1,2),(6,0,0,0)]
pt=copy(t) #kopia
pt=t #referencja
pt[1]=(6,0,0,0)
print (t)
print(pt)        
# zmiana pojedynczego elementu w tuple
x=t[3] # (2,4,1,2)
y = list(x)  #zamieniamy tuple na list
y[2] = 123 #zmieniamy 4 na 123
x = tuple(y) # ponownie  zmieniamy liste na tuple
t[3]=x # umiesczamy w tablicy
print (t)
