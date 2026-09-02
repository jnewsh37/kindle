DATE=$(date +'%m/%d/%Y')

DIR=$(dirname $0)
cd $DIR

#gets the icon for the current weather and resizes it

python3 weather-icon.py

convert weather-icon.svg \
	-resize 158x$1 \
        -define png:color-type=0 \
        -define png:bit-depth=8 \
	weather-icon.png

rm weather-icon.svg

convert -size 642x$1 xc:transparent \
	-font Palatino-Bold \
	-pointsize 130 \
	-fill black \
	-draw "text 25,115 '${DATE}'" \
	date.png

convert date.png \
	-background "#FFFFFF" \
	-flatten \
        Date.png

convert +append weather-icon.png Date.png dateweather.png
rm date.png
#rm weather-icon.png
