from os import listdir
import pandas as pd
import json


def create_tables(conn):
    # Creating tables:
    cursor = conn.cursor() 
    cursor.execute(open("app/schema.sql", "r").read())
    cursor.close()

    # Insert countries:
    insertCountry = "INSERT INTO Countries(Country, Code) VALUES (%s, %s)"

    f = open("app/data/countries/countries.json", "r")
    countriesdata = json.load(f)
    f.close()

    cursor = conn.cursor()
    for country in countriesdata.keys():
        cursor.execute(insertCountry, (countriesdata[country], country))
    cursor.close()

    # Insert datasets:
    Games = []
    filenames = listdir("app/data/games")
    for name in filenames:
        if name.endswith(".csv"):
            Games.append(name[:-4])

    insertDATASET = "INSERT INTO Dataset(Dataset_ID, Dataset_Name) VALUES (%s, %s)"
    insertDATAROW = "INSERT INTO Datarow(Dataset_ID, Country, Value) VALUES (%s, %s, %s)"
    selectCountry = "SELECT * FROM Countries WHERE Country = %s"

    cursor = conn.cursor()
    for i in range(len(Games)):
        cursor.execute(insertDATASET, (i, Games[i]))
        data = pd.read_csv("app/data/games/" + Games[i] + ".csv")
        for j in range(len(data)):
            cursor.execute(selectCountry, (data.iloc[j, 0],))
            if cursor.fetchone() is not None:
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


