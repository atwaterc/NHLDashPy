import requests
import json
import traceback
from datetime import datetime

# 10
# 2021020494
# define game info like shots, goals, assists, etc
full_game_data = {}
full_game_data['home'] = {}
full_game_data['away'] = {}
full_game_data['periods'] = {}
full_game_data['miscInfo'] = {}
full_game_data['miscInfo']['gameId'] = 0

# define stats for players during game
player_game_stats = {}

# define Maple Leaf team stats
maple_team_stats = {}
maple_team_stats['stats'] = {}
maple_team_stats['rankings'] = {}

def getData():
    team_schedule_data = "https://statsapi.web.nhl.com/api/v1/schedule?teamId=10"
    schedule_response = requests.get(team_schedule_data)

    data = schedule_response.json()
    #print(data)

    if data['dates']:
        try:
            gameId = 2021020501
            #gameId = data['dates'][0]['games'][0]['gamePk']
            full_game_data['miscInfo']['gameId'] = gameId

            print(gameId)

            # get and format game start time
            start_time = data['dates'][0]['games'][0]['gameDate']
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            full_game_data['miscInfo']['gameDate'] = start_time.strftime("%b %d, %Y %H:%M")

            game_data = "https://statsapi.web.nhl.com/api/v1/schedule?gamePk=" + str(gameId) + "&expand=schedule.teams,schedule.linescore"

            game_response = requests.get(game_data)
            game = game_response.json()

            #print(game)
            linescore_data = game['dates'][0]['games'][0]['linescore']
            team_data = game['dates'][0]['games'][0]['teams']
            #print(team_data)

            full_game_data['miscInfo']['venue'] = game['dates'][0]['games'][0]['venue']['name']
            # define home team record and info
            home_team = team_data.get('home')
            home_record = home_team.get('leagueRecord')
            home_name = home_team.get('team')

            # fill team info home dict
            full_game_data['home']['id'] = home_name.get('id', 999)
            full_game_data['home']['name'] = home_name.get('name', 0)
            full_game_data['home']['abbreviation'] = home_name.get('abbreviation')
            full_game_data['home']['wins'] = home_record.get('wins')
            full_game_data['home']['losses'] = home_record.get('losses')
            full_game_data['home']['ot'] = home_record.get('ot')
            full_game_data['home']['totalPoints'] = (full_game_data['home']['wins'] * 2) + full_game_data['home']['ot']

            #print(full_game_data['home'])

            # define away team record and info
            away_team = team_data.get('away')
            away_record = away_team.get('leagueRecord')
            away_name = away_team.get('team')

            # fill team info away dict
            full_game_data['away']['id'] = away_name.get('id', 999)
            full_game_data['away']['name'] = away_name.get('name', 0)
            full_game_data['away']['abbreviation'] = away_name.get('abbreviation')
            full_game_data['away']['wins'] = away_record.get('wins')
            full_game_data['away']['losses'] = away_record.get('losses')
            full_game_data['away']['ot'] = away_record.get('ot')
            full_game_data['away']['totalPoints'] = (full_game_data['away']['wins'] * 2) + full_game_data['away']['ot']

            #print(full_game_data['away'])

            # define linescore for game, periods
            full_game_data['miscInfo']['currentPeriod'] = linescore_data.get('currentPeriod')
            full_game_data['miscInfo']['gameStatus'] = linescore_data.get('currentPeriodTimeRemaining')

            full_game_data['home']['totalShots'] = 0
            full_game_data['home']['totalGoals'] = 0

            full_game_data['away']['totalShots'] = 0
            full_game_data['away']['totalGoals'] = 0

            # fill data for each period played

            for period in linescore_data['periods']:
                # if period.get('num') == 1:
                #     cur_per = 'First'
                # elif period.get('num') == 2:
                #     cur_per = 'Second'
                # else:
                #     cur_per = 'Third'
                cur_per = period.get('num')

                if full_game_data['periods'].get(cur_per) is None:
                    full_game_data['periods'][cur_per] = {}

                full_game_data['periods'][cur_per]['home'] = period.get('home')
                full_game_data['periods'][cur_per]['away'] = period.get('away')

                full_game_data['home']['totalShots'] += full_game_data['periods'][cur_per]['home']['shotsOnGoal']
                full_game_data['home']['totalGoals'] += full_game_data['periods'][cur_per]['home']['goals']

                full_game_data['away']['totalShots'] += full_game_data['periods'][cur_per]['away']['shotsOnGoal']
                full_game_data['away']['totalGoals'] += full_game_data['periods'][cur_per]['away']['goals']

            #print(full_game_data)
            return full_game_data
        except Exception as ex:
            print('Something happened')
            return None
            print(traceback.format_exc())

    else:
        return 'No Game Today'


def getPlayerData():
    if full_game_data['miscInfo']['gameId'] == 0:
        return 'No Game Today'

    gameId = full_game_data['miscInfo']['gameId']

    game_player_data_url = "https://statsapi.web.nhl.com/api/v1/game/"+ str(gameId) +"/boxscore"
    game_player_data_response = requests.get(game_player_data_url)
    game_player_data = game_player_data_response.json()

    #for player in game_player_data['teams']['away']:
    #print(game_player_data)

def getMapleLeafsData():
    maple_data_url = "https://statsapi.web.nhl.com/api/v1/teams/10/stats"
    maple_data_response = requests.get(maple_data_url)
    maple_data = maple_data_response.json()

    # maple_team_stats['GP'] = maple_data.get('stats')
    maple_team_stats['stats'] = maple_data['stats'][0]['splits'][0]['stat']
    maple_team_stats['rankings'] = maple_data['stats'][1]['splits'][0]['stat']

    return maple_team_stats
#print(getMapleLeafsData())
#print(getPlayerData())
