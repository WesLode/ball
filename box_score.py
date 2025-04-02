from asyncio import Task
from datetime import datetime

import requests
import json 
import unicodedata
from nba_api.live.nba.endpoints import boxscore, scoreboard
from utils import json_to_file, make_dir, get_nested
import pandas as pd
import json

def game_summary(date, game):
    y = pd.json_normalize(game)
    y['id'] = y['id'].astype('int') % 100
    y[['1','2','3','4','timeout','matchUp','score']] = None
    y.assign
    for index, row in y.iterrows():
        y.loc[index,'timeout'] = f'{row['awayTimeout']}-{row['homeTimeout']}'
        y.loc[index,'matchUp'] = f'{row['awayTeam']}-{row['homeTeam']}'
        y.loc[index,'score'] = f'{row['awayScore']}-{row['homeScore']}'
        try:
            x = datetime.strptime(row['startTime'], "%Y-%m-%dT%H:%M:%S-04:00")
        except:
            x=datetime.strptime("2025-04-01T19:30:00-04:00", "%Y-%m-%dT%H:%M:%S-04:00")
        y.loc[index,'startTime'] = x.strftime("%H:%M")
        for i in range(1,5):
            temp = pd.DataFrame({str(i):[f'{row['awayQuarter'][i-1]['score']}-{row["homeQuarter"][i-1]['score']}']}, index=[index])
            y.update(temp)


    # y.sort_values(by=['startTime','id'])
    y_report=y[['id',
                'startTime',
                'matchUp',
                'gameClock',
                'timeout',
                'score',
                '1','2','3','4']]
    y_report.rename(columns={
        # 'gameClock':'test',
        'timeout': 'T/O',
        '1':'Q1',
        '2':'Q2',
        '3': 'Q3',
        '4': 'Q4'
        },inplace=True)
    # print(y)

    
    # sort table
    y_report.sort_values(by=['startTime','id'])
    
    with open(f'data/{date}_gameSummary.txt', 'w') as f1:
        f1.write(    y_report[[
            'startTime',
            'matchUp',
            'gameClock',
            'T/O',
            'score',
            'Q1','Q2','Q3','Q4'
            ]].to_markdown(index=False))
    return 'Yes'

def test_True(x):
    return x == '1'

def map_data(stat, csv_map):
    player_dict = dict()
    path_map = pd.read_csv(csv_map)
    for index, row in path_map.iterrows():
        try:
            player_dict[f'{row['info']}'] = get_nested(stat, row['path'].split("."))
        except KeyError:
            player_dict[f'{row['info']}'] = None
    return player_dict

def get_player(game, d_dir):
    result = dict()
    result['homeTeam'] = list()
    result['awayTeam'] = list()
    team = ['homeTeam', 'awayTeam']
    for side in team:
        for i in game[side]['players']:
            result[side] += [map_data(i,'report.csv')]

    for side in team:    
        side_pd = pd.json_normalize(result[side])
        side_pd['name'] = side_pd['name'].apply(
            lambda x: unicodedata.normalize('NFD',x).encode('ascii', 'ignore')
        )
        with open(f'data/{d_dir}/player/{game[side]['teamName']}.txt', 'w') as f1:
            f1.write(side_pd.to_markdown(index=False))
    
    return result


def today_day():
    board = scoreboard.ScoreBoard().get_dict()
    json_to_file('test',board)

    match_code = dict()
    result = dict()
    for games in board['scoreboard']['games']:
        match_code[games['gameCode'].split('/')[1]] = {
            'code':games['gameId'],
            'status':games['gameStatus'], 
            'games':games}

    result['gameDate'] = board['scoreboard']['gameDate'].replace('-','')
    result['gameCode'] = match_code
    json_to_file('today_game',result)
    return result

def score_table():
    full_talbe = list()
    today_game = today_day()
    match_code = today_game['gameCode']
    d_dir = today_game['gameDate']
    make_dir(f'data/{d_dir}/player')
    for games in match_code:
        if match_code[games]['status'] in [2,3]:
            game_boxScore = boxscore.BoxScore(match_code[games]['code']).game.get_dict()
            player_stat = get_player(game_boxScore, d_dir)
        else:
            game_boxScore = match_code[games]['games']
            game_boxScore['gameEt'] = game_boxScore['gameEt'].replace('Z','-04:00')
        json_to_file(f'{d_dir}/boxScore_{games}',game_boxScore)
        full_talbe += [map_data(game_boxScore, 'scoreboard.csv')]


    if len(full_talbe) > 0:
        game_summary(d_dir, full_talbe)



if __name__ == "__main__":
    score_table()
    # print(f'gg')


