./newfetch.sh
./newfetch.sh -g
./date.sh
rm joinedcomics.png
convert -gravity center -append Date2.png garfield.png bignate.png joinedcomics.png 

# send it to the kindle and display it
scp -q joinedcomics.png kindle:. 2> /dev/null
ssh kindle "/usr/sbin/eips -c; /usr/sbin/eips -g ./joinedcomics.png" 2> /dev/null
