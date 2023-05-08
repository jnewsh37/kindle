./fetchcomic.sh
./datesunday.sh
rm joinedcomics.png
convert bignate.png \
	-resize 530x800 \
	bignate.png
convert +append -gravity center Date2.png bignate.png joinedcomics.png 
rm bignate.png
rm Date2.png
# send it to the kindle and display it
echo "sending to kindle..."
scp -q joinedcomics.png kindle:. 2> /dev/null
ssh kindle "/usr/sbin/eips -c; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
echo "done"
