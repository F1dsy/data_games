

DROP TABLE IF EXISTS Users CASCADE;
CREATE TABLE IF NOT EXISTS Users(
	User_ID integer PRIMARY KEY,
	name varchar(60),
	password varchar(120)
);

DROP TABLE IF EXISTS Dataset CASCADE;
CREATE TABLE IF NOT EXISTS Dataset(
	Dataset_ID integer PRIMARY KEY,
	Dataset_Name varchar(60) UNIQUE
);

DROP TABLE IF EXISTS Countries CASCADE;
CREATE TABLE IF NOT EXISTS Countries(
	Country varchar(60) PRIMARY KEY,
	Code varchar(6) UNIQUE
);

DROP TABLE IF EXISTS Datarow CASCADE;
CREATE TABLE IF NOT EXISTS Datarow(
	Dataset_ID integer,
	Country varchar(60),
	Value Real,
	FOREIGN KEY (Dataset_ID) REFERENCES Dataset(Dataset_ID) ON DELETE CASCADE,
	FOREIGN KEY (Country) REFERENCES Countries(Country) ON DELETE CASCADE,
	PRIMARY KEY (Dataset_ID, Country)
);

DROP TABLE IF EXISTS Highscore CASCADE;
CREATE TABLE IF NOT EXISTS Highscore(
	User_ID integer,
	Dataset_ID integer,
	score integer,
	FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
	FOREIGN KEY (Dataset_ID) REFERENCES Dataset(Dataset_ID) ON DELETE CASCADE,
	PRIMARY KEY (User_ID, Dataset_ID)
);

DROP VIEW IF EXISTS Leaderboard CASCADE;
CREATE VIEW Leaderboard AS
Select Dataset_ID, ROW_NUMBER() OVER(PARTITION BY Dataset_ID ORDER BY Score DESC) AS Rank, name, User_ID, score 
FROM Highscore 
Natural join Users 
ORDER BY Score DESC;

DROP TABLE IF EXISTS ScoreProgress CASCADE;
CREATE TABLE IF NOT EXISTS ScoreProgress(
	User_ID integer,
	Dataset_ID integer,
	score integer,
	Country1 varchar(60),
	Country2 varchar(60),
	FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
	FOREIGN KEY (Dataset_ID, Country1) REFERENCES Datarow(Dataset_ID, Country) ON DELETE CASCADE,
	FOREIGN KEY (Dataset_ID, Country2) REFERENCES Datarow(Dataset_ID, Country) ON DELETE CASCADE,
	PRIMARY KEY (User_ID, Dataset_ID)
);
