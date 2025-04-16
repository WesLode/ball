import requests
import json

api_link = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard'

res = requests.get(api_link)

# print(res)
response = json.loads(res.text)
