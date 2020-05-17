from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
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
            user.delete_user()
            return {"message": "User deleted."}
        return {"message": "User not found."}, 404

class UserRegister(Resource):
    # /register
    @staticmethod
    def post():
        data = args.parse_args()

        if UserModel.find_by_login(data["login"]):
            return {"message": f"The login '{data['login']}' already exists."}

        user = UserModel(**data)
        user.save_user()
        return {"message": "User created successfully!"}, 201 # Created status code

class UserLogin(Resource):
    # /login
    @staticmethod
    def post():
        data = args.parse_args()
        user = UserModel.find_by_login(data["login"])
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.user_id)
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