Najwazniejsze pliki systemu If-CsV1.0:
	simple_switch0_Mat.py - klasa kontrolera
	conf.py - plik konfig. ustawienie parametrów ruchu, wybór alg.
	RoutingAlgoInterface.py - implem alg. routingu - modyfikujemy  funkcję hid2mac()  - util.py
	util.py - f. hid2mac()
	netgen.py - generator macierzy - pokazuje jak tworzyć plik z topologią .pickle (plik binarny )
		topologia jest tablicą czwórek(w pythonie nazywają to listą - nie mylić z linked list) :
		np.         dijkstra=[(1, 2, 1, 1), (2, 1, 1, 1), (2, 3, 1, 2), (3, 2, 1, 1),  (3 , 1, 1,2), (1, 3, 1, 2),(3, 0, 0, 0)] # zrodlo (dpid), cel,waga,port)
	rnnLib.py -parser i sender wiadomości do serwera Rnn (unitedRNNPlugin.jar)
	AsM.py - 2 procesowy nadajnik i odbiornik pakietów COG
	Userv.py - odbiorni pakietów USER
	users.py
	*.cli - sposób wywołania serwerów i klientów COG USER (mininet)
Pzostałe pliki nie wymagają edycji
Pliki narzędziowe: 
	ifcsPathTracker.py - sledzi pakiet na podstawie zewnętznego polecenia ovs-ofctl -wersja dla Rnn (3 wymiarowa tablica)
	ifcsPathTracker2d.py - wersja dla DW i DA - 2 wymiarowa tablica
		
			*** Ewentualne brakujące pliki na bisonie   ****
Pomocna funkcja basha wyswietla nazwę i pojawienie sie  wybranego stringu w plikach *.cc, *.py ....
finds2() {

	#find . -type f \( -name "*.cc" -o  -name "*.h" \) -exec grep   $1 {} \;
	find . -type f \( -name "*.py" \) -exec grep  --with-filename  $1 {} \; # TYLKO *.py

					CAłóść około 100 KB kodu w pytonie
