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
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import json_to_file, markdown_report


with open('ref.json','r') as f1:
    all_header = json.load(f1)


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

def export_standing():
    col_map = dict()
    raw_data = leaguestandingsv3.LeagueStandingsV3().get_dict()
    json_to_file('rawdata',raw_data)
    standings_header = raw_data['resultSets'][0]['headers']


    for i in range(len(standings_header)):
        if raw_data['resultSets'][0]['headers'][i] in data_header:
            col_map[ raw_data['resultSets'][0]['headers'][i]] = i


    Con_rank = list()

    for i in raw_data['resultSets'][0]['rowSet']:
        team_item = dict()
        for j in col_map:
            team_item[j] = i[col_map[j]]
        Con_rank += [team_item]

    y = pd.json_normalize(Con_rank)
    y.rename(columns={'PlayoffRank': 'Standing'}, inplace=True)

    standing_col = [
        'Standing',
        'TeamCity',
        'TeamName',
        'Record',
        'L10'
    ]

    report_structure = {
        "West": "Western Conference",
        "East": "Eastern Conference",
    }

    standing_report = str()
    standing_report = "# NBA Standing\n\n"
    for i in report_structure:
        standing_report+= f'## {report_structure[i]}\n\n'
        standing_report += f'{y.loc[y.Conference == i][standing_col].to_markdown(index=False)}'
        standing_report +='\n\n\n'

    markdown_report('standing',standing_report,'app/static/report')
    

if __name__ == "__main__":
    export_standing()
    print(len(all_header['all_header']))
    print(f'gg')


