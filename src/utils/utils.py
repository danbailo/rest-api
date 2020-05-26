import json
import os.path

def get_credentials(path=os.path.join("..", "config", ""), input_file="credentials.json"):
	with open(path + input_file) as file:
		return json.load(file)

def get_db_path(path=os.path.join("..", "config", ""), input_file="database.json"):
	with open(path + input_file) as file:
		return json.load(file)		