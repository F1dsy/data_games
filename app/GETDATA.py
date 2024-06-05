from os import listdir
import json
import random

import pandas as pd

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
        data = pd.read_csv("app/data/games/" + Games[i] + ".csv", dtype={"Country": str, "Value": float}, sep=",")

        for j in range(len(data)):
            cursor.execute(selectCountry, (data.iloc[j, 0],))
            if cursor.fetchone() is not None:
                cursor.execute(insertDATAROW, (i, data.iloc[j, 0], data.iloc[j, 1]))
        
        # Insert highscore and scoreprogress for test users:
        for j in range(len(testusersandpassword)):
            high = random.randint(0,9)
            cursor.execute(insertHighscore, (j, i, high))
            
            progress = random.randint(0,9)
            Country1 = getRandomCountry(conn, i, "Not a Country")[0]
            Country2 = getRandomCountry(conn, i, Country1)[0]
            cursor.execute(insertSCOREProgress, (j, i, progress, Country1, Country2))

    cursor.close()


def getRandomCountry(conn, Dataset_id:int, Country_name:str):
    #get random row from schema.sql
    cursor = conn.cursor()
    cursor.execute("SELECT Country FROM Datarow WHERE Dataset_ID = %s AND Country != %s ORDER BY RANDOM() LIMIT 1;", (Dataset_id, Country_name))
    data = cursor.fetchone()
    cursor.close()
    return data

def getCountryValueAndCode(conn, Dataset_id:int, Country_name:str):
    cursor = conn.cursor()
    cursor.execute("SELECT Value FROM Datarow WHERE Dataset_ID = %s AND Country = %s", (Dataset_id, Country_name))
    value = cursor.fetchone()[0]
    cursor.execute("SELECT Code FROM Countries WHERE Country = %s", (Country_name,))
    code = cursor.fetchone()[0]
    cursor.close()
    return value, code.lower()

def getGames(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT Dataset_Name FROM Dataset order by Dataset_ID")
    data = cursor.fetchall()
    cursor.close()
    return data

def searchGames(conn, Game):
    cursor = conn.cursor()
    cursor.execute("SELECT Dataset_Name FROM Dataset where regexp_count(Dataset_Name,%s, 1, 'i') > 0 order by Dataset_ID", (Game,))
    data = cursor.fetchall()
    cursor.close()
    return data

def getDatasetID(conn, Game):
    cursor = conn.cursor()
    cursor.execute("SELECT Dataset_ID FROM Dataset WHERE Dataset_Name = %s", (Game,))
    data = cursor.fetchone()[0]
    cursor.close()
    return data

def getLeaderboard(conn, Game_id):
    query = "Select Rank, name, User_ID, score FROM Leaderboard WHERE Dataset_ID = %s"
    cursor = conn.cursor()
    cursor.execute(query, (Game_id,))
    data = cursor.fetchall()
    cursor.close()
    return data

def getUsersFromLeaderboard(conn, Game, username):
    cursor = conn.cursor()
    cursor.execute("SELECT Rank, name, User_ID, score FROM Leaderboard natural join Users WHERE Dataset_ID = %s AND regexp_count(name,%s, 1, 'i') > 0 order by Rank", (Game, username))
    data = cursor.fetchall()
    cursor.close()
    return data

def getHighscore(conn, User_ID, Dataset_ID):
    cursor = conn.cursor()
    cursor.execute("SELECT Score FROM Highscore WHERE User_ID = %s AND Dataset_ID = %s", (User_ID, Dataset_ID))
    data = cursor.fetchone()
    cursor.close()
    return data

def updateHighscore(conn, User_ID, Dataset_ID, Score):
    cursor = conn.cursor()
    cursor.execute("UPDATE Highscore SET Score = %s WHERE User_ID = %s AND Dataset_ID = %s", (Score, User_ID, Dataset_ID))
    cursor.close()

def getSCOREprogress(conn, User_ID, Dataset_ID):
    cursor = conn.cursor()
    cursor.execute("SELECT Score, Country1, Country2 FROM ScoreProgress WHERE User_ID = %s AND Dataset_ID = %s", (User_ID, Dataset_ID))
    data = cursor.fetchone()
    cursor.close()
    return data

def updateSCOREprogress(conn, User_ID, Dataset_ID, Score, Country1, Country2):
    cursor = conn.cursor()
    cursor.execute("UPDATE ScoreProgress SET Score = %s, Country1 = %s, Country2 = %s WHERE User_ID = %s AND Dataset_ID = %s", (Score, Country1, Country2, User_ID, Dataset_ID))
    cursor.close()

def deleteSCOREprogress(conn, User_ID, Dataset_ID):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ScoreProgress WHERE User_ID = %s AND Dataset_ID = %s", (User_ID, Dataset_ID))
    cursor.close()

def insertSCOREprogress(conn, User_ID, Dataset_ID, Score, Country1, Country2):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ScoreProgress(User_ID, Dataset_ID, Score, Country1, Country2) VALUES (%s, %s, %s, %s, %s)", (User_ID, Dataset_ID, Score, Country1, Country2))
    cursor.close()

def giveAnswer(conn, User_ID, Dataset_ID, Answer):
    Score, Country1, Country2 = getSCOREprogress(conn, User_ID, Dataset_ID)
    Value1, Code1 = getCountryValueAndCode(conn, Dataset_ID, Country1)
    Value2, Code2 = getCountryValueAndCode(conn, Dataset_ID, Country2)

    if Value1 == Value2 or (Value1 > Value2 and Answer == "Lower") or (Value1 < Value2 and Answer == "Higher"):
        Score += 1
        newCountry = getRandomCountry(conn, Dataset_ID, Country2)[0]
        updateSCOREprogress(conn, User_ID, Dataset_ID, Score, Country2, newCountry)
    else:
        deleteSCOREprogress(conn, User_ID, Dataset_ID)
        Highscore = getHighscore(conn, User_ID, Dataset_ID)[0]
        if Score > Highscore:
            updateHighscore(conn, User_ID, Dataset_ID, Score)

def insertUser(conn, name, password):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(User_ID) FROM Users")
    User_ID = cursor.fetchone()[0] + 1
    cursor.execute("INSERT INTO Users(User_ID, name, Password) VALUES (%s, %s, %s)", (User_ID, name, password))
    cursor.close()

def updateUser(conn, User_ID, name, password):
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET name = %s, Password = %s WHERE User_ID = %s", (name, password, User_ID))
    cursor.close()

def deleteUser(conn, User_ID):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE User_ID = %s", (User_ID,))
    cursor.close()

def floatToString(inputValue):
    return (f"{inputValue:,.2f}").rstrip('0').rstrip('.')

