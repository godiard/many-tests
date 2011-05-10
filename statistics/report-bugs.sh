for LINE in `cat ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
    CANT_BUGS_BSO="-"
    CANT=0
	cd $ACTIVITY
    if [ -f $ACTIVITY-bugs-bso.csv ]; then
        CANT_BUGS_BSO=`tail -n +1 $ACTIVITY-bugs-bso.csv | wc -l | awk '{printf("%s", $1)}'`
        CANT=$CANT_BUGS_BSO
    fi

    CANT_BUGS_DLO="-"
    if [ -f $ACTIVITY-bugs-dlo.csv ]; then
        CANT_BUGS_DLO=`tail -n +1 $ACTIVITY-bugs-dlo.csv | wc -l | awk '{printf("%s", $1)}'` 
        CANT=`echo "$CANT + $CANT_BUGS_DLO" | bc` 
    fi

    echo $CANT $ACTIVITY $CANT_BUGS_BSO $CANT_BUGS_DLO
    echo $CANT > total_bugs.txt
    cd ..
done
