#! /usr/bin/python3 
import subprocess, time

class game:
	def __init__(self, num, name):
		self.num = num
		self.name = name
		self.team1 = runCommand('jq', '-r', f'.events[{self.num}].competitions[0].competitors[0].team.name', './mlb.txt').strip()
		self.team2 = runCommand('jq', '-r', f'.events[{self.num}].competitions[0].competitors[1].team.name', './mlb.txt').strip()
	def getScore(self):
		self.score1 = runCommand('jq', '-r', f'.events[{self.num}].competitions[0].competitors[0].score', './mlb.txt').strip()
		self.score2 = runCommand('jq', '-r', f'.events[{self.num}].competitions[0].competitors[1].score', './mlb.txt').strip()
		return f"{self.team1}: {self.score1} {self.team2}: {self.score2}"
	def getLastPlay(self):
		print(runCommand('jq', f'.events[{self.num}].competitions[].playByPlayAvailable', './mlb.txt'))
		if (runCommand('jq', f'.events[{self.num}].competitions[].situation', './mlb.txt').strip() != "null"):
			self.playDesc = runCommand('jq', '-r', f'.events[{self.num}].competitions[0].situation.lastPlay.text', './mlb.txt').strip()
			return self.playDesc
		else:
			return " "
	def getCount(self):
		if (runCommand('jq', f'.events[{self.num}].competitions[].situation', './mlb.txt').strip() != "null"):
			self.count = f"Balls: {runCommand('jq', '-r', f'.events[{self.num}].competitions[0].situation.balls', './mlb.txt').strip()} Strikes: {runCommand('jq', '-r', f'.events[{self.num}].competitions[0].situation.strikes', './mlb.txt').strip()}"
			return self.count
		else:
			return "Game end"

	

def runCommand(program, *params):
	result = subprocess.run([program,*params], capture_output=True, text=True)
	return result.stdout


games = {}
gamelist = runCommand('jq', '-r', '.events[].id', './mlb.txt').splitlines()
gamenames = runCommand('jq', '-r', '.events[].name', './mlb.txt').splitlines()

for g in gamelist:
	print(g)
	tmp=gamenames[gamelist.index(g)]
#	print(tmp)
	games[g] = game(gamelist.index(g), tmp)
print(games["401816428"].getScore())
writeQueue = []
def addToQueue(line, row, info):
	toAppend = f'/usr/sbin/eips {row} {line} "{info}"'
	writeQueue.append(toAppend)
runCommand('curl', "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard", '--output', 'mlb.txt')
runCommand('ssh', 'kindle', '/usr/sbin/eips', '-fc')

def run10():
	spacing = 5
	yspacing = 3
	runCommand('ssh', 'kindle', '/usr/sbin/eips', '-c')
	for i in range(5):
		addToQueue((yspacing + i*spacing), 3, f'{games[f"{gamelist[i]}"].getScore()}')
		addToQueue((yspacing+1 + i*spacing), 3, f'{games[f"{gamelist[i]}"].getCount()}')
#		print(gamelist[i])
		pbp = games[f"{gamelist[i]}"].getLastPlay()
		if (len(pbp) > 26):
			pbp1 = pbp[:(pbp.rfind(' ', 0, 26))]
			pbp2 = pbp[(len(pbp1)+1):]
			addToQueue((yspacing+2 + i*spacing), 3, ("  " + pbp1))
			addToQueue((yspacing+3 + i*spacing), 3, ("  " + pbp2))
		else:
			addToQueue((yspacing+2 + i*spacing), 3, f'  {games[f"{gamelist[i]}"].getLastPlay()}')

	for i in range(5):
		addToQueue((yspacing + i*spacing), 35, f'{games[f"{gamelist[i+3]}"].getScore()}')
		addToQueue((yspacing+1 + i*spacing), 35, f'{games[f"{gamelist[i+3]}"].getCount()}')
#		print(gamelist[i])
		pbp = games[f"{gamelist[i+3]}"].getLastPlay()
		if (len(pbp) > 26):
				pbp1 = pbp[:(pbp.rfind(' ', 0, 26))]
				pbp2 = pbp[(len(pbp1)+1):]
				addToQueue((yspacing+2 + i*spacing), 35, ("  " + pbp1))
				addToQueue((yspacing+3 + i*spacing), 35, ("  " + pbp2))
		else:	
				addToQueue((yspacing+2 + i*spacing), 35, f'  {games[f"{gamelist[i+3]}"].getLastPlay()}')
		
	runCommand('ssh', 'kindle', ";".join(writeQueue))
	runCommand('curl', "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard", '--output', 'mlb.txt')
	writeQueue.clear()

while True:
	run10()
	time.sleep(60)