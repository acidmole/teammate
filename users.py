from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id, first_name FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["first_name"] = user[2]
            return True
        else:
            return False

def user_id():
	return session.get("user_id",0)

def is_admin():
	result = db.session.execute("SELECT admin FROM users WHERE id=" + str(user_id()))
	user_type = result.fetchone()
	if user_type[0] == True:
		return True
	else:
		return False

def logout():
    del session["user_id"]

def new_user(username, password, first_name, last_name):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, first_name, last_name) VALUES (:username, :password, :first_name, :last_name)"
    db.session.execute(sql, {"username":username, "password":hash_value, "first_name":first_name, "last_name":last_name})
    db.session.commit()
    return True


def new_player(username, jersey, height, weight, position):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    sql = "INSERT INTO players (user_id, jersey_number, height, weight, position) VALUES ('" + str(user[0]) + "', :jersey, :height, :weight, :position)"
    db.session.execute(sql, {"jersey":jersey, "height":height, "weight":weight, "position":position})
    db.session.commit()
    return True

def get_user(user_id):
	sql = "SELECT :user_id, first_name, last_name FROM users"
	result = db.session.execute(sql, {"user_id":user_id})
	return result.fetchone()

def update_user(user_id, first_name, last_name):
	sql = "UPDATE users SET first_name=:first_name, last_name=:last_name WHERE id=:user_id"
	result = db.session.execute(sql, {"user_id":user_id, "first_name":first_name, "last_name":last_name})
	return True

def change_password(new_password):
	return null
