echo "I am $(whoami) $(id)"
DIR=$(dirname $0)
cd $DIR

./fetchcomic.sh $1
./fetchcomic.sh $2
./date.sh
rm -f joinedcomics.png
convert +append dateweather.png $1.png $2.png joinedcomics.png 
#convert +append chargekindleicon.png garfield.png bignate.png comicscharge.png
convert -rotate 90 joinedcomics.png joinedcomics.png
echo "removing unneeded files..."
mv ../Comics/*.png ../Comics/Vault/
mv bignate.png ../Comics/mkindle/"$1$DATE".png
mv garfield.png ../Comics/mkindle/"$2$DATE".png
cp joinedcomics.png ../Comics/"comics$DATE".png
rm Date.png
# send it to the kindle and display it
echo "sending to kindle..."
scp -q joinedcomics.png mkindle:. 2> /dev/null
ssh mkindle "/usr/sbin/eips -c; sleep 1; /usr/sbin/eips -vg ./joinedcomics.png; sleep 1; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
echo "done"
