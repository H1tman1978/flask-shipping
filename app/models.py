from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
	return Users.query.get(int(id))

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(70), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	date_joined = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

	shippings = db.relationship("Shipping", backref="author", lazy=True)

	def __repr__(self):
		return f"Name: {self.name} Email: {self.email} Date Joined: {self.date_joined} "


class Shipping(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	from_location = db.Column(db.String(), nullable=False)
	to_location = db.Column(db.String(), nullable=False)
	service_level = db.Column(db.String(100), nullable=False)
	special_instructions = db.Column(db.Text(400), nullable=False)
	package_contents = db.Column(db.String(100), nullable=False)
	package_code = db.Column(db.String(30), nullable=False)
	date_requested = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	def __repr__(self):
		return f"from location: {self.from_location} to location: {self.to_location}\
			service level: {self.service_level} special instructions: {self.special_instructions}\
			package contents: {self.package_contents} package code: {self.package_code} "