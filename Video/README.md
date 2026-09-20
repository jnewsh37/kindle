Geekmaster (legend in the Kindle jailbreaking community, RIP) wrote all of the programs and the instructions I followed, this is a condensed version
Video player post: https://www.mobileread.com/forums/showthread.php?t=177455
Transcoder+ditherer post: https://www.mobileread.com/forums/showthread.php?p=2074379#post2074379

How to convert videos to geekmaster's player's format:
Run "ffmpeg -i input.mp4 -r 7.7 -s 800x600 -pix_fmt gray -vf "transpose=1,transpose=1" -f rawvideo output" to convert input to the raw format geekmaster's gmv program accepts
Pipe raw video into compiled gmv file and redirect output to a file

How to play:
Copy video to your kindle and pipe into gmplay (install from mobileread forum)
