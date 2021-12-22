import requests
import json
import traceback

# 10
# 2021020494
full_game_data = {}
full_game_data['home'] = {}
full_game_data['away'] = {}
full_game_data['periods'] = {}

team_schedule_data = "https://statsapi.web.nhl.com/api/v1/schedule?teamId=3"
schedule_response = requests.get(team_schedule_data)

data = schedule_response.json()
#print(data)

if data['dates']:
    try:
        gameId = data['dates'][0]['games'][0]['gamePk']

        print(gameId)

        game_data = "https://statsapi.web.nhl.com/api/v1/schedule?gamePk=" + str(gameId) + "&expand=schedule.teams,schedule.linescore"

        game_response = requests.get(game_data)
        game = game_response.json()

        #print(game)
        linescore_data = game['dates'][0]['games'][0]['linescore']
        team_data = game['dates'][0]['games'][0]['teams']
        #print(team_data)

        full_game_data['venue'] = game['dates'][0]['games'][0]['venue']['name']
        # define home team record and info
        home_team = team_data.get('home')
        home_record = home_team.get('leagueRecord')
        home_name = home_team.get('team')

        # fill team info home dict
        full_game_data['home']['id'] = home_name.get('id', 999)
        full_game_data['home']['name'] = home_name.get('name', 0)
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
        full_game_data['away']['wins'] = away_record.get('wins')
        full_game_data['away']['losses'] = away_record.get('losses')
        full_game_data['away']['ot'] = away_record.get('ot')
        full_game_data['away']['totalPoints'] = (full_game_data['away']['wins'] * 2) + full_game_data['away']['ot']

        #print(full_game_data['away'])

        # define linescore for game, periods
        full_game_data['currentPeriod'] = linescore_data.get('currentPeriod')

        full_game_data['home']['totalShots'] = 0
        full_game_data['away']['totalShots'] = 0

        # fill data for each period played
        for period in linescore_data['periods']:
            cur_per = period.get('num')
            print(cur_per)

            if full_game_data['periods'].get(cur_per) is None:
                print('Creating period Key')
                full_game_data['periods'][cur_per] = {}

            full_game_data['periods'][cur_per]['home'] = period.get('home')
            full_game_data['periods'][cur_per]['away'] = period.get('away')

            full_game_data['home']['totalShots'] += full_game_data['periods'][cur_per]['home']['shotsOnGoal']
            full_game_data['away']['totalShots'] += full_game_data['periods'][cur_per]['away']['shotsOnGoal']

        print(full_game_data)



    except Exception as ex:
        print('Something happened')
        print(traceback.format_exc())

else:
    print('No Game Today')


