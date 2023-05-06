DATE=$(date +'%m/%d/%Y')
convert -size 600x70 xc:transparent \
	-font Palatino-Bold \
	-pointsize 80 \
	-fill black \
	-draw "text 115,62.5 '${DATE}'" \
	date.png

convert date.png \
	-background "#FFFFFF" \
	-flatten \
        Date2.png

rm date.png
