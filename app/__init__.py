from flask import Flask, render_template, request
import psycopg2
import webbrowser

try:
    import app.GETDATA
except:
    import GETDATA


# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from flask import session
# from flask_session import Session

app = Flask(__name__)

app.config["SECRET_KEY"] = "fc089b9218301ad987914c53481bff04"

# set your own database
db = "dbname='flask_project' user='postgres' host='127.0.0.1' password = 'password123'"

conn = psycopg2.connect(db)
conn.autocommit = True

GETDATA.create_tables(conn)

# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.login_message_category = "info"

# Check Configuration section for more details
# SESSION_TYPE = 'filesystem'

#roles = ["ingen", "employee", "customer"]
#print(roles)
#mysession = {"state": "initializing", "role": "Not assingned", "id": 0, "age": 202212}
#print(mysession)

# from bank.Login.routes import Login
# from bank.Customer.routes import Customer
# from bank.Employee.routes import Employee
# app.register_blueprint(Login)
# app.register_blueprint(Customer)
# app.register_blueprint(Employee)
  
#webbrowser.open("http://127.0.0.1:5000", new=0, autoraise=True)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("homepage.html", data=GETDATA.getGames(conn))


@app.route("/<Game>", methods=["GET", "POST"])
def Game(Game, User_ID=None):
    Game_id = GETDATA.getDatasetID(conn, Game)
    if User_ID == None:
        User_ID = 1

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
    print(Value1, Code1)
    
    return render_template("game.html", Country1=Country1, Country2=Country2, Value1=Value1, Value2=Value2, Code1=Code1, Code2=Code2, Score=Score, Highscore=Highscore, Game=Game)

@app.route("/<Game>/Leaderboard", methods=["GET", "POST"])
def Leaderboard(Game):
    data = GETDATA.getLeaderboard(conn, Game)
    return render_template("leaderboard.html", data=data, Game=Game)
