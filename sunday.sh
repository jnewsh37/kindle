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
	-resize 530x800 \
	$COMIC.png
convert +append -gravity center Date2.png $COMIC.png joinedcomics.png 
convert j
rm $COMIC.png
rm Date2.png
# send it to the kindle and display it
echo "sending to kindle..."
scp -q joinedcomics.png kindle:. 2> /dev/null
ssh kindle "/usr/sbin/eips -c; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
echo "done"
