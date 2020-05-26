from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from flask_restful import Resource, reqparse
from models.user import UserModel
from utils.blacklist import BLACKLIST
import datetime
import traceback

args = reqparse.RequestParser()
args.add_argument("login", type=str, required=True, help="The field 'login' cannot be left blank.")
args.add_argument("password", type=str, required=True, help="The field 'password' cannot be left blank.")
args.add_argument("email", type=str) #if i had left "required=True", all operations in user.py would need this field

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
                traceback.print_exc()
                return {"message": "An error ocurred trying to delete user."}, 500 #Internal Server Error
            return {"message": f"user {user.login} deleted with successfully!"}
        return {"message": f"user {user.login} not found!"}, 404

class UserRegister(Resource):
    # /register
    @staticmethod
    def post():
        global args
        data = args.parse_args()
        if not data.get("email"):
            return {"message": "insert a valid email!"}      
        if UserModel.find_by_login(data["login"]):
            return {"message": f"The login '{data['login']}' already exists."}
        if UserModel.find_by_email(data["email"]):
            return {"message": f"The email '{data['email']}' already exists."}            
        user = UserModel(**data)
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return {"message": "An error ocurred trying to create user."}, 500 #Internal Server Error
        return {"message": f"user {user.login} has been created successfully!"}, 201 # Created status code

class UserLogin(Resource):
    # /login
    @staticmethod
    def post():
        global args
        data = args.parse_args()
        user = UserModel.find_by_login(data["login"])
        if not user.confirmed:
            return {"message": f"user '{user.login}' is not confirmed."}, 401 # Unauthorized access
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.user_id, expires_delta=datetime.timedelta(seconds=3600))
            return {"access_token": access_token}, 200
        return {"message": "username or password is incorrect."}, 401 # Unauthorized access

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
            return {"message": f"user '{user.user_id}' not found."}, 404
        if user.confirmed:
            return {"message": f"user '{user.user_id}' has already been activated!"}, 200
        user.confirmed = True
        try:
            user.save_user()
        except:
            traceback.print_exc()
            return {"message": "An error ocurred trying to confirm user."}, 500 #Internal Server Error
        return {"message": f"user '{user.login}' has been confirmed with success!"}, 200