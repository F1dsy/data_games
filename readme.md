## Initialization ✔

Clone / download repository files and run the following to install the required packages (preferably within a venv):

    pip install -r requirements.txt

Create a new database in pgAdmin (preferably named flask_project)


## Add data to tables

Run the python file GETDATA to get the csv files to populate the sql database

    python3 GETDATA.py


## Run the webapp

Now you can run the working app

    flask run