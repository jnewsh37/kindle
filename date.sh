DATE=$(date +'%m/%d/%Y')
convert -size 800x147 xc:transparent \
	-font Palatino-Bold \
	-pointsize 150 \
	-fill black \
	-draw "text 55,125 '${DATE}'" \
	date.png

convert date.png \
        -rotate 270 \
	-background "#FFFFFF" \
	-flatten \
        Date.png

rm date.png
