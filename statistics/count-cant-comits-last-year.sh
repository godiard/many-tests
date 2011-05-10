for LINE in `cat ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
	cd $ACTIVITY
    if [ -d mainline ]; then
        cd mainline
        CANT_COMMITS=`git log --oneline --since=05-03-2010 | grep -v Pootle | grep -v "Translation System" | wc -l`
        echo $CANT_COMMITS $ACTIVITY
        cd ..
        echo $CANT_COMMITS > commits_last_year.txt
    fi
    cd ..
done


