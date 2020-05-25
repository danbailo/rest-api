import re

def get_credentials():
	pattern = re.compile(r"\w*\s=\s(.*)")
	with open("src/models/CREDENTIALS.txt") as file:
		credentials = [pattern.match(line).group(1) for line in file]
	return credentials