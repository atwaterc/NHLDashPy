from flask import Flask, render_template
from nhldash import *
#import full_game_data from nhldash

app = Flask(__name__)

hd = getData()
hdp = None
tml_stats = getMapleLeafsData()

gameOver = False
if hd != 'No Game Today' and hd != None:
    print('THERES A GAME TODAY GETTING PLAYER DATA')
    hdp = getPlayerData(hd['miscInfo']['gameId'])
    print(hdp['home'])
#print(hd['periods'].items())
# for data in hd['periods'].values():
#     print(data)
#     print(type(data))
# print(hd['periods'][2]['home']['shotsOnGoal'])

@app.route("/")
@app.route("/dashboard")
def home():
    return render_template('dashboard.html', hd=hd, tmls=tml_stats, hdp=hdp)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
