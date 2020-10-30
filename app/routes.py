from app import app, bcrypt, db
from app.models import Users, Shipping
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

			

			db.session.commit()
			return jsonify({'data':'success'})
		return render_template('shipping.html')
	else:
		flash("Not yet logged in", "warning")
		return redirect(url_for('login'))