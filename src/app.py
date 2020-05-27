from flask import Flask, jsonify, redirect, url_for
from flask_restful import Api
from resources.hotel import Hotels, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.site import Sites, Site
from flask_jwt_extended import JWTManager
from utils.blacklist import BLACKLIST
from utils.config import PATH, DATABASE, JWT_SECRET_KEY

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{PATH+DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
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

api.add_resource(Hotels, "/hotels")
api.add_resource(Hotel, "/hotels/<string:hotel_id>")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserConfirm, "/confirm/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(Sites, "/sites")
api.add_resource(Site, "/sites/<string:url>")


if __name__ == "__main__":
	from utils.sql_alchemy import db
	db.init_app(app)
	app.run(debug=True) #while i'm programming, set this flag to True. After deployied, set to false.