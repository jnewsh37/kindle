DIR=$(dirname $0)
cd $DIR

convert -size 642x147 xc:transparent \
	-font Palatino-Bold \
	-pointsize 130 \
	-fill black \
	-draw "text 25,115 '${1}'" \
	date.png

convert date.png \
        -rotate 270 \
	-background "#FFFFFF" \
	-flatten \
        Date.png
rm date.png
