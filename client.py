from flask import Flask, render_template,  redirect, request
import requests
app = Flask(__name__)

API_URL = 'http://127.0.0.1:5000'

@app.route('/')
def allUsers():
    response = requests.get(API_URL + '/users')
    users = response.json()
    return render_template("users.html", users = users)

# @app.route('/register')
# def auth():


app.run(port=3000)