from werkzeug.security import check_password_hash
from flask import redirect, url_for, flash, render_template, jsonify, request
import model
def registerController(database, username, email, password):
    error = None

    if not username:
        error = 'Username is required !'
    elif not email:
        error = 'Email is required !'
    elif not password:
        error = 'Password is required !'

    if error is None:
        try:
            model.Register(database, username, email, password)
        except database.IntegrityError:
                error = f"User {username} is already registered."
        else:
            return redirect(url_for("login"))
    flash(error)

def loginController(database, email, password):
    error = None
    user = model.Login(database, email)
    if user is None:
        error = 'Incorrect email.'
        print(error)
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'
        print(error)

    if error is None:
        return render_template('welcome.html', name = user['username'])
    
    flash(error)
    return error

def getUsers(database):
    users = model.getAllUsers(database)
    return jsonify([dict(user) for user in users])

def getUser(database, id):
    user  = model.getOneUser(database, id)
    if user:
        return jsonify([dict(user)])
    else: 
        return jsonify({"Error": "User not found !"}), 404

def updateUser(database, id, username = None, email = None, password = None):
    model.UpdateUser(database, id, username, email, password)
    print("User updated !")
    return  jsonify({"Status": "User deleted !"}), 200

def deleteUser(database, id):
    model.DeleteUser(database, id)
    print("User deleted !")
    return jsonify({"Status": "User deleted !"}), 200

def update_user(database, id):
    user = model.getOneUser(database, id)
    if user == None:
        return jsonify({'Error': 'User not found !'}), 404
    
    username = request.get_json().get('username')
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    model.UpdateUser(database, id, username, email, password,)
    
    return jsonify({'Status': 'User updated !'}), 200
