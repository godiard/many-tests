INDEX_FILE="./bugs_index.html"

echo "<html>" > $INDEX_FILE
echo "<head>
<style type="text/css">
body {
background-color:#d0e4fe;
font-family:"Arial";
font-size:10px;
}

p {
font-size:14px;
color:orange;
}

th {
background-color:grey;
color:orange;
text-align:center;
}

td {
background-color:white;
}
</style>
</head>" > $INDEX_FILE
echo "<body>" >> $INDEX_FILE

for LINE in `cat ./query-links.txt`
do
	LABEL=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
	URL=`echo $LINE | awk -F '|' '{printf("%s",$2)}'`
    	echo "<p><a href='$URL' target='_blank'>$LABEL</a></p>" >> $INDEX_FILE
done

echo "<table>" >> $INDEX_FILE
echo "<tr><th>Actividad</th><th>Bugs en Sugarlabs</th><th>Bugs en OLPC</th></tr>" >> $INDEX_FILE

for LINE in `cat ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
	BSO_COMPONENT=`echo $LINE | awk -F '|' '{printf("%s",$3)}'`
	DLO_COMPONENT=`echo $LINE | awk -F '|' '{printf("%s",$4)}'`
    	echo "<tr><td>$ACTIVITY</td><td>" >> $INDEX_FILE
    	if [ -n "$BSO_COMPONENT" ]; then
            	URL_BSO="http://bugs.sugarlabs.org/query?status=accepted&status=assigned&status=new&status=reopened&component=$BSO_COMPONENT&order=priority&col=id&col=summary&col=priority&col=status&col=owner&col=type&col=milestone"	
    		echo "<a href='$URL_BSO' target='_blank'>$BSO_COMPONENT</a>" >> $INDEX_FILE
        fi
	echo "</td><td>" >> $INDEX_FILE
	if [ -n "$DLO_COMPONENT" ]; then
            	URL_DLO="http://dev.laptop.org/query?status=assigned&status=new&status=reopened&component=$DLO_COMPONENT&order=priority&col=id&col=summary&col=status&col=owner&col=type&col=milestone"
    		echo "<a href='$URL_DLO' target='_blank'>$DLO_COMPONENT</a>" >> $INDEX_FILE
        fi
	echo "</td></tr>" >> $INDEX_FILE
done

echo "</table>" >> $INDEX_FILE
echo "</body></html>" >> $INDEX_FILE
