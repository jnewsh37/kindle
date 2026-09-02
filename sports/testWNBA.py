#! /usr/bin/python3 
import subprocess, time, json
from PIL import Image, ImageDraw, ImageFont


wnba = "testWNBA.txt"
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 1)
stats = []

def runCommand(program, *params):
	result = subprocess.run([program,*params], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
	return result.stdout

event = []
stats = []

def refreshData():
	#runCommand("curl", "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard", "--output", wnba)
	global event, stats
	stats.clear()
	with open(wnba) as f:
		data = json.load(f)
	event = data["events"]
	for g in event:
		id = g["id"]
		runCommand("curl", f'https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/summary?event={id}', "--output", f'{id}.txt')
		with open(f'{id}.txt') as s:
			sdata = json.load(s)
		sdata = sdata["boxscore"]
		stats.append(sdata)

refreshData()

class Game:
	def __init__(self, event):
		self.event = event
	def getScore(self, g):
		comp = event[g]["competitions"][0]["competitors"]
		return f'{comp[0]["score"]} - {comp[1]["score"]}'
	def getLastPlay(self, g):
		if ("situation" in event[g]["competitions"][0]):
			lastPlay = event[g]["competitions"][0]["situation"]["lastPlay"]
			athletes = lastPlay.get("athletesInvolved", [])
			team = lastPlay.get("team", [])
			player = athletes[0].get("id", "noAthlete") if athletes else "noAthlete"
			id = team.get("id", "noTeam") if team else "noTeam"
			return lastPlay["text"], player, id
		else:
			return "Game not active", 0, 0

	def getTeamLogo(self, g, t):
		logo = event[g]["competitions"][0]["competitors"][t]["team"]["logo"]
		name = f'WNBA{(event[g]["competitions"][0]["competitors"][t]["team"]["name"]).lower()}.png'
		runCommand("curl", logo, "--output", f'{name}')
		return name



game = Game(event)

writeQueue = []

def queueLine(x, y, info):
	toAppend = f'/usr/sbin/eips {x} {y} "{info}"'
	writeQueue.append(toAppend)

def textData():
	gAmount = (len(event))
	for i in range(gAmount):
		queueLine(3, 2+ i*3, game.getScore(i))
		queueLine(3, 2+ i*3 + 1, game.getLastPlay(i))

def fontSize(f):
	global font
	font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", f)

def pasteImage(x, y, size, cvs, url):
	runCommand("curl", url, "--output", "tmp.png")
	with Image.open("tmp.png") as img:
		img = img.resize((size,size))
		cvs.paste(img, (x, y), img)

def playerIcon(x, y, size, cvs, url):
	runCommand("curl", url, "--output", "tmp.png")
	with Image.open("tmp.png") as img:
		img.thumbnail((size,size))
		mask = Image.new("L", img.size, 0)
		height, foo = img.size
		maskDraw = ImageDraw.Draw(mask)
		maskDraw.ellipse((0,0,height,height), fill=255)
		cvs.paste(img, (x,y), mask=mask)

def renderImage(g):
	global font
	screen = Image.new("L", (800,600), 255)
	draw = ImageDraw.Draw(screen)
	# Layout elements
	draw.line((40, 255, 328, 255), fill=0, width=5)
	draw.line((474, 255, 762, 255), fill=0, width=5)
	fontSize(18)
	draw.text((400,253), "Team Stats", font=font, fill=0, align="center", anchor="mm")
	draw.line((400, 272, 400, 408), fill=0, width=5)

	draw.line((40, 435, 328, 435), fill=0, width=5)
	draw.line((474, 435, 762, 435), fill=0, width=5)
	draw.text((400,435), "Team Leaders", font=font, fill=0, align="center", anchor="mm")
	draw.line((400, 452, 400, 588), fill=0, width=5)

	#Header
	fontSize(30)
	for i in range(2):
		draw.text((125+i*462,22), f'{event[g]["competitions"][0]["competitors"][i]["team"]["location"]}\n{event[g]["competitions"][0]["competitors"][i]["team"]["name"]}', font=font, fill=0)
		pasteImage(22+i*462, 15, 85, screen, event[g]["competitions"][0]["competitors"][i]["team"]["logo"])
	fontSize(40)
	draw.text((400, 70), "@", font=font, fill=0, align="center", anchor="mm")

	#Status
	fontSize(25)
	draw.text((400, 30), event[g]["competitions"][0]["status"]["type"]["shortDetail"], font=font, align="center", anchor="mm")
	fontSize(35)
	draw.text((400,125), game.getScore(g), font=font, align="center", anchor="mm")

	#Latest play
	#Play info
	yCoord = 160
	play, player, team = game.getLastPlay(g)
	fontSize(24)
	if (play != "Game not active"):
		draw.text((136, yCoord+40), f'{play}', font=font)
		print(play)
		if ((play != "Game not active") & (player !="noAthlete") & (team != "noTeam")):
			tNum = 2
			for i in range(2):
				if (team == event[g]["competitions"][0]["competitors"][i]["id"]):
					tNum = 1-i
					break
			athletes = stats[g]["players"][tNum]["statistics"][0]["athletes"]
			for p in range(len(athletes)):
#				print(f'{athletes[p]["athlete"]["id"]}')
				if (athletes[p]["athlete"]["id"] == player):
					athleteStats = athletes[p]["stats"]
					draw.text((136,yCoord), f'{athletes[p]["athlete"]["displayName"]} - {athleteStats[1]} points, {athleteStats[2]} reb, {athleteStats[6]} ast, {athleteStats[8]} stl, {athleteStats[9]} blk', font=font)

	else:
		fontSize(50)
		draw.text((400, 200), play, font=font, align="center", anchor="mm")

	screen.save("testrender.png")


#while True:
#	renderImage(2)
#	runCommand("scp", "testrender.png", "kindle:~/")
#	runCommand("ssh", "kindle", "/usr/sbin/eips -g testrender.png")
#	refreshData()
#	time.sleep(8)

foo, player, bar = game.getLastPlay(0)
athletes = stats[0]["players"][1]["statistics"][0]["athletes"]
for p in range(len(athletes)):
	if (athletes[p]["athlete"]["id"] == player):
		url = athletes[p]["athlete"]["headshot"]["href"]


screen = Image.new("L", (800,600), 255)
playerIcon(0,0, 400, screen, url)
screen.save("icontest.png")
#print(stats[0]["boxscore"]["players"][0]["statistics"][0]["athletes"])

#runCommand('ssh', 'kindle', '/usr/sbin/eips -fc')

#while True:
#	textData()
#	runCommand('ssh', 'kindle', ";".join(writeQueue))
#	runCommand('curl', "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard", '--output', wnba)
#	refreshData()
#	writeQueue.clear()
#	time.sleep(8)
