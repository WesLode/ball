import requests
import json 

import pandas as pd
import json
# print(date.today())

def json_to_file(f_name, sometext):
    json_object = json.dumps(sometext, indent=4)
    with open(f'data/{f_name}.json', "w") as outfile:
        outfile.write(json_object)

api_link = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard'

res = requests.get(api_link)
response = json.loads(res.text)
# print(response)

data2 = list()

for game in response["events"]:
    if game['id'] == '401705613' or True:
        # print(game['id'])
        # print(game['status']['displayClock'])
        for team in game['competitions'][0]['competitors']:
            temp_dict =dict()
            temp_dict['matchUp'] = game['shortName']
            temp_dict['status'] = game['status']['type']['description']
            temp_dict['period'] = game['status']['period']
            temp_dict['clock'] = game['status']['displayClock']
            temp_dict['team'] = team['team']['name']
            temp_dict['homeAway'] = team['homeAway']
            for quarter in range(len(team['linescores'])):
                temp_dict[f'quarter_{quarter + 1}'] = team['linescores'][quarter]['value']
            temp_dict['Score'] = team['score']
            print(team['team']['name'])
            data2 += [temp_dict]
        # data2 += [{}]

y = pd.json_normalize(data2)

print(y)
json_to_file('liveScore_espn',response)

# Fill the Null value for quarter
for i in range(1,5):
    # print(i)
    y.fillna({f'quarter_{i}': 0}, inplace=True)

with open('data/scoreboard_simple.txt', 'w') as f1:
    f1.write(y.to_markdown(index=False))