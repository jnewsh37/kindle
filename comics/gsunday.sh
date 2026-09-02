DIR=$(dirname $0)
cd $DIR
./fetchcomic.sh -g
./datesunday.sh
rm joinedcomics.png
convert garfield.png \
	-resize 530x800 \
	garfield.png
convert +append -gravity center Date2.png garfield.png joinedcomics.png 
rm garfield.png
rm Date2.png
# send it to the kindle and display it
echo "sending to kindle..."
scp -q joinedcomics.png kindle:. 2> /dev/null
ssh kindle "/usr/sbin/eips -c; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
echo "done"
