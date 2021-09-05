
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

global members
members = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]

game_data = {"Map": 0, "GameType": 0, "banned": [], "picked": []}

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

def get_parameter():
	parser = argparse.ArgumentParser()
	parser.add_argument('replay_file', help='.StormReplay file to load')
	args = parser.parse_args()	
	return args

def get_replay_file(args):
	replay_file = mpyq.MPQArchive(args.replay_file)
	return replay_file
	
def get_file_name(args):
	line = str(args)
	line = line.split("'")
	file_name = line[1]	#store replay file name
	return file_name

def read_details(replay_file):
	contents = replay_file.read_file('replay.details')
	details = protocol.decode_replay_details(contents)
	return details

def process_details(replay_file):
	details = read_details(replay_file)
	for i in range(0, 10):
		members[i]["name"] = details["m_playerList"][i]["m_name"].decode('utf-8')
		members[i]["hero"] = details["m_playerList"][i]["m_hero"].decode('utf-8')
		game_data["picked"].append(details["m_playerList"][i]["m_hero"].decode('utf-8'))
		members[i]["result"] = details["m_playerList"][i]["m_result"]
		members[i]["teamid"] = details["m_playerList"][i]["m_teamId"]
	game_data["Map"] = details["m_title"].decode('utf-8')

def read_trackerevents(replay_file):
	contents = replay_file.read_file('replay.tracker.events')
	temp = protocol.decode_replay_tracker_events(contents)
	trackerevents = []
	for i in temp:
		trackerevents.append(i)
	return trackerevents
	
def process_trackerevents(replay_file):
	trackerevents = read_trackerevents(replay_file)
	k=0
	for i in range(0, len(trackerevents)):
		if "m_eventName" in trackerevents[i].keys():
				if trackerevents[i]["m_eventName"] == b'EndOfGameTalentChoices':
					temp = trackerevents[i]["m_stringData"][3:]
					for j in range(0, len(temp)):
						level = th_level(temp[j]["m_key"].decode('utf-8'))
						members[k]["talent"][level] = temp[j]["m_value"].decode('utf-8')
					k+=1

def extract_banned(replay_file):
	trackerevents = read_trackerevents(replay_file)
	for i in range(0, 100):
		if trackerevents[i]['_event'] == "NNet.Replay.Tracker.SHeroBannedEvent":
			game_data["banned"].append(trackerevents[i]["m_hero"].decode('utf-8'))

def make_team():
	_dict = {"Team1": [], "Team2": []}
	for i in range(0, len(members)):
		if members[i]["result"] == 1:
			_dict["Team1"].append(members[i])
		else:
			_dict["Team2"].append(members[i])
	return _dict
		

def make_json(args):
	dict_replay = make_team()
	json_replay = json.dumps(dict_replay, indent=4, ensure_ascii=False)
	json_replay_game_data = json.dumps(game_data, indent=4, ensure_ascii=False)
	file_name = get_file_name(args)
	file_name_json = file_name + ".json"
	f = open(file_name_json, 'w')
	f.write(json_replay_game_data)
	f.write("\n\n")
	f.write(json_replay)
	f.close()
#############################MAIN##############################

args = get_parameter()
replay_file = get_replay_file(args)

process_details(replay_file)
process_trackerevents(replay_file)
extract_banned(replay_file)

make_json(args)

