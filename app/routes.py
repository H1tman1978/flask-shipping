from app import app, bcrypt, db
from app.models import Users, Shipping
from flask import render_template, request,\
	redirect, url_for, jsonify, flash
from flask_login import current_user, logout_user, login_user

@app.route("/")
@app.route("/dashboard")
def home():
	if current_user.is_authenticated:
		shippings = Shipping.query.filter_by(author=current_user).all()
		return render_template("dashboard.html", shippings=shippings)
	flash("Not yet logged in", "warning")
	return redirect(url_for('login'))

def hash_password(password):
	return bcrypt.generate_password_hash(password).decode('utf-8')

@app.route("/register", methods=["POST", "GET"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	if request.method == "POST":
		user = Users.query.filter_by(email=request.form["email"]).first()
		if user:
			return jsonify({'data':'exist'})
		new_user = Users(name=request.form["name"], email=request.form["email"],\
			password=hash_password(request.form["password"]))
		db.session.add(new_user)
		db.session.commit()
		return jsonify({'data':'success'})
	return render_template("register.html")

@app.route('/login', methods=["POST", "GET"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	if request.method == "POST":
		user = Users.query.filter_by(email=request.form['email']).first()
		if user and bcrypt.check_password_hash(user.password, request.form['password']):
			login_user(user, remember=True)
			return jsonify({'data':'success'})
		return jsonify({'data':'error'})
	return render_template('login.html')

@app.route("/logout")
def logout():
	logout_user()
	flash("Logout successfull", "success")
	return redirect('login')


@app.route("/request_shipping", methods=["POST", "GET"])
def shipping():
	if current_user.is_authenticated:
		if request.method == "POST":
			data = request.form
			new_shipping = Shipping(ship_to_company=data['ship_to_company'],\
				ship_from_company=data["ship_from_company"], ship_to_city=data["ship_to_city"],\
				ship_from_city=data["ship_from_city"], ship_to_zip=data["ship_to_zip"],\
				ship_from_zip=data["ship_from_zip"], ship_to_phone_number=data["ship_to_phone_number"],\
				external_phone_number=data["external_phone_number"], ship_to_address=data["ship_to_address"],
				ship_from_address=data["ship_from_address"], ship_to_state=data["ship_to_state"],\
				ship_from_state=data["ship_from_state"], senders_name=data["senders_name"],\
				special_instructions=data["special_instructions"],\
				department=data["department"], item_description=data["item_description"],\
				quantity=data["quantity"], author=current_user)

			db.session.add(new_shipping)
			db.session.commit()
			return jsonify({'data':'success'})
		return render_template('shipping.html')
	else:
		flash("Not yet logged in", "warning")
		return redirect(url_for('login'))