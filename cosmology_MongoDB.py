import time
import glob, os, sys
import signal, subprocess
from dotenv import load_dotenv
from cosmology_gmail import gmail_authenticate, send_message
from pymongo import MongoClient

'''
NEEDS pymongo
	pymongo[srv]
	python 3.6+
	google-api-python-client
	google-auth-httplib2
	google-auth-oauthlib
	credentials.json - Includes credentials for write gmail
'''
def writeDataToFile(fileName, data):
	dataLines = data.split("\n")
	_file = open(fileName, "w", encoding ="utf8")
	for line in dataLines:
		print(line, file=_file)
	_file.close()

def readDataFromFile(fileName):
	fileOutput = ""
	_file = open(fileName, "r", encoding="utf8")
	for line in _file:
		fileOutput += line
	_file.close()
	return fileOutput


load_dotenv()
service = gmail_authenticate()

#Collection for submitted commands
client = MongoClient(os.environ.get("CLIENT"))
SRTDb = client.SRTDatabase
queryCollection = SRTDb.queries
#Collection for measured commands
resultCollection = SRTDb.results


#Default COMMAND file - cmd.txt
#Changes need to be reflected in srt.cat
while(True):
	readDoc = 0
	for doc in queryCollection.find():
		emailFiles = []
		writeDataToFile("./cmd.txt", doc["command"])

		#Create new srtn process	
		srtn = subprocess.Popen("./srtn", stdout=subprocess.DEVNULL, 
			stderr=subprocess.DEVNULL, shell=True, preexec_fn=os.setsid)
		
		#Ensures that data files is created
		output = []
		while not output:
			output = glob.glob("./*.ps")
			time.sleep(10)
		plotFile = output[0]
		timeCurrent = os.path.getmtime(plotFile)
		
		#Checks whether .rad file is done being written too
		timeModified = os.path.getmtime(plotFile)
		while (timeCurrent != timeModified):
			timeCurrent = timeModified
			time.sleep(60)
			timeModified = os.path.getmtime(plotFile)
		os.killpg(os.getpgid(srtn.pid), signal.SIGKILL)
		
		
		#Reads postscript plot
		plot = readDataFromFile(plotFile)

		#Reads outputFile	
		output = glob.glob("./*.rad")
		dataFile = output[0]
		data = readDataFromFile(dataFile)

		emailFiles.append(dataFile)
		emailFiles.append(plotFile)
		
		readDoc += 1
		resultId = resultCollection.insert_one({
			"_id": doc["_id"],
			"command": doc["command"],
			"data": data,
			"image": image
		}).inserted_id
		queryCollection.find_one_and_delete({"_id": resultId})
		send_message(service, doc["email"], "test", "test", emailFiles)
		os.remove(dataFile)
		os.remove(plotFile)

	if (readDoc == 0):
		time.sleep(600) #Sleeps for 10 minutes if no file is found

