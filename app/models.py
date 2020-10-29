from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
	return Users.query.get(int(id))

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	first_name = db.Column(db.String(70), nullable=False)
	last_name = db.Column(db.String(70), nullable=False)
	user_name = db.Column(db.String(70), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	slack_handle: db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	date_joined = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

	# shippings = db.relationship("Shipping", backref="author", lazy=True)

	def __repr__(self):
		return f"Name: {self.name} Email: {self.email} Date Joined: {self.date_joined} "


class Shipping(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	# Addresses
	attention: db.Column(db.String(70), nullable=False)
	company: db.Column(db.String(70), nullable=False)
	address1: db.Column(db.String(70), nullable=False)
	address2: db.Column(db.String(70), nullable=False)
	city: db.Column(db.String(70), nullable=False)
	state_province: db.Column(db.String(70), nullable=True)
	postal_code: db.Column(db.String(70), nullable=False)
	country: db.Column(db.String(70), nullable=True)
	template_name: db.Column(db.String(70), nullable=True)

	handling_unit = db.relationship("HandlingUnit", backref="shipping_handling_unit", lazy=True)

class HandlingUnit(db.Model):
	# HANDLING_UNIT:
	case_number: db.Column(db.Integer, primary_key=True, unique=True)
	instruction_id = db.Column(db.Integer, db.ForeignKey('shipping.id'), nullable=False)

	type: db.Column(db.String(70), nullable=False) #string field (drop down field with box, pallet, case, drum, crate as options) Required
	length: db.Column(db.Integer(), nullable=True) #float number representing the length of the handling unit. Optional for creating instruction, mandatory for shipping
	width: db.Column(db.Integer(), nullable=True) #same as length
	height: db.Column(db.Integer(), nullable=True) #same as length

	weight: db.Column(db.Integer(), nullable=False) #(weights will be rounded up to the nearest whole unit.) Optional for creating instruction, mandatory for shipping
	has_shipped: db.Column(db.Boolean(), nullable=False)
	tracking_number: db.Column(db.String(70), nullable=False)
	carrier: db.Column(db.String(70), nullable=False)