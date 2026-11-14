#! /usr/bin/env python3
import subprocess, time, requests, sys, json, base64
from skinpy import Skin, Perspective
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

hypixel = "https://api.hypixel.net/v2/player"
mojang = "https://sessionserver.mojang.com/session/minecraft/profile/"

bedwarsStats = {
    "Win Streak": "winstreak",
    "Items Purchased (Legacy)": "_items_purchased_bedwars",
    "Beds Lost": "beds_lost_bedwars",
    "Combat Final Deaths": "entity_attack_final_deaths_bedwars",
    "Final Deaths": "final_deaths_bedwars",
    "Games Played": "games_played_bedwars",
    "Gold Collected": "gold_resources_collected_bedwars",
    "Iron Collected": "iron_resources_collected_bedwars",
    "Items Purchased": "items_purchased_bedwars",
    "Losses": "losses_bedwars",
    "Permanent Items Purchased": "permanent_items_purchased_bedwars",
    "Resources Collected": "resources_collected_bedwars",
    "Deaths": "deaths_bedwars",
    "Diamonds Collected": "diamond_resources_collected_bedwars",
    "Combat Deaths": "entity_attack_deaths_bedwars",
    "Combat Kills": "entity_attack_kills_bedwars",
    "Kills": "kills_bedwars",
    "Void Deaths": "void_deaths_bedwars",
    "Emeralds Collected": "emerald_resources_collected_bedwars",
    "Combat Final Kills": "entity_attack_final_kills_bedwars",
    "Final Kills": "final_kills_bedwars",
    "Magic Final Deaths": "magic_final_deaths_bedwars",
    "Beds Broken": "beds_broken_bedwars",
    "Void Final Deaths": "void_final_deaths_bedwars",
    "Fall Final Deaths": "fall_final_deaths_bedwars",
    "Fall Kills": "fall_kills_bedwars",
    "Void Kills": "void_kills_bedwars",
    "Fall Deaths": "fall_deaths_bedwars",
    "Fall Final Kills": "fall_final_kills_bedwars",
    "Void Final Kills": "void_final_kills_bedwars",
    "Explosion Kills": "entity_explosion_kills_bedwars",
    "Wins": "wins_bedwars",
    "Magic Kills": "magic_kills_bedwars",
    "Fire Deaths": "fire_tick_deaths_bedwars",
    "Projectile Final Deaths": "projectile_final_deaths_bedwars",
    "Magic Final Kills": "magic_final_kills_bedwars",
    "Explosion Final Deaths": "entity_explosion_final_deaths_bedwars",
    "Explosion Deaths": "entity_explosion_deaths_bedwars",
    "Projectile Deaths": "projectile_deaths_bedwars",
    "Projectile Kills": "projectile_kills_bedwars",
    "Magic Deaths": "magic_deaths_bedwars",
    "Fire Kills": "fire_tick_kills_bedwars",
    "Fire Final Deaths": "fire_tick_final_deaths_bedwars",
    "One Block Win Streak": "oneblock_winstreak",
    "One Block Final Deaths": "oneblock_final_deaths_bedwars",
    "One Block Games Played": "oneblock_games_played_bedwars",
    "One Block Losses": "oneblock_losses_bedwars",
    "One Block Void Final Deaths": "oneblock_void_final_deaths_bedwars",
    "One Block Deaths": "oneblock_deaths_bedwars",
    "One Block Combat Deaths": "oneblock_entity_attack_deaths_bedwars",
    "One Block Combat Kills": "oneblock_entity_attack_kills_bedwars",
    "One Block Kills": "oneblock_kills_bedwars",
    "One Block Lava Deaths": "oneblock_lava_deaths_bedwars",
    "One Block Lava Final Deaths": "oneblock_lava_final_deaths_bedwars",
    "One Block Void Deaths": "oneblock_void_deaths_bedwars",
    "One Block Beds Lost": "oneblock_beds_lost_bedwars",
    "One Block Void Kills": "oneblock_void_kills_bedwars",
    "One Block Beds Broken": "oneblock_beds_broken_bedwars",
    "One Block Final Kills": "oneblock_final_kills_bedwars",
    "One Block Gold Collected": "oneblock_gold_resources_collected_bedwars",
    "One Block Iron Collected": "oneblock_iron_resources_collected_bedwars",
    "One Block Resources Collected": "oneblock_resources_collected_bedwars",
    "One Block Void Final Kills": "oneblock_void_final_kills_bedwars",
    "One Block Wins": "oneblock_wins_bedwars",
    "Fire Final Kills": "fire_tick_final_kills_bedwars",
    "Projectile Final Kills": "projectile_final_kills_bedwars",
    "8v1 Explosion Final Kills": "eight_one_entity_explosion_final_kills_bedwars"
}

def runCommand(program, *params):
	result = subprocess.run([program,*params], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
#	print(result.stderr)
	return result.stdout

def getHypixelStats(url, apikey, uuid):
	return requests.get(url, headers = {"API-Key": apikey}, params = {"uuid": uuid})

def getMojangInfo(uuid):
    return requests.get(mojang + uuid)

def renderUserSkin(uuid):
	userCosmetics = json.loads(base64.b64decode(getMojangInfo(sys.argv[2]).json()["properties"][0]["value"]).decode("utf-8"))
	print(userCosmetics["textures"]["SKIN"]["url"])
	skinImg = Image.open(BytesIO(requests.get(userCosmetics["textures"]["SKIN"]["url"]).content))
	skin = Skin.from_image(skinImg)
	perspective = Perspective(x = "left", y = "front", z = "up", scaling_factor = 10)
	return skin.to_isometric_image(perspective)

def fontSize(f):
	global font
	font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", f)

def renderStats(x, y, w, h, lines, hypixelData, statsToRender, statsDict, cvs):
	draw = ImageDraw.Draw(cvs)
	maxSize = int(h/lines - 10)
	print(maxSize)
	longestKey = 0
	for s in statsToRender:
		if (len(s) > longestKey):
			longestKey = len(s)
	print(longestKey)
	perRow = int((len(statsToRender)+1)/lines) if lines != 1 else int((len(statsToRender))/lines)
	print(perRow)
	if (1.2*perRow*.35*maxSize*longestKey > w):
		maxSize = int((w/(perRow*longestKey*1.2))/.15)
	print(maxSize)
	for i in range(len(statsToRender)):
		fontSize(int(.35*maxSize))
		draw.text(((x+int(i%perRow)*int(w/perRow)), y+(maxSize+10)*int(i/perRow)), statsToRender[i], font=font)
		fontSize(int(.55*maxSize))
		draw.text(((x+int(i%perRow)*int(w/perRow)), y+(maxSize+10)*int(i/perRow)+int(.35*maxSize)), str(hypixelData["player"]["stats"]["Bedwars"]["eight_one_"+statsDict[statsToRender[i]]]), font=font)

def render(hypixelData):
	screen = Image.new("L", (800,600), 255)
	draw = ImageDraw.Draw(screen)
	skin = renderUserSkin(sys.argv[2])
	fontSize(60)
	draw.text((400,40), "Bedwars Stats Tracker", font=font, alight="center", anchor="mm")
	screen.paste(skin, (10,80), skin)
	renderStats(250,80,520,100,1,hypixelData, ["Kills", "Deaths", "Combat Deaths", "Combat Kills"], bedwarsStats, screen)
	renderStats(250,180,520,300,2,hypixelData, ["Final Kills", "Wins", "Beds Broken", "Games Played"], bedwarsStats, screen)
	screen.save("render.png")

print(f"API Key: {sys.argv[1]}\nUUID: {sys.argv[2]}")
hypixelData = getHypixelStats(hypixel, sys.argv[1], sys.argv[2]).json()
#renderUserSkin(sys.argv[2])

def runCommand(program, *params):
	result = subprocess.run([program,*params], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
#	print(result.stderr)
	return result.stdout
render(hypixelData)
runCommand("scp", "render.png", f"kindle3:~/")
runCommand("ssh", "kindle3", "/usr/sbin/eips -g ~/render.png")
