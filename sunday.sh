DIR=$(dirname $0)
cd $DIR
COMIC=$1
./fetchcomic.sh $1
./datesunday.sh
rm joinedcomics.png
convert $COMIC.png \
	-resize 530x800 \
	$COMIC.png
convert +append -gravity center Date2.png $COMIC.png joinedcomics.png 
convert -rotate 90 joinedcomics.png joinedcomics.png
#convert $COMIC.png -rotate 90 -resize 800x453 alt.png
#convert -append -gravity center blankstrip.png alt.png alt.png
rm $COMIC.png
rm Date2.png
# send it to the kindle and display it
echo "sending to kindle..."
scp -q joinedcomics.png mkindle:. 2> /dev/null
scp -q alt.png mkindle:. 2> /dev/null
ssh mkindle "/usr/sbin/eips -c; sleep 1; /usr/sbin/eips -vg ./joinedcomics.png; sleep 1; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
echo "done"
