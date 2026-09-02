#!/bin/bash
#
# Script for fetching today's bignate and pushing it to
# the kindle.
#

COMIC=bignate
COMIC=$1
DATE=$(date +'%Y/%m/%d')
comicurl=https://www.gocomics.com/$COMIC/$DATE

# fetch comic page and get the URL for the image
echo "fetching $comicurl"
wget -q -O source $comicurl
var=$(cat source|grep -m 1 'content="https://featureassets.gocomics.com/assets/')
imgurl=$(echo $var|cut -c 6135-6208)

# fetch the comic image
echo "fetching $imgurl"
wget -q -O comic.png $imgurl
rm source

# convert the picture to a format that the kindle likes best
convert comic.png \
	-filter LanczosSharp \
	-resize 800x800 \
	-background white \
	-gravity center \
	-colorspace Gray \
	-dither FloydSteinberg \
	-quality 75 \
	-define png:color-type=0 \
	-define png:bit-depth=8 \
	$COMIC.png 
rm comic.png
