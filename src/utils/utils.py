import json
import os.path

with open(os.path.join("..", "config", "") + "credentials.json") as file:
	CREDENTIALS = json.load(file)

with open(os.path.join("..", "config", "") + "database.json") as file:
	DATABASE = json.load(file)