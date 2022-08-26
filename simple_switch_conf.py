IP_ADDR="10.0.0." # na test bandzie  zmienic MAX liczba wezlow: 0xFF-1 :ostatni bajt
TOPO="connections12mesh.pickle" # plik binarny z topolagia sieci dla alg routingu : plik *topo_dijkstra.py* *RoutingAlgoInterface.py* *simple_switch0_Mat.py*
NS=12 #liczba switchy mozna odczytac funkcja  createLinksDijkstra("connections12mesh.pickle")
TestMode=True #rowne opoznienia do testow MOZLIWE sztuczne obciazenie wybranych wezlow:   *simple_switch0_Mat.py* linia: @wagi
RoutingAlgo=-1 # 0 (DA) 1 (DW) 2 (Rnn) Dijkstra bez wag, z wagami, oparty o siec  neuronowa 
#EqualWeigthMode=False 
################################
NaS=0.000000001 # nano sekunda
US=0.000001 # mikro sekunda
MS=0.001 
Sec=1.0 #float
SEC=1 # integer
##################################
SendIntCog=10*MS# odstep czasu [US,MS] miedzy wysylanymi  pakietami Cognitywnymi 
FlowTimeOut=40*SEC  # po tym czasie wywolany zostanie alg. routingu
CAP=1000 # pojemnosc zgloszen pakietow kognitywnych - po przekroczeniu - wywolania alg. Routingu
COPORT=5007 # nr portu dla pakietow COG
PRIOCOG=58888 # priorytet dla COG
UDP_CTRL=5006 # wyslanie na ten port przekierowuje pakiet do kontrolera plik   *AsM.py*
BUFSIZE=1024
DELTA=1*1000 #  opoznienie progowe   [NS] - ponizej nie wysylamy infomacji do kontrolera  *AsM.py*
#####################################
USPORT=5008 # nr portu dla pakietow USER *users.py*  *Userv.py* /mininet: *user.cli* *init12sv.cli*
PRIOUS=58888 # priorytet dla pakietow user  (proporcjonalnie do wielkosci)
SendIntUser=0.0001*MS# odstep czasu [US,MS] miedzy wysylanymi  pakietami
NP=4000000 # liczba pakietow wysylanych prze USER plik:  *users.py*
