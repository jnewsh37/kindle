#! /usr/bin/python3 
import subprocess, time, json, sys
from PIL import Image, ImageDraw, ImageFont

wnba = "wnba.txt"
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 1)

def runCommand(program, *params):
	result = subprocess.run([program,*params], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
	return result.stdout
stats = []
event = []
stats = []
leaders = []
awayIndex = []

def refreshData():
	runCommand("curl", "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard", "--output", wnba)
	global event, stats, leaders, awayIndex
	stats.clear()
	leaders.clear()
	with open(wnba) as f:
		data = json.load(f)
	event = data["events"]
	e = 0
	for g in event:
		id = g["id"]
		runCommand("curl", f'https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/summary?event={id}', "--output", f'{id}.txt')
		with open(f'{id}.txt') as s:
			sdata = json.load(s)
		leaders.append(sdata["leaders"])
		sdata = sdata["boxscore"]
		stats.append(sdata)
		tmpIndex = {}
		tmpIndex["scoreboard"] = 0 if event[e]["competitions"][0]["competitors"][0]["homeAway"] == "away" else 1
		tmpIndex["stats"] = 0 if "away" in stats[e]["teams"][0]["homeAway"] else 1
		tmpIndex["leaders"] = 0 if leaders[e][0]["team"]["displayName"] == event[e]["competitions"][0]["competitors"][tmpIndex["scoreboard"]]["team"]["displayName"] else 1
		awayIndex.append(tmpIndex)
		e += 1

refreshData()

class Game:
	def __init__(self, event):
		self.event = event
	def getScore(self, g):
		comp = event[g]["competitions"][0]["competitors"]
		return f'{comp[awayIndex[g]["scoreboard"]]["score"]} - {comp[1 - awayIndex[g]["scoreboard"]]["score"]}'
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

def fontSize(f):
	global font
	font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", f)

def pasteImage(x, y, size, cvs, url):
	runCommand("curl", url, "--output", "tmp.png")
	with Image.open("tmp.png") as img:
		img = img.resize((size,size))
		cvs.paste(img, (x, y), img)

def pbpIcon(x, y, size, cvs, url, width, fill):
	runCommand("curl", url, "--output", "tmp.png")
	with Image.open("tmp.png") as img:
		background = Image.new("L", (size, size), fill)
		ar = img.width/img.height
		img = img.resize((int(size*ar),size))
		mask = Image.new("L", background.size, 0)
		maskDraw = ImageDraw.Draw(mask)
		maskDraw.ellipse((0,0,background.height,background.height), fill=255)
		background.paste(img, (int((background.width - img.width)/2), 0), img)
		ImageDraw.Draw(background).ellipse((0,0,background.height-width/2,background.height-width/2), outline = 0, width=width)
		cvs.paste(background, (x,y), mask=mask)

def renderStats(x, y, g, t, cvs):
	teamStats = {}
	draw = ImageDraw.Draw(cvs)
	rawStats = stats[g]["teams"][t]["statistics"]
	for s in rawStats:
		teamStats[s["name"]] = s["displayValue"]
	statsToRender = ["FG", "3FG", "FT", "AST", "REB", "TO", "STL", "BLK", "PFT", "PF"]
	espnNames = {"FG": "fieldGoalsMade-fieldGoalsAttempted", "3FG": "threePointFieldGoalsMade-threePointFieldGoalsAttempted","FT": "freeThrowsMade-freeThrowsAttempted","AST": "assists","REB": "totalRebounds","TO": "turnovers","STL": "steals","BLK": "blocks","PFT": "turnoverPoints","PF": "fouls",}
	spacing=0
	row = 0
	for i in range(10):
		statValue = teamStats[espnNames[statsToRender[i]]]
		fontSize(18)
		draw.text((x + spacing, y + (row * 85) + 32), statsToRender[i], font=font)
		fontSize(28)
		draw.text((x + spacing, y + (row * 85)), statValue, font=font)
		if ('-' in statValue):
			num1 = int(statValue[:statValue.find("-")])
			num2 = int(statValue[statValue.find("-")+1:])
			print(f'{num1}/{num2}')
			fontSize(18)
			draw.text((x + spacing, y + (row * 85) + 55), f'{int((num1/num2)*1000)/10 if num2 != 0 else 0}%', font=font)
		statLen = len(statValue) if len(statValue) > 2 else 2
		spacing += ((statLen * 14) + 20)
		if (i == 4):
			row+=1
			spacing = 0


def renderLeaders(x, y, g, t, cvs):
	l = leaders[g][t]["leaders"]
	draw = ImageDraw.Draw(cvs)
	statsToRender = ["pts", "ast", "reb"]
	for i in range(len(statsToRender)):
		fontSize(26)
		draw.text((x, y + 32*i), (f'{l[i]["leaders"][0]["athlete"]["fullName"]} • {l[i]["leaders"][0]["athlete"]["position"]["abbreviation"]}: {int(l[i]["leaders"][0]["value"])} {statsToRender[i]}'), font=font)



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
		draw.text((125+i*462,22), f'{event[g]["competitions"][0]["competitors"][1*i - awayIndex[g]["scoreboard"]]["team"]["location"]}\n{event[g]["competitions"][0]["competitors"][1*i-awayIndex[g]["scoreboard"]]["team"]["name"]}', font=font, fill=0)
		pasteImage(22+i*462, 15, 85, screen, event[g]["competitions"][0]["competitors"][1*i - awayIndex[g]["scoreboard"]]["team"]["logo"])
	fontSize(40)
	draw.text((400, 70), "@", font=font, fill=0, align="center", anchor="mm")

	#Status
	fontSize(25)
	draw.text((400, 30), event[g]["competitions"][0]["status"]["type"]["shortDetail"], font=font, align="center", anchor="mm")
	fontSize(35)
	draw.text((400,120), game.getScore(g), font=font, align="center", anchor="mm")

	#Latest play
	#Play info
	yCoord = 150
	play, player, team = game.getLastPlay(g)
	fontSize(24)
	if (play != "Game not active"):
		draw.text((136, yCoord), f'{play.replace("\n", "")}', font=font)
		print(play)

	#Player info + player/team pfp
		if (team != "noTeam"):
			for i in range(2):
				if (team == event[g]["competitions"][0]["competitors"][i]["id"]):
					if (event[g]["competitions"][0]["competitors"][i]["homeAway"] == "away"):
						tNum = awayIndex[g]["stats"]
					else:
						tNum = 1 - awayIndex[g]["stats"]
					break
			if ((player !="noAthlete") & (team != "noTeam")):
				athletes = stats[g]["players"][tNum]["statistics"][0]["athletes"]
				for p in range(len(athletes)):
					if (athletes[p]["athlete"]["id"] == player):
						athleteStats = dict(zip(stats[g]["players"][tNum]["statistics"][0]["names"], stats[g]["players"][tNum]["statistics"][0]["athletes"][p]["stats"]))
						draw.text((136,yCoord+40), f'{athletes[p]["athlete"]["displayName"]} - {athleteStats.get("PTS", 0)} pts, {athleteStats.get("REB", 0)} reb, {athleteStats.get("AST", 0)} ast, {athleteStats.get("FG", 0)} FG, {int(athleteStats.get("STL", 0)) + int(athleteStats.get("BLK", 0))} stl+blk', font=font)
						url = athletes[p]["athlete"]["headshot"]["href"] if athletes[p]["athlete"].get("headshot", []) else "default.png"
						pbpIcon(10, yCoord-25, 110, screen, url, 2, 180)
			else:
				pbpIcon(10, yCoord-25, 110, screen, event[g]["competitions"][0]["competitors"][i]["team"]["logo"], 0, 255)
	else:
		fontSize(50)
		draw.text((400, 200), play, font=font, align="center", anchor="mm")

	#Team stats
	renderStats(30, 275, g, awayIndex[g]["stats"], screen)
	renderStats(430, 275, g, 1 - awayIndex[g]["stats"], screen)

	#Team leaders
	renderLeaders(30, 465, g, awayIndex[g]["leaders"], screen)
	renderLeaders(430, 465, g, 1-awayIndex[g]["leaders"], screen)

	screen.save(f"render.png")

runCommand('ssh', 'kindle2', '/usr/sbin/eips -fc')
count = 0
while True:
	renderImage(int(sys.argv[1]))
	runCommand("scp", "render.png", "kindle2:~/")
	command = "/usr/sbin/eips -g testrender.png" if count%10 != 0 else "/usr/sbin/eips -fg render.png"
	runCommand("ssh", "kindle2", command)
	count += 1
	refreshData()
	time.sleep(7)

#Old program (showed status of multiple games)
#
#writeQueue = []
#
#def queueLine(x, y, info):
#	toAppend = f'/usr/sbin/eips {x} {y} "{info}"'
#	writeQueue.append(toAppend)
#
#def textData():
#	gAmount = (len(event))
#	for i in range(gAmount):
#		queueLine(3, 2+ i*3, game.getScore(i))
#		queueLine(3, 2+ i*3 + 1, game.getLastPlay(i))
#

#runCommand('ssh', 'kindle', '/usr/sbin/eips -fc')

#while True:
#	textData()
#	runCommand('ssh', 'kindle2', ";".join(writeQueue))
#	runCommand('curl', "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard", '--output', wnba)
#	refreshData()
#	writeQueue.clear()
#	time.sleep(8)