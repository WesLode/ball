import requests
import json 

import pandas as pd
import json
# print(date.today())

def json_to_file(f_name, sometext):
    json_object = json.dumps(sometext, indent=4)
    with open(f'data/{f_name}.json', "w") as outfile:
        outfile.write(json_object)

api_link = 'https://site.api.espn.com/apis/site/v3/sports/basketball/nba/scoreboard'

res = requests.get(api_link)
response = json.loads(res.text)
print(response)

for game in response["events"]:
    if game['id'] == '401705613':
        print(game['id'])
        print(game['status']['displayClock'])
        for team in game['competitions'][0]['competitors']:
            print(team['team']['name'])

json_to_file('liveScore_espn',response)