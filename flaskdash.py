from flask import Flask, render_template
from nhldash import *
#import full_game_data from nhldash

app = Flask(__name__)

hd = getData()
hdp = None
tml_stats = getMapleLeafsData()
print(tml_stats['stats'])

gameOver = False

if hd != 'No Game Today':
    hdp = getPlayerData()

#print(hd['periods'].items())
# for data in hd['periods'].values():
#     print(data)
#     print(type(data))

@app.route("/")
@app.route("/dashboard")
def home():
    return render_template('dashboard.html', hd=hd, tmls=tml_stats)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
