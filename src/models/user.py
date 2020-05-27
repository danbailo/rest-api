from utils.sql_alchemy import db
from utils.utils import API_KEY, API_SECRET
from flask import request, url_for
from mailjet_rest import Client

api_key, api_secret = API_KEY, API_SECRET

class UserModel(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email

    def json(self):		
        return {
			"user_id": self.user_id,
			"login": self.login,
			"email": self.email,
			"confirmed": self.confirmed
		}

    def send_confirmation_email(self):
        #http://127.0.0.1:5000/confirm/{user_id}
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.user_id)
        data = \
        {
            "Messages":[
                {
                    "From":{
                        "Email":"danbailoufms@gmail.com",
                        "Name":"Daniel Bailo"
                    },
                    "To":[
                        {
                            "Email":f"{self.email}",
                            "Name":"passenger 1"
                        }
                    ],
                    "Subject":"Account Email Verification - Action Required",
                    "HTMLPart":f"""<p>
                                    Click <a href="{link}">here</a> to active your account!
                                </p>"""
                }
            ]
        }
        mailjet.send.create(data=data)

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None        

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()