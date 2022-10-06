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

my_team_games = {
			'Russell Westbrook': 4,
			'Lauri Markkanen': 4,
			'Kevin Durant': 4,
			'Pascal Siakam': 2,
			'Mo Bamba': 4,
			'Tyler Herro': 3,
			'Kyle Kuzma': 3,
			'Nikola Vucevic': 3,
			'DeMar DeRozan': 3,
			'Jarred Vanderbilt': 4,
			'Cade Cunningham': 4,
			'Al Horford': 3,
			'Alec Burks': 4}

other_team = {
			'Lonzo Ball': 3,
			'Darius Garland': 4,
			'Anthony Edwards': 4,
			'Wendell Carter Jr.': 4,
			'Karl-Anthony Towns': 4,
			'Derrick Rose': 4,
			'Desmond Bane': 4,
			'Harrison Barnes': 3,
			'Isaiah Stewart': 4,
			'Luguentz Dort': 4}

scoreboard = [0.0,0.0,0,0,0.0,0,0,0,0]
final = pd.DataFrame()
for j, k in other_team.items():
	filename = j + ".xlsx"
	player_name = filename.replace(".xlsx", "")	
	temp_player = pd.read_excel("players/" + filename, header=0, index_col=1)
	temp_player["GAME_DATE"] = pd.to_datetime(temp_player['GAME_DATE'])
	fgm = fga = fta = ftm = ast = tov = reb = blk = stl = fg3m = pts = dd = count = 0.0
	# fgp_sum = ftp_sum = ato_sum = reb_sum = blk_sum = stl_sum = fg3m_sum = pts_sum = dd_sum = 0
	for index, row in temp_player.iterrows():
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
		if (row['REB'] >= 10 or row['AST'] >= 10) and row['PTS'] >= 10:
			dd = dd + 1
		pts = pts + row["PTS"]
	# fgp_sum = fgp_sum + float((fgm / fga) * k)
	# ftp_sum = ftp_sum + float((ftm / fta) * k)
	# fg3m_sum = fg3m_sum + (fg3m + k)
	# reb_sum = reb_sum + (reb + k)
	# ato_sum = ato_sum + float((ast / tov) * k)
	# stl_sum = stl_sum + (stl + k)
	# blk_sum = blk_sum + (blk + k)
	# dd_sum = dd_sum + (dd+ k)
	# pts_sum = pts_sum + (pts + k)
	# print(str(fgp_sum) + " " + str(ftp_sum)  + " " + str(ato_sum) + " " + str(reb_sum) + " " + str(blk_sum)  + " " + str(stl_sum)  + " " + str(fg3m_sum)  + " " + str(pts_sum) + " " + str(dd_sum))



	newrow = [{'Name': player_name, "Last 7 Days": k, 
	'FGM': fgm  * (other_team[player_name]/count), 
	'FGA': fga * (other_team[player_name]/count), 
	'FTM': ftm * (other_team[player_name]/count), 
	'FTA': fta * (other_team[player_name]/count), 
	'AST': ast * (other_team[player_name]/count), 
	'TOV': tov * (other_team[player_name]/count), 
	'REB': reb * (other_team[player_name]/count), 
	"FG3M": fg3m * (other_team[player_name]/count), 
	"STL": stl * (other_team[player_name]/count), 
	"BLK": blk * (other_team[player_name]/count), 
	"DD": dd * (other_team[player_name]/count), 
	"PTS": pts * (other_team[player_name]/count)}]
	final = final.append(newrow, ignore_index=True)

final.to_excel("otherteam.xlsx")
fgp_sum = float(final["FGM"].sum()) / float(final["FGA"].sum())
ftp_sum = float(final["FTM"].sum() / final["FTA"].sum())
fg3m_sum = final["FG3M"].sum()
reb_sum = final["REB"].sum()
ato_sum = float(final["AST"].sum()) / float(final["TOV"].sum())
stl_sum = final["STL"].sum()
blk_sum = final["BLK"].sum()
dd_sum = final["DD"].sum()
pts_sum = final["PTS"].sum()
print(str(round(fgp_sum, 2)) + 
		" " + str(round(ftp_sum, 2))  + 
		" " + str(round(fg3m_sum, 2)) + 
		" " + str(round(reb_sum, 2))  + 
		" " + str(round(ato_sum, 2))  + 
		" " + str(round(stl_sum, 2)) + 
		" " + str(round(blk_sum, 2))  + 
		" " + str(round(dd_sum, 2)) + 
		" " + str(round(pts_sum)))


scoreboard = [fgp_sum, ftp_sum, fg3m_sum, reb_sum, ato_sum, stl_sum, blk_sum, dd_sum, pts_sum]


d_now = datetime.now() + timedelta(days=-7)
timestamp = d_now.strftime("%Y-%m-%d %H:%M:%S")
l = list(combinations(my_team_games, 10))
all_scores = {}
# count_games = 0
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
mean_highest = 0.0
ftmean = 0.0
for i in l:
	final = pd.DataFrame()
	dict_players = {}
	for ll in i:
		dict_players[ll] = my_team_games[ll]
	for p, k in dict_players.items():
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
			if (row['REB'] >= 10 or row['AST'] >= 10) and row['PTS'] >= 10:
				dd = dd + 1
			pts = pts + row["PTS"]
		newrow = [{'Name': player_name, "Last 7 Days": k, 
		'FGM': fgm  * (my_team_games[player_name]/count) , 
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
	fgmean = (fgp_sum - scoreboard[0]) / scoreboard[0]
	ftp_sum = float(final["FTM"].sum() / final["FTA"].sum())
	if (ftp_sum >= scoreboard[1]):
		winner = winner + 1
		ftmean = (ftp_sum - scoreboard[1]) / scoreboard[1]
	fg3m_sum = final["FG3M"].sum()
	if (fg3m_sum >= scoreboard[2]):
		winner = winner + 1
	f3mean = (fg3m_sum - scoreboard[2]) / scoreboard[2]
	reb_sum = final["REB"].sum()
	if (reb_sum >= scoreboard[3]):
		winner = winner + 1
	rebmean = (reb_sum - scoreboard[3]) / scoreboard[3]
	ato_sum = float(final["AST"].sum()) / float(final["TOV"].sum())
	if (ato_sum >= scoreboard[4]):
		winner = winner + 1
	atomean = (ato_sum - scoreboard[4]) / scoreboard[4]
	stl_sum = final["STL"].sum()
	if (stl_sum >= scoreboard[5]):
		winner = winner + 1
	stlmean = (stl_sum - scoreboard[5]) / scoreboard[5]
	blk_sum = final["BLK"].sum()
	if (blk_sum >= scoreboard[6]):
		winner = winner + 1
	blkmean = (blk_sum - scoreboard[6]) / scoreboard[7]
	dd_sum = final["DD"].sum()
	if (dd_sum >= scoreboard[7]):
		winner = winner + 1
	ddmean = (dd_sum - scoreboard[7]) / scoreboard[7]
	pts_sum = final["PTS"].sum()
	if (pts_sum >= scoreboard[8]):
		winner = winner + 1
	ptsmean = (pts_sum - scoreboard[8]) / scoreboard[8]
	newrow = [{'FGP': fgp_sum, 'FTP': ftp_sum, 'ATO': ato_sum, 'REB': reb_sum, "FG3M": fg3m_sum, "STL": stl_sum, "BLK": blk_sum, "DD": dd_sum, "PTS": pts_sum}]
	all_outcomes = all_outcomes.append(newrow, ignore_index=True)
	if winner >= 5:
		print("WINNER!!")
		print(i)
		print(str(round(fgp_sum, 2)) + 
		" " + str(round(ftp_sum, 2))  + 
		" " + str(round(fg3m_sum, 2)) + 
		" " + str(round(reb_sum, 2))  + 
		" " + str(round(ato_sum, 2))  + 
		" " + str(round(stl_sum, 2)) + 
		" " + str(round(blk_sum, 2))  + 
		" " + str(round(dd_sum, 2)) + 
		" " + str(round(pts_sum)))
		print("it beat:")
	if mean_highest == 0.0 or fgmean +ftmean + f3mean + rebmean +atomean + stlmean + blkmean + ddmean + ptsmean > mean_highest:
		mean_highest = fgmean +ftmean + f3mean + rebmean +atomean + stlmean + blkmean + ddmean + ptsmean
		print("Closest...")
		print(i)
		print(str(round(fgp_sum, 2)) + 
		" " + str(round(ftp_sum, 2))  + 
		" " + str(round(fg3m_sum, 2)) + 
		" " + str(round(reb_sum, 2))  + 
		" " + str(round(ato_sum, 2))  + 
		" " + str(round(stl_sum, 2)) + 
		" " + str(round(blk_sum, 2))  + 
		" " + str(round(dd_sum, 2)) + 
		" " + str(round(pts_sum)))		



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

