
import json
import mpyq
import argparse
from heroprotocol import hero_cli
from heroprotocol.versions import protocol85894 as protocol


#make 10 players
p0 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}
p1 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}
p2 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}
p3 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}
p4 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}
p5 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}
p6 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}
p7 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}
p8 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}
p9 = {"name":0, "hero":0, "result":0, "teamid":0, "talent": {1:0, 4:0, 7:0, 10:0, 13:0, 16:0, 20:0}}

members = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]


#Change nth Tier to level
def th_level(a):
	if a == "Tier 1 Choice":
		return 1
	elif a == "Tier 2 Choice":
		return 4
	elif a == "Tier 3 Choice":
		return 7
	elif a == "Tier 4 Choice":
		return 10
	elif a == "Tier 5 Choice":
		return 13
	elif a == "Tier 6 Choice":
		return 16
	elif a == "Tier 7 Choice":
		return 20

#make team
def make_team(members):
	_dict = {"Team1":  members[0:5], "Team2" : members[5:10]}
	return _dict

	
#############################MAIN##############################

#Nickname, Hero, Gameresult, Gameid
parser = argparse.ArgumentParser()
parser.add_argument('replay_file', help='.StormReplay file to load')
args = parser.parse_args()
archive = mpyq.MPQArchive(args.replay_file)

line = str(args)
line = line.split("'")
line = line[1]	#store replay file name

contents = archive.read_file('replay.details') 
details = protocol.decode_replay_details(contents)

a = []
for i in tracker:
	a.append(i)
tracker = a

i=0 #the number of players

while i<10:
	members[i]["name"] = details["m_playerList"][i]["m_name"].decode('utf-8')
	members[i]["hero"] = details["m_playerList"][i]["m_hero"].decode('utf-8')
	members[i]["result"] = details["m_playerList"][i]["m_result"]
	members[i]["teamid"] = details["m_playerList"][i]["m_teamId"]
	i += 1

#Talent
contents = archive.read_file('replay.tracker.events')
tracker = protocol.decode_replay_tracker_events(contents)

k = 0 #the number of players
j = 0 #the number of talents

for i in range(0, len(a)):
	if "m_eventName" in tracker[i].keys():
		if tracker[i]["m_eventName"] == b'EndOfGameTalentChoices':
			a = tracker[i]["m_stringData"][3:]
			for j in range(0, len(a)):
				level = th_level(a[j]["m_key"].decode('utf-8'))
				members[k]["talent"][level] = a[j]["m_value"].decode('utf-8')
			k+=1			

dict_replay = make_team(members) #dict to transform into .json file

filename = line
json_replay = json.dumps(dict_replay, indent = 4,  ensure_ascii=False)
filename_json = filename + ".json"
f = open(filename_json, 'w')
f.write(json_replay)
f.close()

