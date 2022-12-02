# SRT-Cosmology-local
Program that interfaces with the SRT telescope and database through a local computer. It lauches the SRT application whenever a query is available in the database and emails the result to the submitter. 

## Prerequisites

You will need the following installed on your computer
 * [Python](https://www.python.org/downloads/) (ver 3.6 +)
 * [Git](https://git-scm.com/)
 * [SRTN](https://www.haystack.mit.edu/haystack-public-outreach/srt-the-small-radio-telescope-for-education/) (ver. 9)
 * [MYSQL Connection]
 
 ## Installation
 * `git clone <repository-url>` this repository
 * `python -m pip install mysql-connector-python dotenv google-api-python-client google-auth-httplib2 google-auth-oauthlib` 
 * `cd SRT-Cosmology-local`
 
 All files in SRT-Cosmology-local need to be moved into the srtn folder.
 
 You will need to create a file named *.env* and include the following
 ```
 SRTNPATH= #Path to srt application is located
MYSQL_HOST= "" #Host address for MYSQL Connection                                         
MYSQL_USER= "" #Username for MYSQL Connection
MYSQL_PASSWORD= "" #Password for MYSQL Connection
MYSQL_DB= "" #Database for MYSQL Connection
MYSQL_TABLE_RESULTS= "" #Table for SRT Results
MYSQL_TABLE_QUERIES= "" #Table for SRT Queries
MYSQL_TABLE_SOURCE= "" #Table for SRT Sources
```

You will need to create a file named *credentials.json* and store the Google API credentials for the application.
[More information here](https://www.thepythoncode.com/article/use-gmail-api-in-python)

[Gmail API Management](https://console.cloud.google.com/marketplace/product/google/gmail.googleapis.com?q=search&referrer=search&authuser=2&project=wired-yeti-338022)

## Running
 * `python source.py` Populates database with sources from file *srt*.*cat* 
 * `python cosmology.py` Runs the actual code continuously. Needs to be running in the background.
 *  You will be prompted to login to the gmail account inorder for the application to be able to send mail.

# TODO
* Test with actual telescope.
 
