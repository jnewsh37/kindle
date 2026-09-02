pic=$1
name=$2
#110x147
#make padding

#format pic
magick $1 \
        -filter LanczosSharp \
        -background white \
        -gravity center \
        -colorspace Gray \
        -dither FloydSteinberg \
        -quality 75 \
        -define png:color-type=0 \
        -define png:bit-depth=8 \
        pfpic.png

magick pfpic.png -resize 95x95 pfpic.png

#format name
magick -background white \
        -fill black  \
        -font Palatino-Bold \
        -pointsize 19 \
        -size 100x52 \
        -gravity Center \
        caption:" $name" \
        name.png
	
magick \
	-background white \
        pfpic.png name.png \
	-append \
	-gravity Center \
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
