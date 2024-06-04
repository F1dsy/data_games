from os import listdir
import pandas as pd
import json
import random

random.seed(1337)

def create_tables(conn):
    cursor = conn.cursor()

    # Creating tables:
    cursor.execute(open("app/schema.sql", "r").read())

    # Insert countries:
    insertCountry = "INSERT INTO Countries(Country, Code) VALUES (%s, %s)"

    f = open("app/data/countries/countries.json", "r")
    countriesdata = json.load(f)
    f.close()

    for country in countriesdata.keys():
        cursor.execute(insertCountry, (countriesdata[country], country))

    # Insert test users:
    insertUSER = "INSERT INTO Users(User_ID, name, Password) VALUES (%s, %s, %s)"
    testusersandpassword = [("Jonas", "1234"), ("Kasper", "asdasd"), ("Mads", "dwew"), ("Mikkel", "1234"), ("Andreas", "1234"),
                            ("Morten", "876"), ("Mathias", "44343dsa"), ("Jens", "1234"), ("Jesper", "1234"), ("Lars", "1234")]

    for i in range(len(testusersandpassword)):
        cursor.execute(insertUSER, (i, testusersandpassword[i][0], testusersandpassword[i][1]))

    # Insert datasets:
    Games = []
    filenames = listdir("app/data/games")
    for name in filenames:
        if name.endswith(".csv"):
            Games.append(name[:-4])

    insertDATASET = "INSERT INTO Dataset(Dataset_ID, Dataset_Name) VALUES (%s, %s)"
    insertDATAROW = "INSERT INTO Datarow(Dataset_ID, Country, Value) VALUES (%s, %s, %s)"
    selectCountry = "SELECT * FROM Countries WHERE Country = %s"
    insertHighscore = "INSERT INTO Highscore(User_ID, Dataset_ID, Score) VALUES (%s, %s, %s)"
    insertSCOREProgress = "INSERT INTO ScoreProgress(User_ID, Dataset_ID, Score, Country1, Country2) VALUES (%s, %s, %s, %s, %s)"

    for i in range(len(Games)):
        # Insert dataset:
        cursor.execute(insertDATASET, (i, Games[i]))

        # Insert datarows:
        data = pd.read_csv("app/data/games/" + Games[i] + ".csv")
        for j in range(len(data)):
            cursor.execute(selectCountry, (data.iloc[j, 0],))
            if cursor.fetchone() is not None:
                cursor.execute(insertDATAROW, (i, data.iloc[j, 0], data.iloc[j, 1]))
        
        # Insert highscore and scoreprogress for test users:
        for j in range(len(testusersandpassword)):
            high = random.randint(0,9)
            cursor.execute(insertHighscore, (j, i, high))
            
            progress = random.randint(0,9)
            Country1 = getRandomCountry(conn, i, "NOT A COUNTRY")[0]
            Country2 = getRandomCountry(conn, i, Country1)[0]
            cursor.execute(insertSCOREProgress, (j, i, progress, Country1, Country2))

    cursor.close()


def getRandomCountry(conn, Dataset_id:int, Country_name:str):
    #get random row from schema.sql
    cursor = conn.cursor()
    cursor.execute("SELECT Country, Value FROM Datarow WHERE Dataset_ID = %s AND Country != %s ORDER BY RANDOM() LIMIT 1;", (Dataset_id, Country_name))
    data = cursor.fetchone()
    cursor.close()
    return data



updateUSER = "UPDATE Users SET Username = %s, Password = %s WHERE User_ID = %s"
updateHighscore = "UPDATE Highscore SET Score = %s WHERE User_ID = %s AND Dataset_ID = %s"
updateSCOREProgress = "UPDATE ScoreProgress SET Score = %s, Country1 = %s, Country2 = %s WHERE User_ID = %s AND Dataset_ID = %s"

deleteUSER = "DELETE FROM Users WHERE User_ID = %s"

selectHighscore = "SELECT score FROM Highscore WHERE User_ID = %s AND Dataset_ID = %s"
selectSCOREprogress = "SELECT score, Country1, Country2 FROM ScoreProgress WHERE User_ID = %s AND Dataset_ID = %s"
selectTOP10 = "SELECT user_id, name, score FROM Highscore Natural join Users WHERE Dataset_ID = %s ORDER BY Score DESC LIMIT 10"


