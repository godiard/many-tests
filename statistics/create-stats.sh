for LINE in `cat ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
	cd $ACTIVITY
    ../git-stats/gitstats/gitstats mainline/ STATS
    cd ..
done
