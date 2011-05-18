for LINE in `grep -v ^# ./activities-data.txt`
do
	ACTIVITY=`echo $LINE | awk -F '|' '{printf("%s",$1)}'`
	GIT=`echo $LINE | awk -F '|' '{printf("%s",$5)}'`
	REPO=`echo $LINE | awk -F '|' '{printf("%s",$2)}'`

    echo $ACTIVITY
    if [ -d $ACTIVITY/$GIT.git/ ]; then
    	cd $ACTIVITY/$GIT
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
