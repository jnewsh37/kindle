DIR=$(dirname $0)
cd $DIR
COMIC=bignate
if [ "x$1" = "x-b" ] ; then
        COMIC=bignate
fi
if [ "x$1" = "x-g" ] ; then
        COMIC=garfield
fi
./fetchcomic.sh $1
./datesunday.sh
rm joinedcomics.png
convert $COMIC.png \
	-resize 800x453 \
	$COMIC.png
convert +append -gravity center Date2.png $COMIC.png joinedcomics.png 
COMIC=bignate
convert -rotate 90 joinedcomics.png joinedcomics.png
convert $COMIC.png -rotate 90 -resize 800x453 alt.png
convert -append -gravity center blankstrip.png alt.png alt.png
rm $COMIC.png
rm Date2.png
# send it to the kindle and display it
echo "sending to kindle..."
scp -q joinedcomics.png kindle:. 2> /dev/null
scp -q alt.png kindle:. 2> /dev/null
ssh kindle "/usr/sbin/eips -c; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
echo "done"
