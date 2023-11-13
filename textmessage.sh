message=$(echo $1|cut  -c 1-100)
convert -background white \
        -fill black  \
        -font Palatino-Bold \
        -pointsize 36 \
        -size 624x147 \
	-gravity Center \
        caption:" $message" \
        messagetext.png

scp -q messagetext.png kindle:. 2> /dev/null
ssh kindle "/usr/sbin/eips -g ./messagetext.png" 2> /dev/null
