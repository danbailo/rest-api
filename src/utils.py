import json

def get_credentials():
	with open("config/credentials.json") as file:
		return json.load(file)