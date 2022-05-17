from crypt import methods
from operator import methodcaller
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt 
from flask_app.models.users import User

bcrypt = Bcrypt(app)

@app.route("/")
def login_page():
    return render_template("index.html")

# @app.route("/account")
# def display_user_page():
#     return render_template("user_page.html", user = user)

@app.route("/users/register", methods=['POST'])
def register_user():
    if User.validate_user(request.form):
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form ['last_name'],
            'email' : request.form ['email'],
            'password' : bcrypt.generate_password_hash(request.form['password'])
        }
        User.create_user(data)
    
    else: 
        print("is not valid")
    return redirect("/")


@app.route("/users/login", methods=['POST'])
def login_user():   
    users = User.get_user_by_email(request.form)
    if len(users) != 1: 
        flash("Incorrect email address")
        return redirect("/")

    user = users[0]
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password")
        return redirect("/")

    session['user_id'] = user.id
    session['email'] = user.email
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name

    return redirect("/success")

@app.route("/success")
def success(): 
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect("/")
    
    return render_template("user_page.html")

@app.route("/logout")
def logout(): 
    session.clear()
    return redirect("/")

