for LINE in `cat ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
	cd $ACTIVITY
    CANT_COMMITS=`cat commits_last_year.txt`
    CANT_BUGS=`cat total_bugs.txt`
    cd ..
    echo $CANT_BUGS $CANT_COMMITS $ACTIVITY >> commit-bugs.dat
done


