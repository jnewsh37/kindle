DATE=$(date +'%m/%d/%Y')

DIR=$(dirname $0)
cd $DIR

#gets the icon for the current weather and resizes it

python3 weather-icon.py

convert weather-icon.svg \
	-rotate 270 \
	-resize 119x200 \
        -define png:color-type=0 \
        -define png:bit-depth=8 \
	weather-icon.png

rm weather-icon.svg

convert -size 642x119 xc:transparent \
	-font Palatino-Bold \
	-pointsize 130 \
	-fill black \
	-draw "text 25,100 '${DATE}'" \
	date.png

convert date.png \
        -rotate 270 \
	-background "#FFFFFF" \
	-flatten \
        Date.png

convert -append Date.png weather-icon.png dateweather.png
rm date.png
rm weather-icon.png
