from flask import Flask, render_template
import psycopg2
import GETDATA
import webbrowser

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

GETDATA.create_tables(conn)
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
  
webbrowser.open("http://127.0.0.1:5000", new=0, autoraise=True)

@app.route("/")
def hello_world():
    return render_template("homepage.html")
