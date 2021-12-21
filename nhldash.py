import requests
import json
# 10

home = {}
away = {}

team_schedule_data = "https://statsapi.web.nhl.com/api/v1/schedule?teamId=14"
response = requests.get(team_schedule_data)

data = response.json()

gameId = data['dates'][0]['games'][0]['gamePk']
print(type(gameId))

game_data = "https://statsapi.web.nhl.com/api/v1/schedule?gamePk=" + str(gameId) + "&expand=schedule.teams,schedule.linescore"

responses = requests.get(game_data)
game = responses.json()

print(gameId)
#print(game)

team_data = game['dates'][0]['games'][0]['teams']
print(team_data)

# define home team record and info
home_team = team_data.get('home').get('team')
home_name = (home_team.get('name', 0))
home['name'] = home_name
#print(home_name)

# define away team record and info
away_team = team_data.get('away').get('team')
away_name = (away_team.get('name', 0))
away['name'] = away_name

print(home)
print(away)



