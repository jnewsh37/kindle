#!/bin/bash
#
# Script for fetching today's bignate and pushing it to
# the kindle.
#

COMIC=bignate
if [ "x$1" = "x-b" ] ; then
	COMIC=bignate
fi
if [ "x$1" = "x-g" ] ; then
	COMIC=garfield
fi

DATE=$(date +'%Y/%m/%d')
comicurl=https://www.gocomics.com/$COMIC/$DATE
# fetch comic page and get the URL for the image
echo "fetching $comicurl"
wget -q -O source $comicurl
var=$(cat source|grep -m 1 'content="https://assets.amuniversal.com/')
var=${var:35}
imgurl=$(echo $var|cut -c 1-63)

# fetch the comic image
echo "fetching $imgurl"
wget -q -O comic.png $imgurl
rm source

# convert the picture to a format that the kindle likes best
convert comic.png \
	-rotate 270 \
	-filter LanczosSharp \
	-resize 600x800 \
	-background white \
	-gravity center \
	-colorspace Gray \
	-dither FloydSteinberg \
	-quality 75 \
	-define png:color-type=0 \
	-define png:bit-depth=8 \
	convertedcomic.png 
rm comic.png
