message=$(echo $1|cut  -c 1-100)
convert -background white \
        -fill black  \
        -font Palatino-Bold \
        -pointsize 36 \
        -size 624x147 \
        caption:" $message" \
        messagetext.png

