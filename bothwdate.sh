echo "I am $(whoami) $(id)"
DIR=$(dirname $0)
cd $DIR

./getcomic.sh -b $1
./getcomic.sh -g $1
./choosedate.sh $1
rm -f joinedcomics.png
convert +append garfield.png bignate.png Date.png joinedcomics.png 
echo "removing unneeded files..."
rm bignate.png
rm garfield.png
rm Date.png
# send it to the kindle and display it
echo "sending to kindle..."
scp -q joinedcomics.png kindle:. 2> /dev/null
ssh kindle "/usr/sbin/eips -c; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
echo "done"
