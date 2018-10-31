#!/bin/bash



PORT="8880"
PID=$$
CONTENT="index.html"
HEADER="HTTP/1.1 200 Ok\r\n"
HEADER2="Content-type: text\n"
HOST="$(hostname -I)"
HOSTINFO="$(uname -a)"

function cput()
{
	echo $(bc -l <<< "scale=3; $(cat /sys/class/thermal/thermal_zone0/temp)/1000")
}



for arg in $@
do
	if [[ $arg == "kill" ]]
	then
		PIDS=$(ps -ef | grep netcat_server | tr -s " " | head -n -1 | cut -d " " -f 2)
		for pid in $PIDS
		do
			if [[ $pid  != "" ]]
			then
				child_pid=$(ps -ef | grep netcat | head -n -1 | tr -s " " | cut -d " " -f2,3 | grep -E "[0-9]{4} $pid" | cut -d " " -f1)
				kill -9 $pid
				kill -9 $child_pid
				echo -e "NETCAT SERVER [PID: $pid] KILLED WITH CHILD [CHILD_PID: $child_pid]"
			fi
		done
	exit
	fi
	echo $arg
done


echo -e "NETCAT SERVER"
echo -e "PID:\t$PID"
echo -e "PPID:\t$PPID"
echo -e "DATA FILE:\t$CONTENT"
echo -e "LOCAL ADDRESS:\t$HOST:$PORT"

while false
do
	:
done


#echo > $CONTENT

#HEADER_0="HTTP/1.1 200 OK\r\n"
#HEADER_1="Content-type: text\n"
#HEADER_2=""

#echo -e "<!DOCTYPE HTML>\n" > $CONTENT
#echo -e "<html>\n" >> $CONTENT
#echo > $CONTENT
#echo -e "<h1>$(date)</h1><br>" >> $CONTENT
#echo >> $CONTENT
#echo -e "<h1>HOST INFO:</h1><br>\n\t<h1>$HOSTINFO</h1><br>" >> $CONTENT
#echo >> $CONTENT
#echo -e "<h1>HOST ADDRESS:</h1><br>\n\t<h1>$HOST</h1><br>" >> $CONTENT
#echo >> $CONTENT
#echo -e "<h1>CPU TEMPERATURE:</h1><br>\n\t<h1>$(cput)</h1><br>\n" >> $CONTENT
#echo >> $CONTENT
#echo -e "\n</html>" >> $CONTENT


#while true
#do
#
#	{ echo -e $HEADER; echo -e $HEADER2; cat $CONTENT; } | netcat -lp $PORT
#	{ echo -e $HEADER_0; echo -e $HEADER_1; echo -e $HEADER_2; cat $CONTENT; } | netcat -lp $PORT
#
#	echo -e "<!DOCTYPE HTML>\n" > $CONTENT
#	echo -e "<html>\n" >> $CONTENT
#	echo > $CONTENT
#	echo -e "<h1>$(date)</h1><br>" >> $CONTENT
#	echo >> $CONTENT
#	echo -e "<h1>HOST INFO:</h1><br>\n\t<h1>$HOSTINFO</h1><br>" >> $CONTENT
#	echo >> $CONTENT
#	echo -e "<h1>HOST ADDRESS:</h1><br>\n\t<h1>$HOST</h1><br>" >> $CONTENT
#	echo >> $CONTENT
#	echo -e "<h1>CPU TEMPERATURE:</h1><br>\n\t<h1>$(cput)</h1><br>\n" >> $CONTENT
#	echo >> $CONTENT
#	echo -e "\n</html>" >> $CONTENT
#
#	printf 'HTTP/1.1 200 OK\n\n%s' "$(cat $CONTENT)" | netcat -l $PORT
#
#done

echo -e "<!DOCTYPE HTML>\n" > $CONTENT
echo -e "<html>\n" >> $CONTENT
echo > $CONTENT
echo -e "<h1>$(date)</h1><br>" >> $CONTENT
echo >> $CONTENT
echo -e "<h1>HOST INFO:</h1><br>\n\t<h1>$HOSTINFO</h1><br>" >> $CONTENT
echo >> $CONTENT
echo -e "<h1>HOST ADDRESS:</h1><br>\n\t<h1>$HOST</h1><br>" >> $CONTENT
echo >> $CONTENT
echo -e "<h1>CPU TEMPERATURE:</h1><br>\n\t<h1>$(cput)</h1><br>\n" >> $CONTENT
echo >> $CONTENT
echo -e "\n</html>" >> $CONTENT

printf 'HTTP/1.1 200 OK\n\n%s' "$(cat $CONTENT)" | netcat -l $PORT

