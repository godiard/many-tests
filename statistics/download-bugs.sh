for LINE in `cat ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
	BSO_COMPONENT=`echo $LINE | awk -F '|' '{printf("%s",$3)}'`
	DLO_COMPONENT=`echo $LINE | awk -F '|' '{printf("%s",$4)}'`
    echo $ACTIVITY
    mkdir -p $ACTIVITY
	cd $ACTIVITY
    if [ -n "$BSO_COMPONENT" ]; then
        if [ ! -f $ACTIVITY-bugs-bso.csv ]; then
            URL_BSO="http://bugs.sugarlabs.org/query?status=accepted&status=assigned&status=new&status=reopened&format=csv&component=$BSO_COMPONENT&order=priority&col=id&col=summary&col=priority&col=status&col=owner&col=type&col=milestone"
            wget -O $ACTIVITY-bugs-bso.csv $URL_BSO
        fi
    fi

    if [ -n "$DLO_COMPONENT" ]; then
        if [ ! -f $ACTIVITY-bugs-dlo.csv ]; then
            URL_DLO="http://dev.laptop.org/query?status=assigned&status=new&status=reopened&format=csv&component=$DLO_COMPONENT&order=priority&col=id&col=summary&col=status&col=owner&col=type&col=milestone"
            wget -O $ACTIVITY-bugs-dlo.csv $URL_DLO 
        fi
    fi
    #echo $URL_BSO
    #echo $URL_DLO
    cd ..
done
