from datetime import date,datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard, boxscore
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import leaguestandingsv3

import pandas as pd
import numpy as np
import matplotlib as mpl
import json

def json_to_file(f_name, sometext):
    json_object = json.dumps(sometext, indent=4)
    with open(f'data/{f_name}.json', "w") as outfile:
        outfile.write(json_object)

data_header =[
    # "SeasonID",
    "TeamID",
    "TeamCity",
    "TeamName",
    "WINS",
    "LOSSES",
    "WinPCT", 
    "Record",
    "PlayoffRank",
    "L10",
    "Conference",
]

col_map = dict()

raw_data = leaguestandingsv3.LeagueStandingsV3().get_dict()

standings_header = raw_data['resultSets'][0]['headers']


for i in range(len(standings_header)):
    if raw_data['resultSets'][0]['headers'][i] in data_header:
        col_map[ raw_data['resultSets'][0]['headers'][i]] = i


Con_rank = list()

for i in raw_data['resultSets'][0]['rowSet']:
    team_item = dict()
    for j in col_map:
        team_item[j] = i[col_map[j]]
    # print(team_item)
    Con_rank += [team_item]

y = pd.json_normalize(Con_rank)
y.rename(columns={'PlayoffRank': 'Standing'}, inplace=True)
eastern_rank = y.loc[y.Conference == "East"]
western_rank = y.loc[y.Conference == "West"]
# print(eastern_rank)
# print(western_rank)

standing_col = [
    # 'PlayoffRank',
    'Standing',
    'TeamCity',
    'TeamName',
    'Record',
    'L10'
]

# print(western_rank.style.highlight_max())
with open('data/Standing.txt', 'w') as f1:
    f1.write('Western Conference\n')
    f1.write(western_rank[standing_col].to_markdown(index=False))
    f1.write('\n\n\n\n')
    f1.write('Eastern Conference\n')
    f1.write(eastern_rank[standing_col].to_markdown(index=False))