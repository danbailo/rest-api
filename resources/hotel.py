from flask_restful import Resource

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