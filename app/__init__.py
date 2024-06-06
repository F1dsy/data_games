import webbrowser  
import re

from flask import Flask, render_template, request
import psycopg2

try:
    import app.GETDATA
except:
    import GETDATA


# FILL IN:
DBusername = 'postgres'
DBpassword = 'password123'
DBname = 'postgres'
DBhost = '127.0.0.1'


app = Flask(__name__)

app.config["SECRET_KEY"] = "fc089b9218301ad987914c53481bff04"

# set your own database
db = f"dbname='{DBname}' user='{DBusername}' host='{DBhost}' password = '{DBpassword}'"
conn = psycopg2.connect(db)
conn.autocommit = True
GETDATA.create_tables(conn)
webbrowser.open(f"http://{DBhost}:5000/", new=0)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = GETDATA.searchGames(conn, request.form['Game'])
    else:
        data = GETDATA.getGames(conn)

    data = [(re.sub('_', ' ', v[0]),)+v for v in data]
    return render_template("homepage.html", data=data)


@app.route("/<Game>", methods=["GET", "POST"])
def Game(Game, User_ID=None):
    Game_id = GETDATA.getDatasetID(conn, Game)
    Game = (re.sub('_', ' ', Game),Game)

    if User_ID == None:
        User_ID = 0

    if request.method == "POST":
        GETDATA.giveAnswer(conn, User_ID, Game_id, request.form['Answer'])


    if GETDATA.getSCOREprogress(conn, User_ID, Game_id) == None:
        Country1 = GETDATA.getRandomCountry(conn, Game_id, "Not a Country")[0]
        Country2 = GETDATA.getRandomCountry(conn, Game_id, Country1)[0]
        Score = 0
        GETDATA.insertSCOREprogress(conn, User_ID, Game_id, Score, Country1, Country2)
    else:
        Score, Country1, Country2 = GETDATA.getSCOREprogress(conn, User_ID, Game_id)

    Highscore = GETDATA.getHighscore(conn, User_ID, Game_id)[0]
    Value1, Code1 = GETDATA.getCountryValueAndCode(conn, Game_id, Country1)
    Value2, Code2 = GETDATA.getCountryValueAndCode(conn, Game_id, Country2)
    Value1 = GETDATA.floatToString(Value1)
    Value2 = GETDATA.floatToString(Value2)
    return render_template("game.html", Country1=Country1, Country2=Country2, Value1=Value1, Value2=Value2, Code1=Code1, Code2=Code2, Score=Score, Highscore=Highscore, Game=Game)

@app.route("/<Game>/Leaderboard", methods=["GET", "POST"])
def Leaderboard(Game):
    Game_id = GETDATA.getDatasetID(conn, Game)
    Game = (re.sub('_', ' ', Game),Game)
    if request.method == "POST":
        data = GETDATA.getUsersFromLeaderboard(conn, Game_id, request.form['GameName'])
    else:
        data = GETDATA.getLeaderboard(conn, Game_id)
    return render_template("leaderboard.html", data=data, Game=Game)
