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

class Hotel(Resource):
	def get(self, hotel_id):
		for hotel in hotels:
			if hotel["hotel_id"] == hotel_id:
				return hotel
		return {"message": "hotel not found!"}, 404 #error status code, not found
	
	def post(self, hotel_id):
		pass

	def put(self, hotel_id):
		pass
	
	def delete(self, hotel_id):
		pass		