from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import CommonAllPlayers
from nba_api.stats import endpoints
import pandas as pd
import time
from datetime import datetime
from datetime import timedelta
import os.path
from os import path

playerNametoGrab = 'LeBron James'
seasonToGrab = '2021'
d = datetime.now() + timedelta(days=-7)
d_one_day = datetime.now() + timedelta(days=-1)
timestamp = d.strftime("%Y-%m-%d %H:%M:%S")
columns = ['Name','FGPCT', 'FGPG', "FG_VALUE", "ATO", "ATO_VALUE", "ASTAVG", "AST_VALUE", 'FTPCT', "FT_VALUE", 'RPG', "RB_VALUE", "FG3", "FG3_VALUE", "STLAVG", "STL_VALUE", "BLKAVG", "BLK_VALUE", "PTSAVG", "PTS_VALUE", "TOTAL_VALUE"]
final = pd.DataFrame(columns = columns)
comall = CommonAllPlayers(is_only_current_season=1).get_data_frames()[0]

for index, row in comall.iterrows():
	# print(row["PERSON_ID"])
	# try:
	player_path = "players/" + row["DISPLAY_FIRST_LAST"] + ".xlsx"
	if path.exists(player_path):
		time_modified = time.ctime(os.path.getmtime(player_path))
		date_mod = datetime.strptime(time_modified, '%a %b %d %H:%M:%S %Y')
		if date_mod > d_one_day:
	# if path.exists(player_path) and date_mod > d_one_day:
			print(time_modified)
			print(row["DISPLAY_FIRST_LAST"] + ": Player exists... moving on")
		else:
			print(row["DISPLAY_FIRST_LAST"])
			player_id = row["PERSON_ID"]
			gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = seasonToGrab)
			df_player_games = gamelog_player.get_data_frames()[0]
			#print(df_player_games)
			df_player_games.to_excel("players/" + row["DISPLAY_FIRST_LAST"] + ".xlsx")
			time.sleep(1)			
	else:
		print(row["DISPLAY_FIRST_LAST"])
		player_id = row["PERSON_ID"]
		gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = seasonToGrab)
		df_player_games = gamelog_player.get_data_frames()[0]
		#print(df_player_games)
		df_player_games.to_excel("players/" + row["DISPLAY_FIRST_LAST"] + ".xlsx")
		time.sleep(1)
	# except:
		# print("timeout: ignoring")

# comall.to_excel("all.xlsx")
# player_dict = players.get_active_players()
# print(player_dict)
# for player in player_dict:
# 	if player['is_active'] == True:
# 		try:
# 			# print(player)
# 			# player_id = player['id']
# 			# gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = seasonToGrab)
# 			# #print(gamelog_player.get_data_frames()[0])
# 			# df_player_games = gamelog_player.get_data_frames()[0]
# 			# #print(df_player_games)
# 			# df_player_games.to_excel("players/" + player["full_name"] + ".xlsx")
# 			# time.sleep(1)



# 			player_path = "players/" + player["full_name"] + ".xlsx"
# 			time_modified = time.ctime(os.path.getmtime(player_path))
# 			date_mod = datetime.strptime(time_modified, '%a %b %d %H:%M:%S %Y')
# 			if path.exists(player_path) and date_mod > d_one_day:
# 				print(time_modified)
# 				print(player["full_name"] + ": Player exists... moving on")
# 			else:
# 				print(player)
# 				player_id = player['id']
# 				gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = seasonToGrab)
# 				df_player_games = gamelog_player.get_data_frames()[0]
# 				#print(df_player_games)
# 				df_player_games.to_excel("players/" + player["full_name"] + ".xlsx")
# 				time.sleep(1)
# 		except:
# 			print("timeout: ignoring")



rpg_high = 0.0
fgpct_high = 0.0
ftpct_high = 0.0
fg3_high = 0.0
points_high = 0.0
steals_high = 0.0
blk_high = 0.0
ato_high = 0.0
ast_high = 0.0

# print(d)
for filename in os.listdir("players/"):
	if "xlsx" in filename:
		player_name = filename.replace(".xlsx", "")
		print(player_name)
		temp_player = pd.read_excel("players/" + filename, header=0, index_col=1)
		# print(player_name + " index: " + str(len(temp_player.index)))
		if len(temp_player.index) != 0:
			if temp_player["FGM"].sum() > 3:
				temp_player["GAME_DATE"] = pd.to_datetime(temp_player['GAME_DATE'])
				count = 0
				for index, row in temp_player.iterrows():
					if str(row["GAME_DATE"]) > timestamp:
						count = count + 1

				if temp_player["TOV"].sum() == 0:
					atopct = 0
				else:
					atopct = temp_player["AST"].sum() / temp_player["TOV"].sum()
				if atopct > ato_high:
					ato_high = atopct

				fgpg = temp_player["FGA"].sum() / len(temp_player.index)
				ftpg = temp_player["FTA"].sum() / len(temp_player.index)

				astavg = temp_player["AST"].sum() / len(temp_player.index)
				if astavg > ast_high:
					ast_high = astavg

				blkavg = temp_player["BLK"].sum() / len(temp_player.index)
				if blkavg > blk_high:
					blk_high = blkavg
				stlavg = temp_player["STL"].sum() / len(temp_player.index)
				if stlavg > steals_high:
					steals_high = stlavg
				ptsavg = temp_player["PTS"].sum() / len(temp_player.index)
				if ptsavg > points_high:
					points_high = ptsavg

				if temp_player["FGA"].sum() == 0 or temp_player["FGM"].sum() == 0:
					fgpct = 0.0
				else:
					fgpct = temp_player["FGM"].sum() / temp_player["FGA"].sum()
				if fgpct > fgpct_high:
					fgpct_high = fgpct

				fg3 = temp_player["FG3M"].sum() / len(temp_player.index)
				if fg3 > fg3_high:
					fg3_high = fg3

				if temp_player["FTM"].sum() == 0 or temp_player["FTA"].sum() == 0:
					ftpct = 0.0
				else:
					ftpct = temp_player["FTM"].sum() / temp_player["FTA"].sum()
				if ftpct > ftpct_high:
					ftpct_high = ftpct
				rpg = temp_player["REB"].sum() / len(temp_player.index)
				if rpg > rpg_high:
					rpg_high = rpg
				newrow = [{'Name': player_name, 'Games Played': len(temp_player.index), "Last 7 Days": count, 'FGPG': fgpg, 'FTPG': ftpg, 'FGPCT': fgpct, 'FTPCT': ftpct, 'RPG': rpg, 'FG3': fg3, 'PTSAVG': ptsavg, "STLAVG": stlavg, "BLKAVG": blkavg, "ASTAVG": astavg, "ATO": atopct}]
				final = final.append(newrow, ignore_index=True)
print(final)
print(final["FGPG"].std())
print(final["FGPCT"].std())
FG_STDEV = final["FGPG"].std()
FG_MEAN = final["FGPG"].mean()
FGP_STDEV = final["FGPCT"].std()
FGP_MEAN = final["FGPCT"].mean()
FT_STDEV = final["FTPG"].std()
FT_MEAN = final["FTPG"].mean()
FTP_STDEV = final["FTPCT"].std()
FTP_MEAN = final["FTPCT"].mean()
AST_STDEV = final["ASTAVG"].std()
AST_MEAN = final["ASTAVG"].mean()
ATO_STDEV = final["ATO"].std()
ATO_MEAN = final["ATO"].mean()
stdev_high = 0.0
stdev_low = 0.0
stdevft_high = 0.0
stdevft_low = 0.0
astdev_high = 0.0
astdev_low = 0.0


for index, row in final.iterrows():
	STDEV_FG = ((float(row["FGPG"])) - FG_MEAN) / FG_STDEV
	STDEV_FGP = ((float(row["FGPCT"])) - FGP_MEAN) / FGP_STDEV
	STDEV_TOTAL = STDEV_FG + (STDEV_FGP * 3)
	final.at[index, "STDEV_FG"] = STDEV_FG
	final.at[index, "STDEV_FGP"] = STDEV_FGP
	final.at[index, "STDEV_TOTAL"] = STDEV_TOTAL	
	if STDEV_TOTAL > stdev_high:
		stdev_high = STDEV_TOTAL
	if STDEV_TOTAL < stdev_low:
		stdev_low = STDEV_TOTAL

	STDEV_FT = ((float(row["FTPG"])) - FT_MEAN) / FT_STDEV
	STDEV_FTP = ((float(row["FTPCT"])) - FTP_MEAN) / FTP_STDEV
	STDEVFT_TOTAL = STDEV_FT + (STDEV_FTP * 3)
	final.at[index, "STDEV_FT"] = STDEV_FT
	final.at[index, "STDEV_FTP"] = STDEV_FTP
	final.at[index, "STDEVFT_TOTAL"] = STDEVFT_TOTAL	
	if STDEVFT_TOTAL > stdevft_high:
		stdevft_high = STDEVFT_TOTAL
	if STDEVFT_TOTAL < stdevft_low:
		stdevft_low = STDEVFT_TOTAL

	STDEV_AST = ((float(row["ASTAVG"])) - AST_MEAN) / AST_STDEV
	STDEV_ATO = ((float(row["ATO"])) - ATO_MEAN) / ATO_STDEV
	STDEVAST_TOTAL = STDEV_AST + (STDEV_ATO * 3)
	final.at[index, "STDEV_AST"] = STDEV_AST
	final.at[index, "STDEV_ATO"] = STDEV_ATO
	final.at[index, "STDEVAST_TOTAL"] = STDEVAST_TOTAL	
	if STDEVAST_TOTAL > astdev_high:
		astdev_high = STDEVAST_TOTAL
	if STDEVAST_TOTAL < astdev_low:
		astdev_low = STDEVAST_TOTAL


stdev_high = stdev_high + abs(stdev_low)
stdevft_high = stdevft_high + abs(stdevft_low)
astdev_high = astdev_high + abs(astdev_low)
for index, row in final.iterrows():
	# STDEV_FG = ((float(row["FGPCT"])) - FGP_MEAN) / FGP_STDEV
	# STDEV_FGP = ((float(row["FGPG"])) - FG_MEAN) / FG_STDEV
	STDEV_TOTAL = row["STDEV_TOTAL"] + abs(stdev_low)
	STDEV_TOTAL = (STDEV_TOTAL / stdev_high) * 100
	STDEVFT_TOTAL = row["STDEVFT_TOTAL"] + abs(stdevft_low)
	STDEVFT_TOTAL = (STDEVFT_TOTAL / stdevft_high) * 100
	STDEVAST_TOTAL = row["STDEVAST_TOTAL"] + abs(astdev_low)
	STDEVAST_TOTAL = (STDEVAST_TOTAL / astdev_high) * 100
	FG_VALUE = (float(row["FGPCT"]) / (fgpct_high - 0.0)) * 100
	FT_VALUE = (float(row["FTPCT"]) / (ftpct_high - 0.0)) * 100
	RB_VALUE = (float(row["RPG"]) / (rpg_high - 0.0)) * 100
	FG3_VALUE = (float(row["FG3"]) / (fg3_high - 0.0)) * 100
	PTS_VALUE = (float(row["PTSAVG"]) / (points_high - 0.0)) * 100	
	STL_VALUE = (float(row["STLAVG"]) / (steals_high - 0.0)) * 100
	BLK_VALUE = (float(row["BLKAVG"]) / (blk_high - 0.0)) * 100	
	ATO_VALUE = (float(row["ATO"]) / (ato_high - 0.0)) * 100
	AST_VALUE = (float(row["ASTAVG"]) / (ast_high - 0.0)) * 100	
	final.at[index, "STDEV_TOTAL"] = STDEV_TOTAL 
	final.at[index, "STDEVFT_TOTAL"] = STDEVFT_TOTAL
	final.at[index, "STDEVAST_TOTAL"] = STDEVAST_TOTAL	
	final.at[index, "FG_VALUE"] = FG_VALUE
	# final.at[index, "STDEV_FG"] = STDEV_FG
	# final.at[index, "STDEV_FGP"] = STDEV_FGP
	final.at[index, "FT_VALUE"] = FT_VALUE
	final.at[index, "RB_VALUE"] = RB_VALUE
	final.at[index, "FG3_VALUE"] = FG3_VALUE
	final.at[index, "PTS_VALUE"] = PTS_VALUE
	final.at[index, "STL_VALUE"] = STL_VALUE
	final.at[index, "BLK_VALUE"] = BLK_VALUE
	final.at[index, "ATO_VALUE"] = ATO_VALUE
	final.at[index, "AST_VALUE"] = AST_VALUE
	TOTAL_VALUE = (STDEV_TOTAL * .11) + (STDEVFT_TOTAL * .11) + (RB_VALUE * .16) + (FG3_VALUE * .11) + (PTS_VALUE * .11) + (STL_VALUE * .11) + (BLK_VALUE * .11) + (STDEVAST_TOTAL * .11) + (AST_VALUE * .5)
	final.at[index, "TOTAL_VALUE"] = TOTAL_VALUE
	final.at[index, "TOTAL_ADJUSTED"] = TOTAL_VALUE * row["Games Played"]
	final.at[index, "TOTAL_LAST_7"] = TOTAL_VALUE * row["Last 7 Days"]
	# lst = ["LeBron James", "James Harden"]
	# final.style.apply(lambda x: ['background: lightgreen' if (set(lst).intersection(x.values)) else '' for i in x], axis=1)

final = final.sort_values(by=['TOTAL_VALUE'], ascending=False)
final.to_excel("percentages.xlsx")




# [SEASON_ID, Player_ID, Game_ID, GAME_DATE, MATCHUP, WL, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT, FTM, FTA, FT_PCT, OREB, DREB, REB, AST, STL, BLK, TOV, PF, PTS, PLUS_MINUS, VIDEO_AVAILABLE]


# dd more weighted
# fga weighted
# base on number of minutes

# FG% 11%
# FT% 11%
# 3PM 11%
# REB 16%
# A/TO 16%
# STL 11%
# BLK 11%
# DD
# PTS 11%
