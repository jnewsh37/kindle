echo "I am $(whoami) $(id)"
DIR=$(dirname $0)
DATE=$(date +'%Y.%m.%d')
KINDLE=$3
cd $DIR

./fetchcomic.sh $1
./fetchcomic.sh $2
./date.sh
rm -f joinedcomics.png
convert +append dateweather.png $1.png $2.png joinedcomics.png
#convert +append chargekindleicon.png garfield.png bignate.png comicscharge.png
convert -rotate 90 joinedcomics.png joinedcomics.png
echo "saving comics to disk..."
mv ../Comics/kindle/*.png ../Comics/kindle/Vault/
mv $1.png ../Comics/kindle/"$1$DATE".png
mv $2.png ../Comics/kindle/"$2$DATE".png
cp joinedcomics.png ../Comics/kindle/"comics$DATE".png
rm Date.png
# send it to the kindle and display it
echo "sending to kindle..."
scp -q joinedcomics.png $KINDLE:. 2> /dev/null
ssh $KINDLE "/usr/sbin/eips -c; sleep 1; /usr/sbin/eips -vg ./joinedcomics.png; sleep 1; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
echo "done"
