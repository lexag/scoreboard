

function setScoreboard(p1name, p1sub, p1score, p2name, p2sub, p2score, info, matchid) {
	$('#one > .name').text(p1name);
	$('#one > .subtitle').text(p1sub);
	$('#one > .score').text(p1score);
	$('#two > .name').text(p2name);
	$('#two > .subtitle').text(p2sub);
	$('#two > .score').text(p2score);
	$('p.info').text(info);
	$('p.match_id').text(matchid);
	console.log(p1name, p1sub, p1score, p2name, p2sub, p2score, info, matchid)
}
eel.expose(setScoreboard)


document.addEventListener('keydown', (event) => {
	var name = event.key;
	var code = event.code;
	// Alert the key name and key code on keydown
	eel.receiveKeyPress(name, code)
	console.log(name)
}, false);


