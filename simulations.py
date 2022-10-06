from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats import endpoints
import pandas as pd
import time
from datetime import datetime
from datetime import timedelta
import os.path
from os import path
from itertools import combinations


seasonToGrab = '2021'

my_team = ['Russell Westbrook',
			'Lauri Markkanen',
			'Kevin Durant',
			'Pascal Siakam',
			'Mo Bamba',
			'Tyler Herro',
			'Kyle Kuzma',
			'Nikola Vucevic',
			'DeMar DeRozan',
			'Jarred Vanderbilt',
			'Terry Rozier',
			'Cade Cunningham',
			'Al Horford']
my_team_games = {
			'Russell Westbrook': 2,
			'Lauri Markkanen': 4,
			'Kevin Durant': 3,
			'Pascal Siakam': 3,
			'Mo Bamba': 3,
			'Tyler Herro': 4,
			'Kyle Kuzma': 4,
			'Nikola Vucevic': 3,
			'DeMar DeRozan': 3,
			'Jarred Vanderbilt': 3,
			'Terry Rozier': 3,
			'Cade Cunningham': 2,
			'Al Horford': 3}


			# RJ Barrett 'Russell Westbrook'
d_now = datetime.now() + timedelta(days=-7)
timestamp = d_now.strftime("%Y-%m-%d %H:%M:%S")
l = list(combinations(my_team, 10))
scoreboard = [0.0,0.0,0,0,0.0,0,0,0,0]
all_scores = {}
count_games = 0
all_outcomes = pd.DataFrame()
rpg_high = 0.0
fgpct_high = 0.0
ftpct_high = 0.0
fg3_high = 0.0
points_high = 0.0
steals_high = 0.0
blk_high = 0.0
ato_high = 0.0
dd_high = 0.0
for i in l:
	final = pd.DataFrame()
	for p in i:

		filename = p + ".xlsx"
		player_name = filename.replace(".xlsx", "")
		#print(player_name)
		temp_player = pd.read_excel("players/" + filename, header=0, index_col=1)
		temp_player["GAME_DATE"] = pd.to_datetime(temp_player['GAME_DATE'])
		fgm = fga = fta = ftm = ast = tov = reb = blk = stl = fg3m = pts = dd = count = 0
		for index, row in temp_player.iterrows():
			#if str(row["GAME_DATE"]) > timestamp:
#			if count < 4:
			#if count < my_team_games[player_name]:
			count = count + 1
			fgm = fgm + row["FGM"]
			fga = fga + row["FGA"]
			fta = fta + row["FTA"]
			ftm = ftm + row["FTM"]
			fg3m = fg3m + row["FG3M"]
			reb = reb + row["REB"]
			ast = ast + row["AST"]
			tov = tov + row["TOV"]
			stl = stl + row["STL"]
			blk = blk + row["BLK"]
			if (row['REB'] or row['AST']) >= 10 and row['PTS'] >= 10:
				dd = dd + 1
			pts = pts + row["PTS"]



		# newrow = [{'Name': player_name, "Last 7 Days": count, 'FGM': fgm , 'FGA': fga, 'FTM': ftm, 'FTA': fta, 'AST': ast, 'TOV': tov, 'REB': reb, "FG3M": fg3m, "STL": stl, "BLK": blk, "DD": dd, "PTS": pts}]
		newrow = [{'Name': player_name, "Last 7 Days": count, 
		'FGM': fgm  * (my_team_games[player_name]/count), 
		'FGA': fga * (my_team_games[player_name]/count), 
		'FTM': ftm * (my_team_games[player_name]/count), 
		'FTA': fta * (my_team_games[player_name]/count), 
		'AST': ast * (my_team_games[player_name]/count), 
		'TOV': tov * (my_team_games[player_name]/count), 
		'REB': reb * (my_team_games[player_name]/count), 
		"FG3M": fg3m * (my_team_games[player_name]/count), 
		"STL": stl * (my_team_games[player_name]/count), 
		"BLK": blk * (my_team_games[player_name]/count), 
		"DD": dd * (my_team_games[player_name]/count), 
		"PTS": pts * (my_team_games[player_name]/count)}]
		final = final.append(newrow, ignore_index=True)
	final.to_excel("percentagesvhjhs.xlsx")
	winner = 0
	fgp_sum = float(final["FGM"].sum()) / float(final["FGA"].sum())
	if (fgp_sum >= scoreboard[0]):
		winner = winner + 1
	if fgp_sum > fgpct_high:
		fgpct_high = fgp_sum
	ftp_sum = float(final["FTM"].sum() / final["FTA"].sum())
	if (ftp_sum >= scoreboard[1]):
		winner = winner + 1
	if ftp_sum > ftpct_high:
		ftpct_high = ftp_sum
	fg3m_sum = final["FG3M"].sum()
	if (fg3m_sum >= scoreboard[2]):
		winner = winner + 1
	if fg3m_sum > fg3_high:
		fg3_high = fg3m_sum
	reb_sum = final["REB"].sum()
	if (reb_sum >= scoreboard[3]):
		winner = winner + 1
	if rpg_high > reb_sum:
		reb_sum = rpg_high
	ato_sum = float(final["AST"].sum()) / float(final["TOV"].sum())
	if (ato_sum >= scoreboard[4]):
		winner = winner + 1
	if ato_high > ato_sum:
		ato_sum = ato_high
	stl_sum = final["STL"].sum()
	if (stl_sum >= scoreboard[5]):
		winner = winner + 1
	if steals_high > stl_sum:
		stl_sum = steals_high
	blk_sum = final["BLK"].sum()
	if (blk_sum >= scoreboard[6]):
		winner = winner + 1
	if blk_high > blk_sum:
		blk_sum = blk_high
	dd_sum = final["DD"].sum()
	if (dd_sum >= scoreboard[7]):
		winner = winner + 1
	if dd_high > dd_sum:
		dd_sum = dd_high
	pts_sum = final["PTS"].sum()
	if (pts_sum >= scoreboard[8]):
		winner = winner + 1
	if points_high > pts_sum:
		pts_sum = points_high
	newrow = [{'FGP': fgp_sum, 'FTP': ftp_sum, 'ATO': ato_sum, 'REB': reb_sum, "FG3M": fg3m_sum, "STL": stl_sum, "BLK": blk_sum, "DD": dd_sum, "PTS": pts_sum}]
	all_outcomes = all_outcomes.append(newrow, ignore_index=True)
	if winner >= 5:
		print("WINNER!!")
		print(i)
		print(fgp_sum, ftp_sum, fg3m_sum, reb_sum, ato_sum, stl_sum, blk_sum, dd_sum, pts_sum)
		scoreboard = [fgp_sum, ftp_sum, fg3m_sum, reb_sum, ato_sum, stl_sum, blk_sum, dd_sum, pts_sum]
		#print(final.at[p['Name'], "PTS"])
	#print(i)
FGP_STDEV = all_outcomes["FGP"].std()
FGP_MEAN = all_outcomes["FGP"].mean()
FTP_STDEV = all_outcomes["FTP"].std()
FTP_MEAN = all_outcomes["FTP"].mean()
ATO_STDEV = all_outcomes["ATO"].std()
ATO_MEAN = all_outcomes["ATO"].mean()
REB_STDEV = all_outcomes["REB"].std()
REB_MEAN = all_outcomes["REB"].mean()
FG3M_STDEV = all_outcomes["FG3M"].std()
FG3M_MEAN = all_outcomes["FG3M"].mean()
STL_STDEV = all_outcomes["STL"].std()
STL_MEAN = all_outcomes["STL"].mean()
BLK_STDEV = all_outcomes["BLK"].std()
BLK_MEAN = all_outcomes["BLK"].mean()
DD_STDEV = all_outcomes["DD"].std()
DD_MEAN = all_outcomes["DD"].mean()
PTS_STDEV = all_outcomes["PTS"].std()
PTS_MEAN = all_outcomes["PTS"].mean()
highest = 0.0
for index, row in all_outcomes.iterrows():
	FG_VALUE = (float(row["FGP"]) / (fgpct_high - 0.0)) * 100
	FT_VALUE = (float(row["FTP"]) / (fgpct_high - 0.0)) * 100
	ATO_VALUE = (float(row["ATO"]) / (fgpct_high - 0.0)) * 100
	REB_VALUE = (float(row["REB"]) / (fgpct_high - 0.0)) * 100	
	FG3M_VALUE = (float(row["FG3M"]) / (fgpct_high - 0.0)) * 100
	STL_VALUE = (float(row["STL"]) / (fgpct_high - 0.0)) * 100
	BLK_VALUE = (float(row["BLK"]) / (fgpct_high - 0.0)) * 100
	DD_VALUE = (float(row["DD"]) / (fgpct_high - 0.0)) * 100
	PTS_VALUE = (float(row["PTS"]) / (fgpct_high - 0.0)) * 100
	total_std = FG_VALUE + FT_VALUE + ATO_VALUE + REB_VALUE + FG3M_VALUE + STL_VALUE + BLK_VALUE + DD_VALUE + PTS_VALUE
	if total_std > highest:
		print(row)
		highest = total_std

