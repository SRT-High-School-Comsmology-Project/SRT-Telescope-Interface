import os
from dotenv import load_dotenv
from pymongo import MongoClient

#Updates sources on the database
load_dotenv()
client = MongoClient(os.environ.get("CLIENT"))
SRTDb = client.SRTDatabase
sourceCollection = SRTDb.source


sourceCollection.delete_many({})
srtCat = open(os.environ.get("SRTNPATH")+"/srt.cat", "r")
for line in srtCat:
	if (line[:3].lower() == "sou"):
		sourceCollection.insert_one({
			"source": line.split(" ")[7].replace("\n", ""),
	})

srtCat.close()
