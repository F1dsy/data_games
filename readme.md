## Initialization ✔

Clone / download repository files and run the following to install the required packages (preferably within a venv):

    pip install -r requirements.txt

Create a database in pgAdmin, it should preferably be named "flask_project" and the password for the postgres user should be "password123". 
You can change the password with this SQL query:

    ALTER USER postgres PASSWORD '<new-password>';

Or you can change the db settings in \_\_init\_\_.py

## Run the webapp

Now you can run the working app with:

    flask run