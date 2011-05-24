for LINE in `grep -v ^# ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
	GIT=`echo $LINE | awk -F '|' '{printf("%s",$5)}'`
	REPO=`echo $LINE | awk -F '|' '{printf("%s",$2)}'`

    echo $ACTIVITY
	cd $ACTIVITY

    if [ -d $GIT.git/ ]; then
    	cd $GIT
        git pull
        CANT_COMMITS=`git log --oneline --since=05-03-2010 | grep -v Pootle | grep -v "Translation System" | wc -l`
        echo $CANT_COMMITS $ACTIVITY
        cd ..
        echo $CANT_COMMITS > commits_last_year.txt
    fi

	BSO_COMPONENT=`echo $LINE | awk -F '|' '{printf("%s",$3)}'`
	DLO_COMPONENT=`echo $LINE | awk -F '|' '{printf("%s",$4)}'`
    CANT=0
    if [ -n "$BSO_COMPONENT" ]; then
        URL_BSO="http://bugs.sugarlabs.org/query?status=accepted&status=assigned&status=new&status=reopened&format=csv&component=$BSO_COMPONENT&order=priority&col=id&col=summary&col=priority&col=status&col=owner&col=type&col=milestone"
        rm $ACTIVITY-bugs-bso.csv
        wget -O $ACTIVITY-bugs-bso.csv $URL_BSO
        CANT_BUGS_BSO=`tail -n +1 $ACTIVITY-bugs-bso.csv | wc -l | awk '{printf("%s", $1)}'`
        CANT=$CANT_BUGS_BSO
    fi

    if [ -n "$DLO_COMPONENT" ]; then
        URL_DLO="http://dev.laptop.org/query?status=assigned&status=new&status=reopened&format=csv&component=$DLO_COMPONENT&order=priority&col=id&col=summary&col=status&col=owner&col=type&col=milestone"
        rm $ACTIVITY-bugs-dlo.csv
        wget -O $ACTIVITY-bugs-dlo.csv $URL_DLO 
        CANT_BUGS_DLO=`tail -n +1 $ACTIVITY-bugs-dlo.csv | wc -l | awk '{printf("%s", $1)}'` 
        CANT=`echo "$CANT + $CANT_BUGS_DLO" | bc` 
    fi
    echo $CANT > total_bugs.txt

	cd ..
    echo $CANT $CANT_COMMITS $ACTIVITY >> commit-bugs.dat
done

gnuplot  < commit-bugs.gnp
