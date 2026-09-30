#! /usr/bin/env python3

import sys, syncedlyrics, spotipy, time
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta
from basketball import runCommand

scope = "user-read-currently-playing"
redirect = "http://127.0.0.1:8888/callback"

# Creates a spotipy.Spotify client
def create_spotify_client(id, secret) -> spotipy.Spotify:
    print("Authenticating using OAuth")
    auth_manager = SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri=redirect, scope=scope)
    auth_manager.get_cached_token()
    client = spotipy.Spotify(auth_manager=auth_manager)
    return client

def pasteImage(x, y, size, cvs, url):
    with Image.open(url) as img:
        img = img.resize((size,size))
        cvs.paste(img, (x, y))

font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 1)
def fontSize(f):
	global font
	font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", f)

def pullLyrics(name, artist):
     return str(syncedlyrics.search(f"[{artist}] [{name}]")).split("\n")

def toSeconds(t):
    tList = t.split(":")
    return (int(tList[0])*60 + int(float(tList[1])))

def getLyrics(lyrics, position:timedelta, parsed=False):
    lyricsToEnd = []
    position = position.total_seconds()
    if not parsed and lyrics[0] != 'None':
        lyricsList = lyrics
        while ":" not in lyricsList[-1]:
            print(lyricsList.pop(-1))
        lyricsDict = {}
        for l in lyricsList:
            lyricsDict[str(l)[1:9]] = str(l)[10:(len(l))]   
        times = list(lyricsDict.keys())
        lPos = ""
        delt = 0.0
        for i,t in enumerate(times):
            newT = toSeconds(t)
            if (newT < position):
                lPos = t
                if (i+1 < len(times)):
                    delt = toSeconds(times[i+1]) - newT
        if lPos in times:
            for l in times[times.index(lPos):]:
                lyricsToEnd.append(lyricsDict[l])
        lyricsToEnd.extend(["***", "***"])
    return(lyricsToEnd, delt)


def splitLines(line, maxLen):
    lineList = []
    line = line.strip("]")
    line = line.lstrip(" ")
    while len(line) > maxLen:
        line = line.lstrip(" ")
        line.lstrip("]")
        i = line.rfind(" ", 0, maxLen)
        lineList.append(line[0:i])
        line = line[i+1:]
    lineList.append(line)
    return "\n".join(lineList)

def renderPlaying(client:spotipy.Spotify, lyrics, name, artists, cover, progress:timedelta, delay, length):
        lyricsList, rest = getLyrics(lyrics, progress+delay)
        lyricsList = [splitLines(l, 30) for l in lyricsList]
        progress = progress.total_seconds() * 1000
        screen = Image.new("L", (800,600), 255)
        draw = ImageDraw.Draw(screen)

        # Song info
        imgSize = 150
        pasteImage(50, 50, imgSize, screen, cover)
        fontSize(30)
        draw.text((100+imgSize, 100), name,font=font)
        fontSize(20)
        draw.text((100+imgSize, 150), ", ".join(artists),font=font)

        # Lyrics
        fontSize(50)
        draw.text((50, 80+imgSize), lyricsList[0], font=font)
        if lyricsList[0].count("\n") + lyricsList[1].count("\n") < 5:
            draw.text((50, 130+50*lyricsList[0].count("\n")+imgSize), lyricsList[1], fill=150, font=font)

        # Progress bar
        draw.line((150, 565, 700, 565), fill=100, width=10)
        draw.line((150, 565, 150+(progress/length*550), 565), fill=0, width=10)
        fontSize(25)
        draw.text((110, 565), ((str(timedelta(milliseconds=progress))[2:7])), font=font, align="center", anchor="mm")

        # Saves render + prints current lyrics
        screen.save("render.png")
        print(f"Current lyrics: {lyricsList[0]}")
        return rest

def run():
    client = create_spotify_client(sys.argv[1], sys.argv[2])
    ip = sys.argv[3]
    data = client.currently_playing()
    currentName = ""
    refresh = 0
    delays = []
    avgTime = 0
    delay = timedelta(seconds=0)
    if data != None:
        while True:
            # Clears terminal and refreshes some data (abstains from refreshing lyrics and cover art until necessary since those are slower)
            print("\033[H\033[J", end="")
            name = data["item"]["name"]
            data = client.currently_playing()
            print("Refreshing Spotify API data...")
            progress = timedelta(milliseconds=data["progress_ms"])
            if currentName != name:
                # Refresh Spotify and lyrical data if song name different
                artists = []
                for artist in data["item"]["artists"]:
                    artists.append(artist["name"])
                progress = timedelta(milliseconds=data["progress_ms"])
                length = data["item"]["duration_ms"]
                coverURL = str(data["item"]["album"]["images"][0]["url"])
                cover = (coverURL.split("/"))[-1] + ".jpeg"
                runCommand("curl", coverURL, "--output", cover)
                print("Waiting for lyric refresh...")
                lyrics = pullLyrics(name, artists[0])
                print(f"Song: {name}\nArtists: {artists}\nCover image URL: {coverURL}\nProgress: {str(progress)[2:7]}\n")
            currentName = name
            print("Rendering...")
            rest = renderPlaying(client, lyrics, name, artists, cover, progress, delay, length)
            rest = 4 if rest > 4 else rest
            print("Copying...")
            copyTime = time.perf_counter()
            runCommand("scp", "render.png", f"{ip}:~/")
            
            # Full refreshes kindle's eink screen every 20 renders (to prevent ghosting and artifacting from compounding too much)
            if refresh%10 == 0:
                runCommand("ssh", ip, "/usr/sbin/eips -fg ~/render.png")
            else:
                runCommand("ssh", ip, "/usr/sbin/eips -g ~/render.png")

            # Calculates copy and display times and dynamically sleeps to try to hit refresh interval target
            copyTime = time.perf_counter() - copyTime
            delays.append(copyTime)
            if len(delays) > 5:
                del delays[0]
            avgTime = sum(delays)/len(delays)
            delay = timedelta(seconds=avgTime)
            refresh += 1
            print(f"Time to copy and display: {copyTime}\nAverage time: {avgTime}")
            (print(f"Sleeping for {rest-avgTime}..."), time.sleep(rest - avgTime)) if avgTime < rest else print("Behind, skipping sleep")

if __name__ == "__main__":
    run()