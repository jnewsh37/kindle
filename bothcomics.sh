cd /home/jack/src/kindle/
./fetchcomic.sh
./fetchcomic.sh -g
./date.sh
rm joinedcomics.png
convert +append Date.png garfield.png bignate.png joinedcomics.png 
echo "removing unneeded files..."
rm bignate.png
rm garfield.png
rm Date.png
# send it to the kindle and display it
echo "sending to kindle..."
scp -q joinedcomics.png kindle:. 2> /dev/null
ssh kindle "/usr/sbin/eips -c; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
echo "done"
