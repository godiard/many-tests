for LINE in `cat ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
    echo $ACTIVITY
    if [ -d $ACTIVITY/mainline/.git/ ]; then
    	cd $ACTIVITY/mainline
        LAST_COMMIT=`git log --oneline | grep -v Pootle | grep -v "Translation System" | head -1 | awk '{printf("%s", $1)}'`
        AUTHOR=`git show $LAST_COMMIT | head -3 | grep "Author"`
        DATE_LAST_COMMIT=`git show $LAST_COMMIT | head -3 | grep "Date"`
        echo $ACTIVITY $DATE_LAST_COMMIT $AUTHOR
        cd ../..
    fi
done
