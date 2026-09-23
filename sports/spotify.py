#! /usr/bin/env python3

import sys, syncedlyrics, subprocess, spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyPKCE
from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta, datetime
from basketball import runCommand

SCOPE = "user-read-currently-playing"
redirect = "http://127.0.0.1:8888/callback"

# Creates a spotipy.Spotify
def create_spotify_client(scope = SCOPE) -> spotipy.Spotify:
    ("Authenticating using OAuth")
    auth_manager = SpotifyOAuth(client_id=sys.argv[1], client_secret=sys.argv[2], redirect_uri=redirect, scope=scope)

    auth_manager.get_cached_token()

    client = spotipy.Spotify(auth_manager=auth_manager)

    return client

def pasteImage(x, y, size, cvs, url):
    with Image.open(url) as img:
        print(img)
        img = img.resize((size,size))
        cvs.paste(img, (x, y))

font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 1)
def fontSize(f):
	global font
	font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", f)

def pullLyrics(name, artist) -> list:
     return str(syncedlyrics.search(f"[{artist}] [{name}]")).split("\n")

def getLyrics(lyrics, position, offset=None, parsed=False):
    if not parsed:
        lyricsList = lyrics
        while ":" not in lyricsList[-1]:
            print(lyricsList.pop(-1))
        lyricsDict = {}
        for l in lyricsList:
            lyricsDict[str(l)[1:9]] = str(l)[11:(len(l))]   
        times = list(lyricsDict.keys())
        delta = -1
        lPos = ""
    for t in times:
        tList = t.split(":")
        newT = (int(tList[0])*60 + int(float(tList[1])))*1000
        if (abs(newT-position)<delta or delta == -1):
            line = lyricsDict[t]
            delta = abs(newT-position)
            lPos = t

    lyricsToEnd = []

    if (delta >= 0) and not offset:
         if (times.index(lPos) == 0):
            return (line, "***", lyricsDict[times[times.index(lPos)+1]])
         elif (times.index(lPos) == len(times)-1):
              return (line, lyricsDict[times[times.index(lPos)-1]], "***")
         else:
              return (line, lyricsDict[times[times.index(lPos)-1]], lyricsDict[times[times.index(lPos)+1]])
    else:
         return "***"  

def renderPlaying(client:spotipy.Spotify):
    data = client.currently_playing()
    name = data["item"]["name"]
    artists = []
    for artist in data["item"]["artists"]:
        artists.append(artist["name"])
    progress = data["progress_ms"]
    length = data["item"]["duration_ms"]
    coverURL = str(data["item"]["album"]["images"][0]["url"])
    cover = (coverURL.split("/"))[-1] + ".jpeg"
    runCommand("curl", coverURL, "--output", cover)

    lyrics = pullLyrics(name, artists[0])
    currentLine, lastLine, nextLine = getLyrics(lyrics, progress)

    screen = Image.new("L", (800,600), 255)
    draw = ImageDraw.Draw(screen)
    imgSize = 150
    pasteImage(50, 50, imgSize, screen, cover)
    fontSize(30)
    draw.text((100+imgSize, 100), name,font=font)
    fontSize(20)
    draw.text((100+imgSize, 150), ", ".join(artists),font=font)

    if len(currentLine) > 30:
         currentLine = f"{currentLine[0:30]}\n{currentLine[30:len(currentLine)]}"
    fontSize(50)
    draw.text((50, 100+imgSize), currentLine, font=font)
    draw.text((50, 150+50*int(len(currentLine)/34)+imgSize), nextLine, fill=150, font=font)

# Progress bar
    draw.line((150, 550, 700, 550), fill=100, width=10)
    draw.line((150, 550, 150+(progress/length*550), 550), fill=0, width=10)
    fontSize(25)
    draw.text((115, 550), ((str(timedelta(milliseconds=progress))[2:7])), font=font, align="center", anchor="mm")

    screen.save("SpotifyTest.png")
    print(f"Song: {name}\nArtists: {artists}\nCover image URL: {coverURL}\nProgress: {int(progress/60000)}:{int((progress%60000)/1000)}\nCurrent lyrics: {currentLine}")

renderPlaying(create_spotify_client())
runCommand("scp", "SpotifyTest.png", "kindle3:~/")
runCommand("ssh", "kindle3", "/usr/sbin/eips -fg ~/SpotifyTest.png")