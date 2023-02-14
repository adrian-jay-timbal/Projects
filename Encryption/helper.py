import random
def dna():
	created = []
	data = open("temp.txt")
	ndata = data.read()
	for i in range(len(ndata)):
		created.append(ndata[i])
	data.close()
	return created

data = dna()

def pwp():
	data = dna()
	inpt1 = input("Enter password: ")
	for i in inpt1:
		if i not in data:
			print("Must not use spaces\nor use different special characters.")
			pwp()
	return inpt1

def ky():
	key = random.randint(10,50)
	return key

def verify(my_log):
	# program starts by logging in
	user_id = my_log
	if user_id == None:
		verify()
	else:
		current_user = user_id
		return int(current_user)

def decryptor(n):
	key = int(n[len(n)-2] + n[len(n)-1])
	enc = n[:len(n)-2]
	pw = ""
	for i in range(len(enc)):
		temp = ""
		temp += enc[i]
		ind = 0
		while True:
			if data[ind] == temp:
				break
			ind += 1
		new = ind - key
		if new < 0:
				let = new + len(data)
				pw += data[let]
		else:
			pw += data[new]
	return pw

def encryptor(pw, key):
	enc = ""
	n_new = str(key)
	for i in range(len(pw)):
		temp = ""
		temp += pw[i]
		ind = 0
		while True:
			if data[ind] == temp:
				break
			ind += 1
		new = ind + key
		if new >= len(data):
				let = new - len(data)
				enc += data[let]
		else:
			enc += data[new]
	enc += n_new
	return enc

