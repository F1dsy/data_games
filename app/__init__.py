from flask import Flask, render_template
import psycopg2

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
#cursor = conn.cursor()

insertUSER = "INSERT INTO Users(User_ID, Username, Password) VALUES (%d, %s, %s)"
insertDATASET = "INSERT INTO Dataset(Dataset_ID, Dataset_Name) VALUES (%d, %s)"
insertDATAROW = "INSERT INTO Datarow(Dataset_ID, Country, Value) VALUES (%d, %s, %f)"
insertHighscore = "INSERT INTO Highscore(User_ID, Dataset_ID, Score) VALUES (%d, %d, %d)"
insertSCOREProgress = "INSERT INTO ScoreProgress(User_ID, Dataset_ID, Score, Country1, Country2) VALUES (%d, %d, %d, %s, %s)"

updateUSER = "UPDATE Users SET Username = %s, Password = %s WHERE User_ID = %d"
updateHighscore = "UPDATE Highscore SET Score = %d WHERE User_ID = %d AND Dataset_ID = %d"
updateSCOREProgress = "UPDATE ScoreProgress SET Score = %d, Country1 = %s, Country2 = %s WHERE User_ID = %d AND Dataset_ID = %d"

deleteUSER = "DELETE FROM Users WHERE User_ID = %d"




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
