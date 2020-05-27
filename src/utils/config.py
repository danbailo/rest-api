import json
import os.path

with open(os.path.join("..", "config", "") + "credentials.json") as file:
	credentials = json.load(file)

with open(os.path.join("..", "config", "") + "database.json") as file:
	database = json.load(file)

API_KEY = credentials.get("API_KEY")
API_SECRET = credentials.get("API_SECRET")
JWT_SECRET_KEY = credentials.get("JWT_SECRET_KEY")

PATH = database.get("PATH")
DATABASE = database.get("DATABASE")