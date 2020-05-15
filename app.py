from flask import Flask
from flask_restful import Api
from resources.hotel import Hotels, Hotel
from resources.user import User, UserRegister, UserLogin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

@app.before_first_request
def create_db():
    db.create_all()

api.add_resource(Hotels, "/hotels")
api.add_resource(Hotel, "/hotels/<string:hotel_id>")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
	from sql_alchemy import db
	db.init_app(app)
	app.run(debug=True) #while i'm programming, set this flag to True. After deployied, set to false.