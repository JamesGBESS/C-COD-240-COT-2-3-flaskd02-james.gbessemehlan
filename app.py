from flask import Flask
# from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash, check_password_hash
import os
import click
import sqlite3
import controller, model
from flask import Flask, g, current_app, request, render_template, redirect, url_for,flash, jsonify
app = Flask(__name__)

app.config.from_object ( __name__ ) # load config from this file app.py
# Load default config and override config from an environment variable
app.config.from_mapping (
DATABASE = os.path.join ( app.root_path , ' DATABASE.db ') ,
SECRET_KEY = 'dev'
)

@app.route('/')
def index():
    return render_template('welcome.html')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def connect_db():
    g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    g.db.row_factory = sqlite3.Row
    
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('run_app')

def init_db_command():
    init_db()
    click.echo('Your database is launched !')

# @with_appcontext
def get_db():
    if 'db' not in g:
        connect_db()
    return g.db
def query_db(query, args=(), methoD="fetch", one=False):
    if not os.path.exists('DATABASE.db'):
        with app.app_context():
            init_db()
    cur = get_db().execute(query, args)
    if (methoD == "fetch"):
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    elif (methoD == "commit"):
        get_db().commit()
        rv = cur.lastrowid
        return rv
def close_db(e=None):
    db = g.pop('db', None)  

    if db is not None:
        db.close()
        
init_app(app)

@app.route('/register', methods=('GET', 'POST'))
def register():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        return controller.registerController(db, username, email, password)

    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    db = get_db()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        return controller.loginController(db, email, password)
    
    return render_template('login.html')
@app.route('/users', methods = ['GET'])
def users():
    db = get_db()
    return controller.getUsers(db)

@app.route('/user/<int:id>', methods=['GET','PUT','DELETE'])
def manageUser(id):
    db = get_db()
    if request.method == 'PUT':
        return controller.update_user(db, id)
    if request.method == 'DELETE':
        return controller.deleteUser(db, id)
    if request.method == 'GET':
        return controller.getUser(db, id)
    