echo "wyswietla MAC dla wszystkich hostow "
for i in 1 2 3 4 5 6
do
	rsh seriot$i ip a|grep 54:b2 |tail -1|awk '{print $2}'
done

