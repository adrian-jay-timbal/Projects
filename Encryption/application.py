import sqlite3
from helper import *
import time
# import psycopg2
# from getpass import getpass

# database connection (SQLITE)
con = sqlite3.connect("Raven.db")
db = con.cursor()

# database connection (PostgreSQL)
# con = psycopg2.connect(
# 	host="localhost",
# 	database="??????",
# 	user="????????",
# 	password="???????",
# 	port=5432
# )
# db = con.cursor()

def main(n):
	print("Menu:\n[E]ncrypt\n[D]ecrypt")
	act = input("Choose action: ")
	if act.upper() == "E":
		print("<<[Encryption sectoR]>>")
		encrypt(n)
	elif act.upper() == "D":
		print("<<[Decryption sectoR]>>")
		decrypt(n)
	else:
		print("Invalid action !")
		main(n)

def encrypt(n):
	# check how many entries in credentials are present to create new id number
	c_id = db.execute("select id from credentials")
	c_ids = len(c_id.fetchall()) + 1

	# check if the account already existed
	while True:
		acc = input("Password for what account ?: ")
		dacc = db.execute("SELECT account FROM credentials WHERE account = ? AND user_id = ?",(acc, n))
		ddacc = dacc.fetchall()
		try:
			if acc.lower() == ddacc[0][0]:
				print(f"You already have {acc} password stored.")
				continue
		except:
			break
		
	# execute the encryption algorithm
	hash = encryptor(pwp(), ky())
	print("Encrypting your password...")
	time.sleep(1)
	print("Encryption Successful...")
	print("Storing your password...")
	db.execute("INSERT INTO credentials VALUES(?,?,?,?)", (c_ids, hash, acc, n))
	con.commit()
	time.sleep(1)
	print("Password stored successfully.")
	print("Do you want to do another transaction ?[Y]es [N]o")
	while True:
		new_trans = input()
		if new_trans.lower() == "y":
			return main(n)
		elif new_trans.lower() == "n":
			break
		else:
			print("Invalid input use options [Y]es or [N]o")
			continue

def decrypt(n):
	while True:
		acc = input("Show password for what account ?: ")
		dacc = db.execute("SELECT account FROM credentials WHERE account = ? AND user_id = ?",(acc, n))
		ddacc = dacc.fetchall()
		try:
			if acc.lower() == ddacc[0][0]:
				print("Password found...\nDecrypting please wait....")
				time.sleep(2)
				break
		except:
			print(f"You don't have password for {acc} account.")
			while True:
				resp = input(f"Enter\n[T] to try again\n[C] to store password for {acc} account or\n[Q] to quit the program\n")
				if resp.upper() == "C":
					time.sleep(0.5)
					return encrypt(n)
				elif resp.upper() == "T":
					time.sleep(0.5)
					break
				elif resp.upper() == "Q":
					print("Exiting the program....")
					time.sleep(1)
					print("Done!")
					quit()
				else:
					print("Invalid input! use the options provided.")
					continue
			continue
	s_pass = db.execute("SELECT hash FROM credentials WHERE account = ? AND user_id = ?",(acc, n))
	n_pass = s_pass.fetchall()
	password = decryptor(n_pass[0][0])
	print(f"{acc} : {password}")
	print("Do you want to do another transaction ?[Y]es [N]o")
	while True:
		new_trans = input()
		if new_trans.lower() == "y":
			return main(n)
		elif new_trans.lower() == "n":
			break
		else:
			print("Invalid input use options [Y]es or [N]o")
			continue

def login():
	print("<=LOGIN=>")
	# Get user input
	names = input("Username: ")
	pas = input("Password: ")

	# query the database for given credentials
	u = db.execute("SELECT * FROM users WHERE name = ? and password = ?",(names, pas))
	users = u.fetchall()

	#check if the given credentials are present in the database
	try:
		if names == users[0][1] and pas == users[0][2]:
			print("User verified! ")
			time.sleep(0.5)
			user_id = users[0][0]
			return user_id
	except:
		print("Invalid username or password!")

	# if user fails to login, they will asked for certain command
	while True:
		resp = input("Enter\n[T] to try again\n[C] to create new user account or\n[Q] to quit the program\n")
		if resp.upper() == "C":
			time.sleep(0.5)
			return new_user()
		elif resp.upper() == "T":
			time.sleep(0.5)
			return login()
		elif resp.upper() == "Q":
			print("Exiting the program....")
			time.sleep(1)
			print("Done!")
			quit()
		else:
			print("Invalid input! use the options provided.")
			continue

def new_user():
	print("<=REGISTRATION=>")
	while True:

		# query database for given user name to ensure no duplication
		name = input("Username: ")
		users = db.execute("SELECT name FROM users WHERE name = ?",(name,))
		u_list = users.fetchall()
		try:
			if name == u_list[0][0]:
				print("Username already exist! Please use a different username.")
				continue
		except:
			print(f"Username {name} is accepted.\nProceeding....")
			break
	while True:
		pwd = input("Register your password: ")
		pwd_r = input("Confirm your password: ")
		if pwd == pwd_r:
			break
		else:
			continue

	# after checking, insertion to database of new user details
	u_id = db.execute("select id from users")
	u_ids = len(u_id.fetchall()) + 1
	db.execute("INSERT INTO users VALUES(?,?,?)",(u_ids, name, pwd))
	con.commit()
	print("Processing please wait.....")
	time.sleep(1)
	print("Registration complete. Proceeding to login...")
	time.sleep(1)
	return

while True:
		promt = input("[L]ogin\n[R]egistier\n")
		if promt.upper() == "L":
			break
		elif promt.upper() == "R":
			new_user()
			continue
		else:
			print("Invalid Input !")
			continue

user = verify(login())
main(user)

# close databse connection
con.close()
# 01/31/2023