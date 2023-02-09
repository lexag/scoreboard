import eel
eel.init('web')

import challonge

secret = open('secret.txt').readlines()

challonge.set_credentials(secret[0].strip(), secret[1].strip())
tournament_id = secret[2].strip()


p1score = 0
p2score = 0 
matchid = ""
matchno = 0
num_matches = 1

current_match = None

matches = []


# Asyncronous
def load_matches():
	global matches, num_matches
	matches = challonge.matches.index(tournament_id)
	num_matches = len(matches)

load_matches()

# on match scroll
def load_match(i):
	global p1score, p2score, matchid
	if matchid != "":
		challonge.matches.unmark_as_underway(tournament_id, matchid)
	
	global current_match
	if i < len(matches) - 1:
		current_match = matches[i]

		p1score = parse_csv_score()[0]
		p2score = parse_csv_score()[1]
		matchid = current_match["id"]

		challonge.matches.mark_as_underway(tournament_id, matchid)
	else:
		current_match = None


# On match score
def save_result():
	print({'scores_csv': str(p1score) + "-" + str(p2score)})
	challonge.matches.update(tournament_id, matchid, scores_csv= str(p1score) + "-" + str(p2score))
	load_matches()



@eel.expose
def receiveKeyPress(name, code):
	global matchno
	global p1score, p2score
	if name.lower() == "arrowleft":
		p1score += 1
		save_result()
	if name.lower() == "arrowright":
		p2score += 1
		save_result()
	if name.lower() == "a":
		p1score -= 1
		save_result()
	if name.lower() == "d":
		p2score -= 1
		save_result()
	
	if name.lower() == "arrowup":
		matchno -= 1
		load_match(matchno)
		print(matchno)
	if name.lower() == "arrowdown":
		matchno += 1
		load_match(matchno)
		print(matchno)
	if name.lower() == "r":
		load_matches()

	update_scoreboard()




# On any action
def update_scoreboard():
	if current_match is not None:
		p1 = challonge.participants.show(tournament_id, current_match["player1_id"])
		p2 = challonge.participants.show(tournament_id, current_match["player2_id"])
		eel.setScoreboard(
			p1["name"].split("|")[0].strip(), 
			p1["name"].split("|")[1].strip(), 
			p1score, 
			p2["name"].split("|")[0].strip(), 
			p2["name"].split("|")[1].strip(), 
			p2score, 
			p1score + p2score + 1, 
			current_match["id"] - matches[0]["id"] + 1)




def parse_csv_score():
	csv = current_match["scores_csv"]
	if len(csv) == 0:
		return (0, 0)
	else:
		a = int(csv.split("-")[0])
		b = int(csv.split("-")[1])
		return (a, b)


eel.start('scoreboard.html')