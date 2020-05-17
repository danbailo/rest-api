from flask import Flask, jsonify, redirect, url_for
from flask_restful import Api
from resources.hotel import Hotels, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "DontTellAnyone" #only the application will know this string
app.config["JWT_BLACKLIST_ENABLED"] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_database():
    db.create_all()

@jwt.token_in_blacklist_loader
def verify_blacklist(token):
	return token["jti"] in BLACKLIST

@jwt.revoked_token_loader
def invalidated_access_token():
	return jsonify({"message": "you have been logged out."}), 401 #unauthorized, if the client try access any resource after logged out.

@app.route("/")
def home():
	return "hello"

api.add_resource(Hotels, "/hotels")
api.add_resource(Hotel, "/hotels/<string:hotel_id>")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
	from sql_alchemy import db
	db.init_app(app)
	app.run(debug=True) #while i'm programming, set this flag to True. After deployied, set to false.