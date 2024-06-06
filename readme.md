## Initialization ✔

Clone / download repository files and run the following to install the required packages (preferably within a venv):

    pip install -r requirements.txt

Create a database in pgAdmin, it should preferably be named "postgres" and the password for the postgres user should be "password123". 
You can change the password with this SQL query:

    ALTER USER postgres PASSWORD '<new-password>';

Or you can change the db settings in \_\_init\_\_.py

## Run the webapp
Now you can run the working app with:

    flask run

## How the app works
We have collected data from ourworldindata.org, and with inspiration from higherlowergame.com we have created a quiz game where you can guess whether a country is higher or lower than another country on a given dataset, for example GDP, population or area. We save your highscore and have created a leaderboard with other players.\\
We use SQL to store all our data. Insert statements are included to insert the initial user and games data, and to create a new score progress when you start a new game. Update statements are used to update highscores and score progress. Delete statements are used to delete scoreprogress when you finish a game. Select statements are used to get all the game and user data when playing and when looking at the leaderboard. We have also used a view to create the leaderboard based on all the highscores.\\ 

We use regular expression matching to find the csv files in our data/games folder, and to search for games and for players on the leaderboard.