import requests
import json 
from nba_api.live.nba.endpoints import boxscore, scoreboard

import pandas as pd
import json

def json_to_file(f_name, sometext):
    json_object = json.dumps(sometext, indent=4)
    with open(f'data/{f_name}.json', "w") as outfile:
        outfile.write(json_object)

def get_score_board(game):
    temp_dict =dict()
    temp_dict[game['awayTeam']['teamTricode']] = game['awayTeam']['score']
    temp_dict[game['homeTeam']['teamTricode']] = game['homeTeam']['score']

def get_score_table(game):
    temp_dict =dict()
    temp_dict['Id'] = int(game['gameId'][-2:])
    temp_dict['matchUp'] = f'{game['awayTeam']['teamTricode']}@{game['homeTeam']['teamTricode']}'
    temp_dict['gameClock'] = game['gameStatusText']
    temp_dict['score'] = f'{game['awayTeam']['score']}:{game['homeTeam']['score']}'
    temp_dict['awayTimeout'] = game['awayTeam']['timeoutsRemaining']
    # temp_dict['homeTeam'] = game['homeTeam']['score']
    temp_dict['homeTimeout'] = game['homeTeam']['timeoutsRemaining']
    # for i in range(len(game['homeTeam']['periods'])):
    #     temp_dict[i+1] = game['homeTeam']['periods'][i]['score']
    return temp_dict

def get_player(game):
    temp_dict = dict()


board = scoreboard.ScoreBoard().get_dict()
match_code = dict()
for games in board['scoreboard']['games']:
    match_code[games['gameCode'].split('/')[1]] = {'code':games['gameId']
    ,'status':games['gameStatus']}
json_to_file('today_game',match_code)

full_talbe = list()
for games in match_code:
    if match_code[games]['status'] in [2,3]:
        game_boxScore = boxscore.BoxScore(match_code[games]['code']).game.get_dict()
        json_to_file(f'boxScore_{games}',game_boxScore)
        get_score_board(game_boxScore)
        full_talbe += [get_score_table(game_boxScore)]

y = pd.json_normalize(full_talbe)
y = y.sort_values(by='Id', ascending=False)
# print(y)
with open('data/full_scoreboard.txt', 'w') as f1:
    f1.write(y.to_markdown(index=True))
# json_to_file('full_scoreboard',y)



