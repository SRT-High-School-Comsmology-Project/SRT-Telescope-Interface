import time
import glob, os, sys
import signal, subprocess
from dotenv import load_dotenv
from cosmology_gmail import gmail_authenticate, send_message
from mysql.connector import connect, Error

'''
NEEDS pymongo
	pymongo[srv]
	python 3.6+
	google-api-python-client
	google-auth-httplib2
	google-auth-oauthlib
	credentials.json - Includes credentials for write gmail
	mysql-connector-python
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
connection = connect(
		host=os.environ.get("MYSQL_HOST"),
		user=os.environ.get("MYSQL_USER"),
		password=os.environ.get("MYSQL_PASSWORD"),
		database=os.environ.get("MYSQL_DB"))
#Collection for submitted commands
queryTB = os.environ.get("MYSQL_TABLE_QUERIES")
#Collection for measured commands
resultTB = os.environ.get("MYSQL_TABLE_RESULTS")
cursor = connection.cursor()

#Default COMMAND file - cmd.txt
#Changes need to be reflected in srt.cat
while(True):	
	readDoc = 0

	selectQueries = f"SELECT * FROM {queryTB}"
	cursor.execute(selectQueries)
	results = cursor.fetchall()
	for res in results:
		_id = res[0]
		commandString = res[1]
		email = res[2]	
		emailFiles = []
		matchQuery = f"SELECT * FROM {resultTB} WHERE command = \"{commandString}\""
		cursor.execute(matchQuery)
		matchResult = cursor.fetchall()
		
		#Write commands to cmdFile
		writeDataToFile("./cmd.txt", commandString)
		
		#Create new srtn process	
		srtn = subprocess.Popen("./srtn", stdout=subprocess.DEVNULL, 
			stderr=subprocess.DEVNULL, shell=True, preexec_fn=os.setsid)
			
		#Ensures that image files is created
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
		
		
		#Reads postScript plot to data to upload	
		plot = readDataFromFile(plotFile)	

		#Reads outputfile to data
		output = glob.glob("./*.rad")
		dataFile = output[0]
		data = readDataFromFile(dataFile)	
		
		emailFiles.append(dataFile)
		emailFiles.append(plotFile)

		readDoc += 1
		insertQuery = (f"INSERT INTO {resultTB} (command, plot, data) "
				"VALUES (%s, %s, %s)") 
		data = (commandString, plot, data)
		cursor.execute(insertQuery, data)
		connection.commit()
		
		deletedQuery = (f"DELETE FROM {queryTB} WHERE _ID={_id}")
		cursor.execute(deletedQuery)
		connection.commit()
		send_message(service, email, "test", "test", emailFiles)
		os.remove(plotFile)
		os.remove(dataFile)

		
	if (readDoc == 0):
		time.sleep(600) #Sleeps for 10 minutes if no file is found


	
