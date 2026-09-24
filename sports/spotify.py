#! /usr/bin/env python3

import sys, syncedlyrics, subprocess, spotipy, time
from spotipy.oauth2 import SpotifyOAuth, SpotifyPKCE
from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta, datetime
from basketball import runCommand

scope = "user-read-currently-playing"
redirect = "http://127.0.0.1:8888/callback"

# Creates a spotipy.Spotify client
def create_spotify_client(id, secret) -> spotipy.Spotify:
    ("Authenticating using OAuth")
    auth_manager = SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri=redirect, scope=scope)

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

def pullLyrics(name, artist):
     return str(syncedlyrics.search(f"[{artist}] [{name}]")).split("\n")

def getLyrics(lyrics, position, parsed=False):
    print(len(lyrics))
    print(lyrics[0])
    lyricsToEnd = []
    delta = -1
    if not parsed and lyrics[0] != 'None':
        lyricsList = lyrics
        while ":" not in lyricsList[-1]:
            print(lyricsList.pop(-1))
        lyricsDict = {}
        for l in lyricsList:
            lyricsDict[str(l)[1:9]] = str(l)[11:(len(l))]   
        times = list(lyricsDict.keys())
        lPos = ""
        for t in times:
            tList = t.split(":")
            newT = (int(tList[0])*60 + int(float(tList[1])))*1000
            if (abs(newT-position)<delta or delta == -1):
                line = lyricsDict[t]
                delta = abs(newT-position)
                lPos = t
        for l in times[times.index(lPos):]:
            lyricsToEnd.append(lyricsDict[l])

    if (delta >= 0 and len(lyricsToEnd) > 1):
        return(lyricsToEnd)
    else:
        print("returning filler")
        lyricsToEnd = ["***", "***"]  
        return lyricsToEnd

def splitLines(line, maxLen):
    lineList = []
    while len(line) > maxLen:
        i = line.rfind(" ", 0, maxLen)
        lineList.append(line[0:i])
        line = line[i+1:]
    lineList.append(line)
    return "\n".join(lineList)

def renderPlaying(client:spotipy.Spotify, lyrics, name, artists, coverURL, cover, progress, length):
        runCommand("curl", coverURL, "--output", cover)
        lyricsList = getLyrics(lyrics, progress)
        lyricsList = [splitLines(l, 30) for l in lyricsList]
        screen = Image.new("L", (800,600), 255)
        draw = ImageDraw.Draw(screen)
        imgSize = 150
        pasteImage(50, 50, imgSize, screen, cover)
        fontSize(30)
        draw.text((100+imgSize, 100), name,font=font)
        fontSize(20)
        draw.text((100+imgSize, 150), ", ".join(artists),font=font)

        fontSize(50)
        draw.text((50, 80+imgSize), lyricsList[0], font=font)
        draw.text((50, 130+50*lyricsList[0].count("\n")+imgSize), lyricsList[1], fill=150, font=font)

    # Progress bar
        draw.line((150, 550, 700, 550), fill=100, width=10)
        draw.line((150, 550, 150+(progress/length*550), 550), fill=0, width=10)
        fontSize(25)
        draw.text((110, 550), ((str(timedelta(milliseconds=progress))[2:7])), font=font, align="center", anchor="mm")

        screen.save("SpotifyTest.png")
        print(f"Song: {name}\nArtists: {artists}\nCover image URL: {coverURL}\nProgress: {int(progress/60000)}:{int((progress%60000)/1000)}\nCurrent lyrics: {lyricsList[0]}")

if __name__ == "__main__":
    client = create_spotify_client(sys.argv[1], sys.argv[2])
    ip = sys.argv[3]
    data = client.currently_playing()
    currentName = ""
    count=0
    if data != None:
        while True:
            name = data["item"]["name"]
            data = client.currently_playing()
            progress = data["progress_ms"]
            if currentName != name:
                artists = []
                for artist in data["item"]["artists"]:
                    artists.append(artist["name"])
                progress = data["progress_ms"]
                length = data["item"]["duration_ms"]
                coverURL = str(data["item"]["album"]["images"][0]["url"])
                cover = (coverURL.split("/"))[-1] + ".jpeg"
                lyrics = pullLyrics(name, artists[0])
            currentName = name
            renderPlaying(client, lyrics, name, artists, coverURL, cover, progress, length)
            runCommand("scp", "SpotifyTest.png", f"{ip}:~/")
            if count%20 == 0:
                runCommand("ssh", ip, "/usr/sbin/eips -fg ~/SpotifyTest.png")
            else:
                runCommand("ssh", ip, "/usr/sbin/eips -g ~/SpotifyTest.png")
            count+=1
            time.sleep(2)
