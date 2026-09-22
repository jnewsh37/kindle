#! /usr/bin/env python3

# Note: WNBA game numbers (at least for stats page) are in the format 102 + season + game number (example: 1022600309 ('26 season, game 309)), will update once I figure out significance of 10226

from yt_dlp import YoutubeDL
from basketball import runCommand, asyncCommand
import json, sys

team = sys.argv[1]
ip = sys.argv[2]
selfIP = sys.argv[3]
lastVid = ""
teamChannels = {"Atlanta Dream": "AtlantaDream",
    "Chicago Sky": "ChicagoSky",
    "Connecticut Sun": "ConnecticutSun",
    "Dallas Wings": "WNBADallasWings",
    "Golden State Valkyries": "ValkyriesWNBA",
    "Indiana Fever": "IndianaFever",
    "Las Vegas Aces": "LVAces",
    "Los Angeles Sparks": "TheLosAngelesSparks",
    "Minnesota Lynx": "MinnesotaLynx",
    "New York Liberty": "NewYorkLiberty",
    "Phoenix Mercury": "PhoenixMercury",
    "Portland Fire": "PortlandFire",
    "Seattle Storm": "SeattleStormOfficial",
    "Toronto Tempo": "TorontoTempo",
    "Washington Mystics": "WashingtonMystics"}

options = {
    "playlistend": 1,
    "outtmpl": "Clip.webm"
    }

with YoutubeDL(options) as yt:
    url = f"https://www.youtube.com/@{teamChannels.get(team, "Indiana Fever")}/shorts"
    info = yt.extract_info(url, download=False)
    id = info["entries"][0]["id"]
    if info["title"]!= lastVid:
        yt.download(f"https://www.youtube.com/shorts/{id}")
        lastVid = id

runCommand("bash", "./Highlight.sh", "Clip.webm", "Highlights/VideoTest.png", "./Highlights/gmv")
print("Formatting vid")
asyncCommand("bash", "./Stream.sh")
runCommand("ssh", ip, f"/bin/sh --login -c 'sleep 2; nc {selfIP} 5555|gmplay'")
print("Streaming")
