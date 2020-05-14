from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

hotels = [
	{
		"hotel_id": "alpha",
		"name": "Alpha Hotel",
		"stars": 4.3,
		"daily": 420.34,
		"city": "Rio de Janeiro"
	},
	{
		"hotel_id": "bravo",
		"name": "Bravo Hotel",
		"stars": 4.4,
		"daily": 380.90,
		"city": "Santa Catarina"
	},
	{
		"hotel_id": "charlie",
		"name": "Charlie Hotel",
		"stars": 3.9,
		"daily": 320.20,
		"city": "Santa Catarina"
	}				
]

class Hotels(Resource):
	def get(self):
		return {"hotels": hotels}

api.add_resource(Hotels, "/hotels")

if __name__ == "__main__":
	app.run(debug=True) #while i'm programming, set this flag to True. After deployied, set to false.

#first resource
#http://127.0.0.1:5000/hotels