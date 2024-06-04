from flask import Flask, render_template
import psycopg2
from os import listdir
import pandas as pd

# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

# from flask import session
# from flask_session import Session


app = Flask(__name__)

app.config["SECRET_KEY"] = "fc089b9218301ad987914c53481bff04"

# set your own database
# db = "dbname='bank' user='postgres' host='127.0.0.1' password = 'UIS'"
db = "dbname='flask_project' user='postgres' host='127.0.0.1' password = 'password123'"
conn = psycopg2.connect(db)
conn.autocommit = True

# Creating tables:
cursor = conn.cursor() 
cursor.execute(open("app/schema.sql", "r").read())
cursor.close()

# Insert data into tables:
Games = []
filenames = listdir("app/data/games")
for name in filenames:
    if name.endswith(".csv"):
        Games.append(name[:-4])

insertDATASET = "INSERT INTO Dataset(Dataset_ID, Dataset_Name) VALUES (%s, %s)"
insertDATAROW = "INSERT INTO Datarow(Dataset_ID, Country, Value) VALUES (%s, %s, %s)"

cursor = conn.cursor()
for i in range(len(Games)):
    cursor.execute(insertDATASET, (i, Games[i]))
    data = pd.read_csv("app/data/games/" + Games[i] + ".csv")
    for j in range(len(data)):
        cursor.execute(insertDATAROW, (i, data.iloc[j, 0], data.iloc[j, 1]))
cursor.close()


insertUSER = "INSERT INTO Users(User_ID, Username, Password) VALUES (%s, %s, %s)"
insertHighscore = "INSERT INTO Highscore(User_ID, Dataset_ID, Score) VALUES (%s, %s, %s)"
insertSCOREProgress = "INSERT INTO ScoreProgress(User_ID, Dataset_ID, Score, Country1, Country2) VALUES (%s, %s, %s, %s, %s)"

updateUSER = "UPDATE Users SET Username = %s, Password = %s WHERE User_ID = %s"
updateHighscore = "UPDATE Highscore SET Score = %s WHERE User_ID = %s AND Dataset_ID = %s"
updateSCOREProgress = "UPDATE ScoreProgress SET Score = %s, Country1 = %s, Country2 = %s WHERE User_ID = %s AND Dataset_ID = %s"

deleteUSER = "DELETE FROM Users WHERE User_ID = %s"

selectHighscore = "SELECT score FROM Highscore WHERE User_ID = %s AND Dataset_ID = %s"
selectSCOREprogress = "SELECT score, Country1, Country2 FROM ScoreProgress WHERE User_ID = %s AND Dataset_ID = %s"
selectTOP10 = "SELECT user_id, name, score FROM Highscore Natural join Users WHERE Dataset_ID = %s ORDER BY Score DESC LIMIT 10"



# bcrypt = Bcrypt(app)


# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.login_message_category = "info"

# Check Configuration section for more details
# SESSION_TYPE = 'filesystem'


roles = ["ingen", "employee", "customer"]
print(roles)
mysession = {"state": "initializing", "role": "Not assingned", "id": 0, "age": 202212}
print(mysession)

# from bank.Login.routes import Login
# from bank.Customer.routes import Customer
# from bank.Employee.routes import Employee
# app.register_blueprint(Login)
# app.register_blueprint(Customer)
# app.register_blueprint(Employee)


@app.route("/")
def hello_world():
    return render_template("homepage.html")
