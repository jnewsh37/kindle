message=$(echo $1|cut  -c 1-100)
convert -background white \
        -fill black  \
        -font Palatino-Bold \
        -pointsize 36 \
        -size 624x147 \
        caption:" $message" \
	-rotate 270 \
        messagetext.png

