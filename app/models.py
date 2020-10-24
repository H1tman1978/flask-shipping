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

	ship_to_company = db.Column(db.String(70), nullable=False)
	ship_from_company = db.Column(db.String(70), nullable=False)

	ship_to_city = db.Column(db.String(70), nullable=False)
	ship_from_city = db.Column(db.String(70), nullable=False)

	ship_to_zip = db.Column(db.Integer(), nullable=False)
	ship_from_zip = db.Column(db.Integer(), nullable=False)

	ship_to_phone_number = db.Column(db.String(70), nullable=False)
	external_phone_number = db.Column(db.String(70), nullable=False)

	ship_to_address = db.Column(db.String(70), nullable=False)
	ship_from_address = db.Column(db.String(70), nullable=False)

	ship_to_state = db.Column(db.String(70), nullable=False)
	ship_from_state = db.Column(db.String(70), nullable=False)

	senders_name = db.Column(db.String(70), nullable=False)
	internal_address = db.Column(db.String(70), nullable=False)

	special_instructions = db.Column(db.Text(400), nullable=False)
	department = db.Column(db.String(70), nullable=False)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)