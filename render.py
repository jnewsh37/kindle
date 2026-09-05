#! /usr/bin/python3
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta

# Planning out the basics of how calendar data will be rendered before using Google's APIs to get real info

d = datetime.now()
events = [("Morning breakfast"), ("Basketball workout")]
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 1)

def fontSize(size):
    global font
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)

def render(saveName):
    event = events[0]
    screen = Image.new("L", (800,600), 255)
    draw = ImageDraw.Draw(screen)

    fontSize(25)
    for i in range(4):
        renderDate = d + timedelta(days=1+i)
        renderDate = renderDate.strftime("%d")
        yCoord = i*(800/4) + 800/4
        draw.line((yCoord, 300, yCoord, 600), fill=0, width=3)
        r = 30
        draw.ellipse(((yCoord-(800/8)-r, 310, (yCoord-(800/8)+r), 310+2*r)), fill=0)
        draw.text((yCoord-(800/8), 310+r),str(renderDate), fill=255, font=font, align="center", anchor="mm")
#        print(i*(800/4) + 800/4)
    fontSize(20)
    draw.line((400, 300, 400, 315), fill=255, width=3)
    draw.text((400, 300), "Upcoming: ", font=font, fill=0, aligh="center", anchor="mm")
    draw.line((0, 300, 325, 300), fill=0, width=3)
    draw.line((475, 300, 800, 300), fill=0, width=3)
    print("yahoods mad")
    screen.save(saveName)

render("testrender.png")