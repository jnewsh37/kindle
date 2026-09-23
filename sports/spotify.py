#! /usr/bin/env python3

import sys, syncedlyrics, subprocess, spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyPKCE
from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta
from basketball import runCommand

SCOPE = "user-read-currently-playing"
redirect = "http://127.0.0.1:8888/callback"

# Creates a spotipy.Spotify client, 
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

def renderPlaying(client:spotipy.Spotify):
    data = client.currently_playing()
    name = data["item"]["name"]
    artists = []
    for artist in data["item"]["artists"]:
        artists.append(artist["name"])
    progress = data["progress_ms"]
    coverURL = str(data["item"]["album"]["images"][0]["url"])
    cover = (coverURL.split("/"))[-1] + ".jpeg"
    runCommand("curl", coverURL, "--output", cover)

    screen = Image.new("L", (800,600), 255)
    draw = ImageDraw.Draw(screen)
    pasteImage(50, 100, 400, screen, cover)
    fontSize(30)
    draw.text((500, 100), name,font=font)
    fontSize(20)
    draw.text((500, 150), artists[0],font=font)

    screen.save("SpotifyTest.png")
    print(f"Song: {name}\nArtists: {artists}\nCover image URL: {coverURL}\nProgress: {progress}")

renderPlaying(create_spotify_client())
runCommand("scp", "SpotifyTest.png", "kindle3:~/")
runCommand("ssh", "kindle3", "/usr/sbin/eips -fg ~/SpotifyTest.png")