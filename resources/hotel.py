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
	def get(self, hotel_id):
		for hotel in hotels:
			if hotel["hotel_id"] == hotel_id:
				return hotel
		return {"message": "hotel not found!"}, 404 #error status code, not found
	
	def post(self, hotel_id): #creating a new hotel (register in website)
		args = reqparse.RequestParser()
		args.add_argument("name")
		args.add_argument("stars")
		args.add_argument("daily")
		args.add_argument("city")

		data = args.parse_args()

		new_hotel = {
			"hotel_id": hotel_id,
			"name": data["name"],
			"stars": data["stars"],
			"daily": data["daily"],
			"city": data["city"]
		}

		#like insert in database
		hotels.append(new_hotel) 

		return new_hotel, 200 #sucess status code

	def put(self, hotel_id):
		NOT_IN = True

		args = reqparse.RequestParser()
		args.add_argument("name")
		args.add_argument("stars")
		args.add_argument("daily")
		args.add_argument("city")
		
		data = args.parse_args()

		for hotel in hotels:
			if hotel_id in hotel["hotel_id"]:
				hotel["name"] = data["name"]
				hotel["stars"] = data["stars"]
				hotel["daily"] = data["daily"]
				hotel["city"] = data["city"]
				NOT_IN = False
				return hotel, 200 #sucess status code	

		if NOT_IN:
			new_hotel = {
				"hotel_id": hotel_id,
				"name": data["name"],
				"stars": data["stars"],
				"daily": data["daily"],
				"city": data["city"]
			}

			#like insert in database
			hotels.append(new_hotel) 

			return new_hotel, 200 #sucess status code			

	
	def delete(self, hotel_id):
		pass		