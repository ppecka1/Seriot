UWAGA:  setxkbmap pl nie dziala na tej wersji ubuntu: 18.04.1-Ubuntu - SMP stad brak polskich znakow
Library for testing routing algo. in openflow networks using Ryu Controler (TestBed ver for 6 switches and one controler)
  
Najwazniejsze pliki systemu If-CsV1.0:
 - simple_switch_13.py - klasa kontrolera
 - conf.py - plik konfig. ustawienie parametrów ruchu, wybór alg.
 - RoutingAlgoInterface.py - implem alg. routingu - modyfikujemy  funkcję hid2mac()  - util.py
 - util.py - f. hid2mac()
 - netgen.py - generator macierzy - pokazuje jak tworzyć plik z topologią .pickle (plik binarny) topologia jest tablicą czwórek(w pythonie nazywają to listą - nie mylić z linked list) :
		np.         dijkstra=[(1, 2, 1, 1), (2, 1, 1, 1), (2, 3, 1, 2), (3, 2, 1, 1),  (3 , 1, 1,2), (1, 3, 1, 2),(3, 0, 0, 0)] # zrodlo (dpid), cel,waga,port)
	rnnLib.py -parser i sender wiadomości do serwera Rnn (unitedRNNPlugin.jar)
	AsM.py - 2 procesowy nadajnik i odbiornik pakietów COG
	asm (alias dla sh AsM.sh) odpala serwery dla pakietow COG
	Userv.py - odbiornik pakietów USER
	Userv.sh dpid  - odpala serwery dla pakietow USER
	users.py - nadajnik  pakietów USER
	*.cli - sposób wywołania serwerów i klientów COG USER (mininet)

Pozstałe pliki nie wymagają edycji.


 
Kontroler (seriot)uruchamiamy na hoscie: seriot w kartotece ~/ryu:
   PYHTONPATH=. ryu-manager  --observe-links ryu/app/gui_topology/gui_topology.py ryu/app/simple_switch_13.py 
Przed uruchomineiem kontrloera na tym samy hosci w kartotece ~/ryu/ryu/app
 kasujemy wszyskie flowy i procesy za pomoca aliasow (.bashrc) :def (uusuwa flowy na kotrolerze) oraz kip 
 (usuwa procesy w python3 na wszystkich hostach seroit1 - seriot6)
 Procesy (3 procesowe: glowny,nadajnik i odbiornik pakietow) roznaszace pakiety kognitywne 
 (niosa informacje o opoznieniach i energii w switchach OpenVswitch (seriot1 -seriot6) uruchamiamy aliasem asm.
 
 
Pliki narzędziowe (testowane tylko na mininet !!!!!!!):
 - ifcsPathTracker.py - sledzi pakiet na podstawie zewnętznego polecenia ovs-ofctl -wersja dla Rnn (3 wymiarowa tablica)
 - ifcsPathTracker2d.py - wersja dla DW i DA - 2 wymiarowa tablica
Uwagi:
   setxkbmap pl nie dziala na tej wersji ubuntu: 18.04.1-Ubuntu - SMP stad brak polskich znakow  
   Nalezy sledzic  pliki z logami np. rapas, rapaser - informacje o ewentualnych bledach w procesach (agentach)
   pythona np. niedopiete urzadzenie (usb) dopomiaru enegii /dev/ttyACM0 na serwerze nr 5  
		
			*** Ewentualne brakujące pliki na bisonie   ****
Pomocna funkcja basha wyswietla nazwę i pojawienie sie  wybranego stringu w plikach *.cc, *.py ....
finds2() {

	#find . -type f \( -name "*.cc" -o  -name "*.h" \) -exec grep   $1 {} \;
	find . -type f \( -name "*.py" \) -exec grep  --with-filename  $1 {} \; # TYLKO *.py

					CAłóść około 100 KB kodu w pytonie
					
					
					
Po dodaniu NOWYCH plikow bezposrednio na serwer robimy "git pull" :
seriot@seriot:~/ryu/ryu/app$ git pull 
remote: Enumerating objects: 8, done.
remote: Counting objects: 100% (8/8), done.
remote: Compressing objects: 100% (7/7), done.
remote: Total 7 (delta 2), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (7/7), done.
From github.com:ppecka1/Seriot
   66a5c8e..8adefff  main       -> origin/main
Updating 66a5c8e..8adefff
Fast-forward
		 SWITCH_jpg.tar | Bin 0 -> 14101504 bytes 
		 testbed6.jpg   | Bin 0 -> 927548 bytes
		 2 files changed, 0 insertions(+), 0 deletions(-)
		 create mode 100644 SWITCH_jpg.tar
		 create mode 100644 testbed6.jpg
sciagamy 2 dodane pliki  SWITCH_jpg.tar i testbed6.jpg

ZLE ustawia porty Rnn i DW !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! - poprawione
