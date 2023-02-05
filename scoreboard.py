import eel
eel.init('web')

import challonge
import json

challonge.set_credentials(input("Challonge username: "), input("Your api key: "))
tournament_id = input("tournament id: ")


p1name = ""
p1subtitle = "" 
p1score = 0
p2name = ""
p2subtitle = ""
p2score = 0 
info = ""
matchid = ""
matchno = 0
num_matches = 1


def refresh():
	global p1name, p1subtitle, p1score, p2name, p2subtitle, p2score, num_matches, info, matchid
	matches = challonge.matches.index(tournament_id)
	num_matches = len(matches)
	p1score = parse_csv_score(matches)[0]
	p2score = parse_csv_score(matches)[1]
	p1 = challonge.participants.show(tournament_id, matches[matchno]["player1_id"])
	p2 = challonge.participants.show(tournament_id, matches[matchno]["player2_id"])
	p1name = p1["name"]
	p2name = p2["name"]
	info = matches[matchno]["round"]
	matchid = matches[matchno]["id"]
	print("id:", matchid)


def push_refresh():
	print({'scores_csv': str(p1score) + "-" + str(p2score)})
	challonge.matches.update(tournament_id, matchid, {'scores_csv': str(p1score) + "-" + str(p2score)})



@eel.expose
def receiveKeyPress(name, code):
	global matchno
	global p1score, p2score
	if name.lower() == "arrowleft":
		p1score += 1
		push_refresh()
	if name.lower() == "arrowright":
		p2score += 1
		push_refresh()
	if name.lower() == "arrowup":
		matchno -= 1
		print(matchno)
	if name.lower() == "arrowdown":
		matchno += 1
		print(matchno)

	refresh()
	push_js()


def push_js():
	eel.setScoreboard(p1name, p1subtitle, p1score, p2name, p2subtitle, p2score, info, matchid)




def parse_csv_score(matches):
	csv = matches[matchno]["scores_csv"]
	if len(csv) == 0:
		return (0, 0)
	else:
		a = int(csv.split("-")[0])
		b = int(csv.split("-")[1])
		return (a, b)


eel.start('scoreboard.html')