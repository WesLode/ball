from datetime import date,datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore

import pandas as pd
# import json
from utils import export_to_file
# print(date.today())

# def json_to_file(f_name, sometext):
#     json_object = json.dumps(sometext, indent=4)
#     with open(f'data/{f_name}.json', "w") as outfile:
#         outfile.write(json_object)

def box_score_search(gameid):
    box = boxscore.BoxScore(game_id=gameid)
    x = box.get_dict()['game']['homeTeam']
    x = box.get_dict()
    export_to_file("box_Score", x)

quarter_dic = {
    "teamName":None,
    "1stQuarter": None,
    "2ndQuarter": None,
    "3rdQuarter": None,
    "4thQuarter": None
}

# Today's Score Board
board  = scoreboard.ScoreBoard(
    timeout=12
)
data2 = list()
day_total_game = board.games.get_dict()
for game in day_total_game:
    data_result = quarter_dic
    for j in game:
        temp_dict = dict()
        if j in ["homeTeam", "awayTeam"]:
            temp_dict['gameId'] = game['gameId']
            temp_dict['gameClock'] = game['gameClock']
            temp_dict['team'] = game[j]['teamName']
            temp_dict['side'] = j.replace('Team','')
            for k in game[j]['periods']:
                if k['period'] == 1:
                    temp_dict['1stQuarter'] = k['score']
                if k['period'] == 2:
                    temp_dict['2ndQuarter'] = k['score']
                if k['period'] == 3:
                    temp_dict['3rdQuarter'] = k['score']
                if k['period'] == 4:
                    temp_dict['4thQuarter'] = k['score']
            data2 += [temp_dict]
    data2 += [{}]
    # break
board.get_dict()
# print(data2)
scoreboard_data = board.get_dict()['scoreboard']['games']

# y = pd.json_normalize(board.get_dict()['scoreboard']['games'])
y = pd.json_normalize(data2)
print(y )
export_to_file('liveScore', board.get_dict())
print(f'Data at data/liveScore.csv')