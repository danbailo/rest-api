from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(
		city=None,
		min_stars=0,
		max_stars=5,
		min_daily=0,
		max_daily=10000,
		limit=50,
		offset=0,
		**kwargs):
	if not city:	
		return {
			"min_stars": min_stars,
			"max_stars": max_stars,
			"min_daily": min_daily,
			"max_daily": max_daily,
			"limit": limit,
			"offset": offset
		}
	return { #**data
		"city": city,
		"min_stars": min_stars,
		"max_stars": max_stars,
		"min_daily": min_daily,
		"max_daily": max_daily,
		"limit": limit,
		"offset": offset
	}


#/hotels?city=Rio de Janeiro&min_stars=4.5&max_daily=400

path_params = reqparse.RequestParser()
path_params.add_argument("city", type=str)
path_params.add_argument("min_stars", type=float)
path_params.add_argument("max_stars", type=float)
path_params.add_argument("min_daily", type=float)
path_params.add_argument("max_daily", type=float)
path_params.add_argument("limit", type=int)
path_params.add_argument("offset", type=int)

#provides resources to all hotels, that is, the info of all hotels
class Hotels(Resource):
	@staticmethod
	def get():
		conn = sqlite3.connect("database.db")
		cursor = conn.cursor()

		global path_params
		data = path_params.parse_args()
		valid_data = {key:data[key] for key in data if data[key] is not None}
		params = normalize_path_params(**valid_data)

		if not params.get("city"):
			query = """
						SELECT * FROM hotels
						WHERE (stars >= ? and stars <= ?)
						and (daily >= ? and daily <= ?)
						LIMIT ? OFFSET ?
					"""
			values = tuple(params.get(key) for key in params)
			result_set = cursor.execute(query, values)
		
		else:
			query = """
						SELECT * FROM hotels
						WHERE (city = ?)
						and (stars >= ? and stars <= ?)
						and (daily >= ? and daily <= ?)
						LIMIT ? OFFSET ?
					"""
			values = tuple(params.get(key) for key in params)
			result_set = cursor.execute(query, values)

		hotels = [{
			"hotel_id": row[0],
            "name": row[1],
            "stars": row[2],
            "daily": row[3],
            "city": row[4]
		} for row in result_set]

		return {"hotels": hotels}

#provides resources for each hotel, that is, the info from determined hotel
class Hotel(Resource):

	#get data from client
	args = reqparse.RequestParser()
	args.add_argument("name")
	args.add_argument("stars")
	args.add_argument("daily")
	args.add_argument("city")

	#to access the get resource, the user not need be logged in the system.
	@staticmethod
	def get(hotel_id):
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			return hotel.json()
		return {"message": f"hotel '{hotel_id}' not found."}, 404 #error status code, not found
	
	#however, to handling the database, he need!
	#that is why we'll use the following decorator
	
	@staticmethod
	@jwt_required
	def post(hotel_id): #creating a new hotel (register in website)
		if HotelModel.find_hotel(hotel_id):
			return {"message": f"hotel {hotel_id} already exists."}, 400 #Bad Request

		data = Hotel.args.parse_args()
		hotel = HotelModel(hotel_id, **data)
		try:
			hotel.save_hotel()
		except:
			return {"message": "An error ocurred trying to create hotel."}, 500 #Internal Server Error
		return hotel.json(), 201
	
	@staticmethod
	@jwt_required
	def put(hotel_id):
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
	
	@staticmethod
	@jwt_required
	def delete(hotel_id):
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			try:
				hotel.delete_hotel()
			except:
				return {"message": "An error ocurred trying to create hotel."}, 500 #Internal Server Error			
			return {"message": f"hotel '{hotel_id}' deleted."}
		return {"message": f"hotel '{hotel_id}' not found."}, 404