from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

load_dotenv()
source_Table = os.environ.get("MYSQL_TABLE_SOURCE")
connection = connect(
		host=os.environ.get("MYSQL_HOST"),
		user=os.environ.get("MYSQL_USER"),
		password=os.environ.get("MYSQL_PASSWORD"),
		database=os.environ.get("MYSQL_DB"))
try:
	cursor = connection.cursor()
	table_query = "DROP TABLE IF EXISTS " + source_Table
	table_query += "; CREATE TABLE " + source_Table
	table_query += " (sources TEXT NOT NULL);"
	cursor.execute(table_query)
	while(connection.next_result()):
		pass	
	srtCat = open(os.environ.get("SRTNPATH")+"/srt.cat", "r")
	for line in srtCat:
		if (line[:3].lower() == "sou"):
			source_query = "INSERT INTO " + source_Table + " (sources) VALUES (\"" + line.split(" ")[7].replace("\n", "") + "\")"
			cursor.execute(source_query)
			connection.commit()
	srtCat.close()
	connection.close()	
except Error as e:
	print(e)
