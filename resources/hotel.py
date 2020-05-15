from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

#provides resources to all hotels, that is, the info of all hotels
class Hotels(Resource):
	def get(self):
		return {"hotels": [hotel.json() for hotel in HotelModel.query.all()]} # SELECT * FROM hoteis

#provides resources for each hotel, that is, the info from determined hotel
class Hotel(Resource):

	#get data from client
	args = reqparse.RequestParser()
	args.add_argument("name")
	args.add_argument("stars")
	args.add_argument("daily")
	args.add_argument("city")

	#to access the get resource, the user not need be logged in the system.
	def get(self, hotel_id):
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			return hotel.json()
		return {"message": f"hotel '{hotel_id}' not found."}, 404 #error status code, not found
	
	#however, to handling the database, he need!
	#that is why we'll use the following decorator

	@jwt_required
	def post(self, hotel_id): #creating a new hotel (register in website)
		if HotelModel.find_hotel(hotel_id):
			return {"message": f"hotel {hotel_id} already exists."}, 400 #Bad Request

		data = Hotel.args.parse_args()
		hotel = HotelModel(hotel_id, **data)
		try:
			hotel.save_hotel()
		except:
			return {"message": "An error ocurred trying to create hotel."}, 500 #Internal Server Error
		return hotel.json(), 201

	@jwt_required
	def put(self, hotel_id):
		data = Hotel.args.parse_args()
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			hotel.update_hotel(**data)
			try:
				hotel.save_hotel()
			except:
				return {"message": "An error ocurred trying to create hotel."}, 500 #Internal Server Error
			return hotel.json(), 200
		hotel_object = HotelModel(hotel_id, **data)
		try:
			hotel.save_hotel()
		except:
			return {"message": "An error ocurred trying to create hotel."}, 500 #Internal Server Error
		return hotel_object.json(), 201#created status code
	
	@jwt_required
	def delete(self, hotel_id):
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			try:
				hotel.delete_hotel()
			except:
				return {"message": "An error ocurred trying to create hotel."}, 500 #Internal Server Error			
			return {"message": f"hotel '{hotel_id}' deleted."}
		return {"message": f"hotel '{hotel_id}' not found."}, 404