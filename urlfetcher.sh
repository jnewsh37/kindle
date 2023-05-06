wget -O source https://www.gocomics.com/bignate/$(date +'%Y/%m/%d')
var=$(cat source|grep -m 1 'content="https://assets.amuniversal.com/')
var=${var:35}
var=$(echo $var|cut -c 1-63)
echo $var
wget -O comic $var
rm source
convert comic -rotate 270 -filter LanczosSharp -resize 600x800 -background white -gravity center -colorspace Gray -dither FloydSteinberg -quality 75 -define png:color-type=0 -define png:bit-depth=8 convertedcomic.png 
rm comic
python3 -m http.server
