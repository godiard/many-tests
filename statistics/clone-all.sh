for LINE in `cat ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
	REPO=`echo $LINE | awk -F '|' '{printf("%s",$2)}'`
    echo $ACTIVITY
    if [ -d $ACTIVITY/mainline/.git/ ]; then
    	cd $ACTIVITY/mainline
        git pull
        cd ..
    else
    	echo $ACTIVITY
	    mkdir $ACTIVITY
    	cd $ACTIVITY
	    git clone $REPO
    fi
	cd ..
done
