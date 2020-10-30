from app import app, bcrypt, db
from app.models import Users, Shipping, HandlingUnit
from flask import render_template, request,\
	redirect, url_for, jsonify, flash
from flask_login import current_user, logout_user, login_user

@app.route("/")
@app.route("/dashboard")
def home():
	if current_user.is_authenticated:
		# shippings = Shipping.query.filter_by(author=current_user).all()
		return render_template("dashboard.html")
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
		new_user = Users(first_name=request.form["first_name"],\
			last_name=request.form["last_name"],\
			email=request.form["email"],\
			user_name = request.form["username"],
			slack_handle = request.form["slack_handle"],\
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

			new_shipping = Shipping(attention=data["attention"], company=data["company"],\
				address1=data["address1"], address2=data["address2"], city=data["city"],\
				state_province=data["state_province"], postal_code=data["postal_code"],\
				country=data["country"], template_name=data["template_name"],\
				author=current_user)

			db.session.add(new_shipping)

			new_handlingUnit = HandlingUnit(type=data["type"], length=data["length"],\
				width=data["width"], height=data["height"], weight=data["weight"],\
				has_shipped=False, tracking_number=data["tracking_number"],\
				carrier=data["carrier"], shipping_handling_unit=new_shipping)

			db.session.add(new_handlingUnit)

			db.session.commit()
			return jsonify({'data':'success'})
		return render_template('shipping.html')
	else:
		flash("Not yet logged in", "warning")
		return redirect(url_for('login'))