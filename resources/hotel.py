from flask_restful import Resource, reqparse

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

	#get data from client
	args = reqparse.RequestParser()
	args.add_argument("name")
	args.add_argument("stars")
	args.add_argument("daily")
	args.add_argument("city")

	@staticmethod
	def find_hotel(hotel_id):
		for hotel in hotels:
			if hotel["hotel_id"] == hotel_id:
				return hotel
		return None

	def get(self, hotel_id):
		hotel = Hotel.find_hotel(hotel_id)
		if hotel:
			return hotel
		return {"message": "hotel not found!"}, 404 #error status code, not found
	
	def post(self, hotel_id): #creating a new hotel (register in website)
		data = Hotel.args.parse_args()
		new_hotel = {"hotel_id": hotel_id, **data}
		hotels.append(new_hotel) 
		return new_hotel, 200 #sucess status code

	def put(self, hotel_id):
		data = Hotel.args.parse_args()
		new_hotel = {"hotel_id": hotel_id, **data}

		hotel = Hotel.find_hotel(hotel_id)
		if hotel:
			hotel.update(new_hotel) #dict method to updated data
			return new_hotel, 200
		hotels.append(new_hotel) 
		return new_hotel, 201 #created status code
	
	def delete(self, hotel_id):
		global hotels
		hotels = [hotel for hotel in hotels if hotel["hotel_id"] != hotel_id]
		return {"message": "hotel deleted."}