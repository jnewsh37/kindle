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
		self.playDesc = runCommand('jq', '-r', f'.events[{self.num}].competitions[0].situation.lastPlay.text', './mlb.txt').strip()
		return self.playDesc
	def getCount(self):
		self.count = f"Balls: {runCommand('jq', '-r', f'.events[{self.num}].competitions[0].situation.balls', './mlb.txt').strip()} Strikes: {runCommand('jq', '-r', f'.events[{self.num}].competitions[0].situation.strikes', './mlb.txt').strip()}"
		return self.count

	

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
spacing = 5
print(games["401816428"].getScore())
old = ""
while True:
	runCommand('ssh', 'kindle', f'/usr/sbin/eips {spacing} {spacing} "{games["401816428"].getScore()}"; /usr/sbin/eips {spacing} {spacing+1} "{games["401816428"].getLastPlay()}"; /usr/sbin/eips {spacing} {spacing+2} "{games["401816428"].getCount()}"')
	runCommand('curl', "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard", '--output', 'mlb.txt')