#! /usr/bin/bash

ffmpeg -i $1 -i $2 -r 7.7 -filter_complex "[0:v]transpose=1,transpose=1,scale=-1:600,pad=800:600:0:0[bg];[1:v]transpose=1,transpose=1[img];[bg][img] overlay=338:0:enable='between(t,0,10000)'" -pix_fmt gray -f rawvideo Clip.raw
cat Clip.raw | $3 > Clip.gmv