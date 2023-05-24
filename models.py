from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from base64 import b64encode
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first = db.Column(db.String(150), nullable=True, default='')
    last = db.Column(db.String(150), nullable = True, default ='')
    email = db.Column(db.String(150), nullable = False)
    username = db.Column(db.String(150), nullable=True, default='')
    password = db.Column(db.String, nullable = True, default ='')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, first='', last='', username='', email='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first = first
        self.last = last
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Meme(db.Model):
    id = db.Column(db.String, primary_key = True)
    quote = db.Column(db.String(15))
    img = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    user = db.relationship('User', backref=db.backref('memes', lazy=True))

    def __init__(self, quote, img, user_token, id=''):
        self.id = self.set_id()
        self.quote = quote
        self.img = img
        self.user_token = user_token


    def __repr__(self):
        return f'The following Meme has been added to the database: {self.id}'

    def set_id(self):
        return (secrets.token_urlsafe())
    
    def get_image_data(self):
        if self.img:
            return b64encode(self.img).decode('utf-8')
        return None 

class MemeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'quote', 'img']

meme_schema = MemeSchema()
memes_schema = MemeSchema(many=True)