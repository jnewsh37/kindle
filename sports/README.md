# Synopsis
Currently contains 2 Python programs that display sports info on an 800x600 Kindle screen using data
from ESPN's internal API; baseball.py shows an overview of the first 10 games and displays info using 
the built-in "eips" command on Kindles while basketball.py shows a detailed overview of one game
including score, time, team stats, and the most recent play rendering info using the Pillow library.

# How to run
basketball.py takes in 3 parameters: the game number (starting at 0 and going to however many games
exist the day ran), the league name (tested on the WNBA and NBA), and the kindle's SSH info (hostname@IP) 

# Notes
Higher refresh intervals run the risk of ESPN detecting abnormal activity and potentially
IP-banning you from pulling data, currently at 7 seconds rest + render and scp time (like 9-10s)

# To-do
Utilize previously downloaded static assets such as player and team images instead of pulling every cycle
Write an automated handler program or web UI so I don't gotta sit at my desk, log into my computer,
open a terminal, and run the program by hand each and every time (so much work, I know)
Rewrite most rendering functions to use dynamic spacing rather than relying on static coords
