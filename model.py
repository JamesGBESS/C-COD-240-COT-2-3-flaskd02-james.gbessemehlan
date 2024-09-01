from werkzeug.security import generate_password_hash

def Register(database, username, email, password):
    database.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password),)
                )
    database.commit()
    database.close()
    print('User registered !')

def Login(database, email):
    user = database.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
    database.commit()
    database.close()
    return user

def getAllUsers(database):
    users = database.execute("SELECT * FROM users").fetchall()
    database.commit()
    database.close()
    return users

def getOneUser(database, id):

    user = database.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()

    return user

def UpdateUser(database, id, username, email, password):

    database.execute('UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?', (username, email, password, id,),)

    database.commit()

    # database.close()

def DeleteUser(database, id):
    database.execute('DELETE FROM users WHERE id=?', (id,))
    database.commit()
    database.close()
