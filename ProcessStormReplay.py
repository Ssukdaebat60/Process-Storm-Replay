import json
import mpyq
import argparse
from heroprotocol import hero_cli
from heroprotocol.versions import protocol85894 as protocol


class ProcessStormReplay:
	def __init__(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('replay_file', help='.StormReplay file to load')
		self.args = parser.parse_args()
	
	def output(self, _dict):
		json_replay = json.dumps(_dict, indent=4, ensure_ascii=False)
		f = open(self.get_file_name(), 'w')
		f.write(json_replay)
		f.close()

	def get_replay(self, option):
		replay_file = mpyq.MPQArchive(self.args.replay_file)
		if option == "details":
			return self.get_details(replay_file)
		elif option == "trackerevents":
			return self.get_trackerevents(replay_file)
		elif option == "initdata":
			return self.get_initdata(replay_file)
	
	def get_file_name(self):	
		line = str(self.args)
		line = line.split("'")
		return line[1] + ".json"

	def get_details(self, replay_file):
		contents = replay_file.read_file('replay.details')
		details = protocol.decode_replay_details(contents)
		return details
	
	def get_trackerevents(self, replay_file):
		contents = replay_file.read_file('replay.tracker.events')
		temp = protocol.decode_replay_tracker_events(contents)
		trackerevents = []
		for i in temp:
			trackerevents.append(i)
		return trackerevents
		
	def get_initdata(self, replay_file):
		contents = replay_file.read_file('replay.initData')
		initdata = protocol.decode_replay_initdata(contents)
		return initdata


class ExtractData(ProcessStormReplay):
	def make_dict(self, player_data, game_data):
		_dict = {"GameData": game_data, "Team1": [], "Team2": []}
		for i in range(0, len(player_data)):
			if player_data[i]["result"] == 1:
				_dict["Team1"].append(player_data[i])
			else:
				_dict["Team2"].append(player_data[i])
		return _dict

	def get_player_data(self):
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
		self.get_player_info("details", members)
		self.get_player_talent("trackerevents", members)
		return members
		
	def get_game_data(self):
		game_data = {"map": 0, "gametype": 0, "banned": [], "picked": []}
		self.get_game_map("details", game_data)
		self.get_game_type("initdata", game_data)
		self.get_game_banned("trackerevents", game_data)
		self.get_game_picked("details", game_data)
		return game_data

	def get_player_info(self, option, members):
		details = super().get_replay(option)
		for i in range(0, 10):
			members[i]["name"] = details["m_playerList"][i]["m_name"].decode('utf-8')
			members[i]["hero"] = details["m_playerList"][i]["m_hero"].decode('utf-8')
			members[i]["result"] = details["m_playerList"][i]["m_result"]
			members[i]["teamid"] = details["m_playerList"][i]["m_teamId"]
	
	def get_player_talent(self, option, members):
		trackerevents = super().get_replay(option)
		k=0
		for i in range(0, len(trackerevents)):
			if "m_eventName" in trackerevents[i].keys():
				if trackerevents[i]["m_eventName"] == b'EndOfGameTalentChoices':
					temp = trackerevents[i]["m_stringData"][3:]
					for j in range(0, len(temp)):
						level = self.th_level(temp[j]["m_key"].decode('utf-8'))
						members[k]["talent"][level] = temp[j]["m_value"].decode('utf-8')
					k+=1		
	
	def get_game_map(self, option, game_data):
		details = super().get_replay(option)
		game_data["map"] = details["m_title"].decode('utf-8')
	
	def get_game_type(self, option, game_data):
		initdata = super().get_replay(option)
		game_data["gametype"] = self.custom_true(initdata["m_syncLobbyState"]['m_gameDescription']['m_gameOptions'])
	
	def get_game_banned(self, option, game_data):
		trackerevents = super().get_replay(option)
		for i in range(0, 100):
			if trackerevents[i]['_event'] == "NNet.Replay.Tracker.SHeroBannedEvent":
				game_data["banned"].append(trackerevents[i]["m_hero"].decode('utf-8'))
	
	def get_game_picked(self, option, game_data):
		details = super().get_replay(option)
		for i in range(0, 10):
			game_data["picked"].append(details["m_playerList"][i]["m_hero"].decode('utf-8'))
		
	def th_level(self, a):
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

	def custom_true(self, gameoptions):
		_list = [False, False, True, False, False, False, True, False, False, False, False]
		list_gameoptions = []
		list_gameoptions.append(gameoptions['m_advancedSharedControl'])
		list_gameoptions.append(gameoptions['m_amm'])
		list_gameoptions.append(gameoptions['m_battleNet'])
		list_gameoptions.append(gameoptions['m_competitive'])
		list_gameoptions.append(gameoptions['m_cooperative'])
		list_gameoptions.append(gameoptions['m_heroDuplicatesAllowed'])
		list_gameoptions.append(gameoptions['m_lockTeams'])
		list_gameoptions.append(gameoptions['m_noVictoryOrDefeat'])
		list_gameoptions.append(gameoptions['m_practice'])
		list_gameoptions.append(gameoptions['m_randomRaces'])
		list_gameoptions.append(gameoptions['m_teamsTogether'])
		if _list == list_gameoptions:
			return 1
		else:
			return 0


#main
if __name__ == "__main__":
	m = ExtractData()
	m.output(m.make_dict(m.get_player_data(), m.get_game_data()))
