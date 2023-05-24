DATE=$(date +'%m/%d/%Y')
#gets the icon for the current weather and resizes it
./weather-icon.py
convert weather-icon.svg \
	-rotate 270 \
	-resize 147x200 \
	weather-icon.png
rm weather-icon.svg

convert -size 642x147 xc:transparent \
	-font Palatino-Bold \
	-pointsize 130 \
	-fill black \
	-draw "text 35,115 '${DATE}'" \
	date.png

convert date.png \
        -rotate 270 \
	-background "#FFFFFF" \
	-flatten \
        Date.png
convert -append Date.png weather-icon.png dateweather.png
rm date.png
