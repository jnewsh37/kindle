#!/bin/bash
#
# push a file to the kindle and show it.
#

if [ $# -ne 1 ] ; then
	echo "usage: $0 filename"
	exit 1
fi
FN=$1

# send it to the kindle and display it
scp -q $FN kindle:showme.png 2> /dev/null
ssh kindle "/usr/sbin/eips -c; /usr/sbin/eips -g ./showme.png" 2> /dev/null
