from app import app, bcrypt, db
from app.models import Users, Shipping
from flask import render_template, request,\
	redirect, url_for, jsonify, flash
from flask_login import current_user, logout_user, login_user

@app.route("/")
@app.route("/dashboard")
def home():
	if current_user.is_authenticated:
		return render_template("dashboard.html")
	return redirect(url_for('login'))

def hash_password(password):
	return bcrypt.generate_password_hash(password).decode('utf-8')

# def send_email(email):
# 	pass

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
			print(data['ship_to_company'])
			# new_shipping = Shipping(ship_to_company=data.)
			# db.session.add(new_shipping)
			# db.session.commit()
			return jsonify({'data':'success'})
		return render_template('shipping.html')
	else:
		return redirect(url_for('login'))