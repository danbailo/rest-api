from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filters import normalize_path_params
from resources.filters import query_off_city, query_on_city
from utils.config import PATH, DATABASE
import traceback
import sqlite3

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
		conn = sqlite3.connect(PATH+DATABASE)
		cursor = conn.cursor()

		global path_params
		data = path_params.parse_args()
		valid_data = {key:data[key] for key in data if data[key] is not None}
		params = normalize_path_params(**valid_data)

		if not params.get("city"):
			values = tuple(params.get(key) for key in params)
			result_set = cursor.execute(query_off_city, values)
		
		else:
			values = tuple(params.get(key) for key in params)
			result_set = cursor.execute(query_on_city, values)

		hotels = [{
			"hotel_id": row[0],
            "name": row[1],
            "stars": row[2],
            "daily": row[3],
            "city": row[4],
            "site_id": row[5],
		} for row in result_set]

		return {"hotels": hotels}

#provides resources for each hotel, that is, the info from determined hotel
class Hotel(Resource):

	#get data from client
	args = reqparse.RequestParser()
	args.add_argument("name", type=str, required=True, help="the field 'name' cant be left blank")
	args.add_argument("stars")
	args.add_argument("daily")
	args.add_argument("city")
	args.add_argument("site_id", type=int, required=True, help="every hotel needs to be linked a site")

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

		if not SiteModel.find_by_id(data.get("site_id")):
			return {"message": "the hotel must be associated with a valid site"}, 400
		try:
			hotel.save_hotel()
		except:
			traceback.print_exc()
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
				traceback.print_exc()
				return {"message": "An error ocurred trying to create hotel."}, 500 #Internal Server Error
			return hotel.json(), 200
		hotel_object = HotelModel(hotel_id, **data)
		try:
			hotel.save_hotel()
		except:
			traceback.print_exc()
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
				traceback.print_exc()
				return {"message": "An error ocurred trying to create hotel."}, 500 #Internal Server Error			
			return {"message": f"hotel '{hotel_id}' deleted."}
		return {"message": f"hotel '{hotel_id}' not found."}, 404