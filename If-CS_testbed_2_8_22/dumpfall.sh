echo "Wyswietla flowy na wszystkich hostach"
ssh seriot1 sudo ovs-ofctl dump-flows br0
ssh seriot2 sudo ovs-ofctl dump-flows br0
ssh seriot3 sudo ovs-ofctl dump-flows br0
ssh seriot4 sudo ovs-ofctl dump-flows br0
ssh seriot5 sudo ovs-ofctl dump-flows br0
ssh seriot6 sudo ovs-ofctl dump-flows br0


