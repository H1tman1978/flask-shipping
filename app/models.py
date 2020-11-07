from app import db


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)

    attention = db.Column(db.String(70), nullable=False)
    company = db.Column(db.String(70), nullable=False)
    address1 = db.Column(db.String(70), nullable=False)
    address2 = db.Column(db.String(70), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    state_province = db.Column(db.String(2), nullable=True)
    postal_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(70), nullable=True)

    template_name = db.Column(db.String(70), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Shipments(db.Model):
    shipment_id = db.Column(db.String(15), primary_key=True, unique=True)
    originating_address = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    ship_to_address = db.Column(db.Column, db.ForeignKey('addresses.id'))
    handling_units = db.relationship('HandlingUnit', backref="shipments", lazy=True)


class HandlingUnit(db.Model):
    # HANDLING_UNIT:
    unit_id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.Integer, unique=True, nullable=True)

    # string field (drop down field with box, pallet, case, drum, crate as options)
    # Required
    type = db.Column(db.String(10),
                     nullable=False)

    # integer number representing the length of the handling unit. Optional for
    # creating instruction, mandatory for shipping
    length = db.Column(db.Integer(),
                       nullable=True)
    width = db.Column(db.Integer(), nullable=True)  # same as length
    height = db.Column(db.Integer(), nullable=True)  # same as length

    # (weights will be rounded up to the nearest whole unit.) Optional for
    # creating instruction, mandatory for shipping
    weight = db.Column(db.Integer(), nullable=True)
    has_shipped = db.Column(db.Boolean(), nullable=False)
    tracking_number = db.Column(db.String(70), nullable=True)
    carrier = db.Column(db.String(70), nullable=True)

    shipment_id = db.Column(db.Integer, db.ForeignKey('shipments.id'), nullable=False)
