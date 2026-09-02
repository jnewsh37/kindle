cd `dirname $0`
message="$(echo $1|cut  -c 1-125)"
convert -background white \
        -fill black  \
        -font Palatino-Bold \
        -pointsize 36 \
        -size 700x147 \
        -gravity Center \
        caption:" $message" \
        -define png:color-type=0 \
        -define png:bit-depth=8 \
        messagetext.png
#echo $2
convert +append ./"${2}.png" messagetext.png messagetext.png
scp -q messagetext.png kindle:. 2> /dev/null
ssh kindle "/usr/sbin/eips -g ./messagetext.png" 2> /dev/null
#624x147
#176x147

