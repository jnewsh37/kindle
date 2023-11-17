pic=$1
name=$2
#110x147
#make padding

#format pic
convert $1 \
        -filter LanczosSharp \
        -background white \
        -gravity center \
        -colorspace Gray \
        -dither FloydSteinberg \
        -quality 75 \
        -define png:color-type=0 \
        -define png:bit-depth=8 \
        pfpic.png

convert pfpic.png -resize 95x95 pfpic.png

#format name
convert -background white \
        -fill black  \
        -font Palatino-Bold \
        -pointsize 19 \
        -size 100x52 \
        -gravity Center \
        caption:" $name" \
        name.png
	
convert \
	-background white \
	-append \
	-gravity Center \
	pfpic.png name.png \
        -filter LanczosSharp \
        -background white \
        -colorspace Gray \
        -define png:color-type=0 \
        -define png:bit-depth=8 \
	$3.png

#convert -resize 111x147 $3.png $3.png
#remove padding
#rm padding1.png
#rm paddding2.png
