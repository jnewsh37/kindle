DATE=$(date +'%m/%d/%Y')
convert -size 800x70 xc:transparent \
	-font Palatino-Bold \
	-pointsize 80 \
	-fill black \
	-draw "text 215,62.5 '${DATE}'" \
	date.png

convert date.png \
	-rotate 270 \
	-background "#FFFFFF" \
	-flatten \
        Date2.png

rm date.png
