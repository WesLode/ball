from asyncio import Task
from datetime import datetime

import requests
import json 
import unicodedata
from nba_api.live.nba.endpoints import boxscore, scoreboard
from utils import json_to_file, make_dir, get_nested, add_to_list
import pandas as pd
import json

def game_summary(date, game):
    y = pd.json_normalize(game)
    y['id'] = y['id'].astype('int') % 100
    y[['timeout','matchUp','score','sortlist']] = None
    y.set_index('id')
    quarter_score_full = list()
    quarter_header = list()
    for index, row in y.iterrows():
        y.loc[index,'timeout'] = f'{row['awayTimeout']}-{row['homeTimeout']}'
        y.loc[index,'matchUp'] = f'{row['awayTeam']}-{row['homeTeam']}'
        y.loc[index,'score'] = f'{row['awayScore']}-{row['homeScore']}'
        try:
            x = datetime.strptime(row['startTime'], "%Y-%m-%dT%H:%M:%S-04:00")
        except:
            x=datetime.strptime("2025-04-01T19:30:00-04:00", "%Y-%m-%dT%H:%M:%S-04:00")
        y.loc[index,'startTime'] = x.strftime("%H:%M")
        y.loc[index, 'sortlist'] = int(x.strftime("%H:%M").replace(':','')) * int(row['id'])
        quarter_score = dict()
        quarter_score['id'] = row['id']
        for i in range(len(row['awayQuarter'])):
            if i <4:
                quarter_header=add_to_list(quarter_header,f'Q{i+1}')
                quarter_score[f'Q{i+1}'] = f'{row['awayQuarter'][i]['score']}-{row["homeQuarter"][i]['score']}'
            else:
                quarter_header=add_to_list(quarter_header,f'OT{i-3}')


                quarter_score[f'OT{i-3}'] = f'{row['awayQuarter'][i]['score']}-{row["homeQuarter"][i]['score']}'
        
        quarter_score_full +=[quarter_score]
    qq = pd.DataFrame(quarter_score_full)
    y = y.join(qq.set_index('id'), on='id')


    y.rename(columns={
        'timeout': 'T/O',
        },inplace=True)
    
    y.sort_values(by=['sortlist'],inplace=True)
    
    with open(f'data/{date}_gameSummary.txt', 'w') as f1:
        f1.write(y[[
            'startTime',
            'matchUp',
            'gameClock',
            'T/O',
            'score',
            ]+quarter_header].to_markdown(index=False))
    return True

def map_data(stat, csv_map):
    player_dict = dict()
    path_map = pd.read_csv(csv_map)
    for index, row in path_map.iterrows():
        try:
            player_dict[f'{row['info']}'] = get_nested(stat, row['path'].split("."))
        except KeyError:
            player_dict[f'{row['info']}'] = None
    return player_dict

def player_stats(game, d_dir):
    print('•')
    result = dict()
    result['homeTeam'] = list()
    result['awayTeam'] = list()
    team = ['homeTeam', 'awayTeam']
    for side in team:
        for i in game[side]['players']:
            result[side] += [map_data(i,'report.csv')]
    
    
    with open(f'data/{d_dir}/player/{game['gameCode'][-6::]}.md', 'w') as f1:
        f1.write(f'# Player Stat\n\n')
        for side in team:    
            side_pd = pd.json_normalize(result[side])
            for index, row in side_pd.iterrows():
                if row['status'] == 'ACTIVE':
                    side_pd.loc[index,'status'] = f'#'
                else:
                    side_pd.loc[index,'status'] = f''

                if row['starter'] =='1':
                    side_pd.loc[index,'name'] = f'(s){row['name']}'
                side_pd.loc[index, 'minutes'] = row['minutes'].replace('PT','')
            side_pd['name'] = side_pd['name'].apply(
                lambda x: unicodedata.normalize('NFD',x).encode('ascii', 'ignore')
            )
            side_pd['minutes'] = side_pd['minutes'].apply(
                lambda x : x.replace('M','m')
            )
            side_pd.rename(columns={
                'minutes': 'mins',
                'status': '*',
                'played':'1'
            },inplace=True)
            side_pd.drop(
                columns=[
                    'starter'
                ],inplace=True
            )
            f1.write(f'## {side.upper()}\n\n')
            f1.write(side_pd.to_markdown(index=False))
            f1.write('\n\n')
    
    return result


def today_day():
    board = scoreboard.ScoreBoard().get_dict()
    # json_to_file('test',board)

    match_code = dict()
    result = dict()
    for games in board['scoreboard']['games']:
        match_code[games['gameCode'].split('/')[1]] = {
            'code':games['gameId'],
            'status':games['gameStatus'], 
            'games':games}

    result['gameDate'] = board['scoreboard']['gameDate'].replace('-','')
    result['gameCode'] = match_code
    json_to_file(f'{result['gameDate']}_game',result)
    return result

def score_table():
    full_talbe = list()
    today_game = today_day()
    match_code = today_game['gameCode']
    if False:
        match_code = {
                    "GSWORL": {
                "code": "0022400845",
                "status": 3},
                    "MINDEN": {
                "code": "0022401102",
                "status": 3
                }
        }
    d_dir = today_game['gameDate']
    make_dir(f'data/{d_dir}/player')
    for games in match_code:
        if match_code[games]['status'] in [2,3]:
            game_boxScore = boxscore.BoxScore(match_code[games]['code']).game.get_dict()
            player_stat = player_stats(game_boxScore, d_dir)
        else:
            game_boxScore = match_code[games]['games']
            game_boxScore['gameEt'] = game_boxScore['gameEt'].replace('Z','-04:00')
        json_to_file(f'{d_dir}/boxScore_{games}',game_boxScore)
        full_talbe += [map_data(game_boxScore, 'scoreboard.csv')]


    if len(full_talbe) > 0:
        game_summary(d_dir, full_talbe)



if __name__ == "__main__":
    score_table()


