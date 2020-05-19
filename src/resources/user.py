from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
import datetime
from blacklist import BLACKLIST

args = reqparse.RequestParser()
args.add_argument("login", type=str, required=True, help="The field 'login' cannot be left blank.")
args.add_argument("password", type=str, required=True, help="The field 'password' cannot be left blank.")

class User(Resource):
    # /users/{user_id}
    @staticmethod
    def get(user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {"message": "User not found."}, 404
    
    @staticmethod
    @jwt_required
    def delete(user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {"message": "An error ocurred trying to delete user."}, 500 #Internal Server Error
            return {"message": "User deleted."}
        return {"message": "User not found."}, 404

class UserRegister(Resource):
    # /register
    @staticmethod
    def post():
        global args
        data = args.parse_args()
        if UserModel.find_by_login(data["login"]):
            return {"message": f"The login '{data['login']}' already exists."}
        user = UserModel(**data)
        try:
            user.save_user()
        except:
            return {"message": "An error ocurred trying to create user."}, 500 #Internal Server Error
        return {"message": "User created successfully!"}, 201 # Created status code

class UserLogin(Resource):
    # /login
    @staticmethod
    def post():
        global args
        data = args.parse_args()
        user = UserModel.find_by_login(data["login"])
        if not user.confirmed:
            return {"message": "The user is not confirmed."}, 401 # Unauthorized access
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.user_id, expires_delta=datetime.timedelta(seconds=3600))
            return {"access_token": access_token}, 200
        return {"message": "The username or password is incorrect."}, 401 # Unauthorized access

class UserLogout(Resource):
    # /logout
    @staticmethod
    @jwt_required
    def post():
        jwt_id = get_raw_jwt()["jti"] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {"message": "logged out successfully!"}, 200

class UserConfirm(Resource):
    # /confirmed/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)
        if not user:
            return {"message": "user not found."}, 404
        if user.confirmed:
            return {"message": f"user '{user.user_id}' has already been activated!"}, 200
        user.confirmed = True
        try:
            user.save_user()
        except:
            return {"message": "An error ocurred trying to confirm user."}, 500 #Internal Server Error
        return {"message": "user has been confirmed with success!"}, 200