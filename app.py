from flask import Flask
from flask_restful import Api
from resources.hotel import Hotels, Hotel

app = Flask(__name__)
api = Api(app)

api.add_resource(Hotels, "/hotels")
api.add_resource(Hotel, "/hotels/<string:hotel_id>")

if __name__ == "__main__":
	app.run(debug=True) #while i'm programming, set this flag to True. After deployied, set to false.

#first resource
#http://127.0.0.1:5000/hotels