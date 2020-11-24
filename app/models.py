from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
import json
import jwt


@login.user_loader
def load_user(id):
	return User.query.get(int(id))
	
class User(UserMixin, db.Model):
	id  = db.Column(db.Integer, primary_key = True)
	email	= db.Column(db.String(120), index = True, unique = True, nullable=False)
	password = db.Column(db.String(128), nullable=False)
	
	def __hash__(self):
		return self.id
		
	def __eq__(self, another):
		return isinstance(another, User) and self.id == another.id
	
	def __repr__(self):
		return json.dumps(self.to_dict())
	
	def SetPassword(self, password):
		self.password = generate_password_hash(password)
		
	def CheckPassword(self, password):
		return check_password_hash(self.password, password)
		
	def GetAvatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
		
	def to_dict(self):
		data = {'id':self.id, 'email':self.email}
		return data
		
	def GetPasswordResetToken(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			current_app.config['SECRET_KEY'],
			algorithm='HS256').decode('utf-8')

	@staticmethod
	def VerifyPasswordResetToken(token):
		try:
			id = jwt.decode(token, current_app.config['SECRET_KEY'],
							algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)