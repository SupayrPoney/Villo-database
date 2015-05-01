import sqlite3
import re
import datetime
import random
from config import db_filename

# TODO should check expiry date
ISADMIN_QUERY="SELECT userID FROM admins WHERE userID=?"
LOGIN_QUERY="SELECT userID FROM users WHERE userID=? and password=?"
USER_INSERT_QUERY="INSERT INTO users (password, expiryDate, card) VALUES(?, ?, ?)"
SUBSCRIBER_INSERT_QUERY="INSERT INTO subs(userID, RFID, lastname, firstname, phone, addresscity, addresscp, addressstreet, addressnumber, subscribeDate)\
VALUES(last_insert_rowid(),?,?,?,?,?,?,?,?,?)"
TEMPUSER_INSERT_QUERY="INSERT INTO tempUsers(userID) VALUES(last_insert_rowid())"

# TODO accents etc
attr_regex = {
	# subscribers
	"lastname": "\w{2,50}",
	"firstname": "\w{2,50}",
	"phone": "[0-9]{9,10}",
	"addresscity": "[\w-]{2,50}",
	"addresscp": "[0-9]{4}",
	"addressstreet": "[\w-]{2,50}",
	"addressnumber": "[0-9]{1,4}\w?",
	# users
	"password": "[0-9]{4}",
	"card": "[0-9]{17}"
}

def login(user, password):
	global LOGIN_QUERY
	db = sqlite3.connect(db_filename)
	cursor = db.cursor()
	cursor.execute(LOGIN_QUERY, (user, password))
	result = cursor.fetchone()
	db.close()
	if result:
		return True
	else:
		return False

def register(user):
	global attr_regex
	attr_names = dict(zip(attr_regex.keys(), ["Postal code", "Phone number", "Street number", "First name", "Street name", "Last name", "Card number", "Password", "City"]))

	errors = []
	for attr, regex in attr_regex.iteritems():
		if not re.match(regex, user[attr]):
			errors.append(attr_names[attr] + " is not valid")

	# TODO generate RFID
	if errors == []:
		db = sqlite3.connect(db_filename)
		cursor = db.cursor()
		if user["validity"] == "2":
			duration = datetime.timedelta(days=365)
		elif user["validity"] == "0":
			duration = datetime.timedelta(days=1)
		elif user["validity"] == "1":
			duration = datetime.timedelta(days=7)
		cursor.execute(USER_INSERT_QUERY, (user["password"], datetime.datetime.now() + duration, user["card"]))
		if user["validity"] == "2":
			cursor.execute(SUBSCRIBER_INSERT_QUERY, 
				(random.randint(10000000000,999999999999), user["lastname"], user["firstname"],
				user["phone"], user["addresscity"], user["addresscp"], user["addressstreet"], user["addressnumber"],
				datetime.datetime.now()))
		elif user["validity"] == "0" or user["validity"] == "1":
			cursor.execute(TEMPUSER_INSERT_QUERY)
		db.commit()
		cursor.close()
		db.close()
		return None
	else:
		return errors

def isAdmin(user):
	global ISADMIN_QUERY
	db = sqlite3.connect(db_filename)
	cursor = db.cursor()
	cursor.execute(ISADMIN_QUERY, (user,))
	result = cursor.fetchone()
	db.close()
	if result:
		return True
	else:
		return False