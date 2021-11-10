import sqlite3
import certifi
import pymongo
import logger
from configMaker import *

logger = logger.get_logger(__name__)

# local database
conn = sqlite3.connect("speedTypeDB.db")
cur = conn.cursor()


def createLocalDBTables():
    try:
        cur.execute("CREATE TABLE results (NR INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, username TEXT NOT NULL, typeSpeed DOUBLE)")
    except:
        print("Something table go boom")


def addDataLocalDB(Username, typeSpeed):
    try:
        cur.execute(
            "INSERT INTO results (Username, typeSpeed) VALUES (?, ?)", (Username, typeSpeed))
        conn.commit()
        logger.info("Data was successfully added to a local database")
    except:
        cur.execute('DELETE FROM results')
        MigrateData()

# online database
user = "Pukitis"
password = "Student007"
cluster = "speedtypecluster"
database = "SpeedTypeCluster"
ca = certifi.where()
myclient = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.jk8qi.mongodb.net/{database}?retryWrites=true&w=majority", tlsCAFile=ca)
mydb = myclient["SpeedTypeCluster"]
mycol = mydb["SpeedTypeCluster"]


def addDataPymongo(Username, typeSpeed):
    mydict = {"Username": Username, "typeSpeed": typeSpeed}
    try:
        x = mycol.insert_one(mydict)
        logger.info("Data was successfully added to Pymongo")
    except:
        print("Couldnt add data to Pymongo")
        logger.critical("Data was not added to Pymongo")
        logger.exception("")

def getPymongoData():
    data = mycol.find({})
    logger.info("Data was successfully read from Pymongo")
    return data

def readPymongoData():
    data = getPymongoData()
    for i in data:
        print(i)

def MigrateData():
    data = getPymongoData()
    for i in data:
        addDataLocalDB(i.get("Username"), i.get("typeSpeed"))
    logger.info("Data was successfully migrated to local database")
