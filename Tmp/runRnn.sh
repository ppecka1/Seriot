while true
do
	echo "**Rnn Restart **." >>/dev/stderr
	java org.iitis.InformationFeeder topo6.json pipe >/dev/null
	
done
