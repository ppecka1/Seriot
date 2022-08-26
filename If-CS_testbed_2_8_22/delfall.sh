#kasuje flowy na wszystkich hostach
echo "kasuje flowy na wszystkich hostach"
ssh seriot1 sudo ovs-ofctl del-flows br0
ssh seriot2 sudo ovs-ofctl del-flows br0
ssh seriot3 sudo ovs-ofctl del-flows br0
ssh seriot4 sudo ovs-ofctl del-flows br0
ssh seriot5 sudo ovs-ofctl del-flows br0
ssh seriot6 sudo ovs-ofctl del-flows br0


