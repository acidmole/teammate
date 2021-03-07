from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(username, password):
    sql = "SELECT password, id, first_name, visible FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None or user[3] == False:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["first_name"] = user[2]
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def get_csrf_token():
	return session.get("csrf_token",0)

def user_id():
	return session.get("user_id",0)

def is_admin():
	result = db.session.execute("SELECT admin FROM users WHERE id=" + str(user_id()))
	user_type = result.fetchone()
	if user_type[0] == True:
		return True
	return False

def set_admin(id):
	sql = "UPDATE users SET admin='t' WHERE id=:id"
	db.session.execute(sql, {"id":id})
	db.session.commit()
	return True

def logout():
    del session["user_id"]

def new_user(username, password, first_name, last_name):
	sql="SELECT username FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	duplicate_user = result.fetchone()
	if duplicate_user == None:
		hash_value = generate_password_hash(password)
		sql = "INSERT INTO users (username, password, first_name, last_name) VALUES (:username, :password, :first_name, :last_name)"
		db.session.execute(sql, {"username":username, "password":hash_value, "first_name":first_name, "last_name":last_name})
		db.session.commit()
		return True
	else:
		return False


def new_player(username, jersey, height, weight, position):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    sql = "INSERT INTO players (user_id, jersey_number, height, weight, position) VALUES ('" + str(user[0]) + "', :jersey, :height, :weight, :position)"
    db.session.execute(sql, {"jersey":jersey, "height":height, "weight":weight, "position":position})
    db.session.commit()
    return True

def get_user(user_id):
	sql = "SELECT id, first_name, last_name, username FROM users WHERE id=:user_id"
	result = db.session.execute(sql, {"user_id":user_id})
	return result.fetchone()

def update_user(user_id, first_name, last_name):
	sql = "UPDATE users SET first_name=:first_name, last_name=:last_name WHERE id=:user_id"
	db.session.execute(sql, {"user_id":user_id, "first_name":first_name, "last_name":last_name})
	db.session.commit()
	return True

def delete_user(id):
	sql = "UPDATE users SET visible='f' WHERE id=:id"
	db.session.execute(sql, {"id":id})
	db.session.commit()
	return True

# returns a list of all users
def get_all_users():
	result = db.session.execute("SELECT id, first_name, last_name, admin FROM users WHERE visible='t' ORDER BY last_name")
	return result.fetchall()

def get_all_deleted_users():
	result = db.session.execute("SELECT id, first_name, last_name, admin FROM users WHERE visible='f'")
	return result.fetchall()


def is_visible(id):
	sql = "SELECT visible FROM users WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	visible = result.fetchone()
	return visible[0]

# returns a list of all players in graveyard
def get_graveyard():
	result = db.session.execute("SELECT id, first_name, last_name FROM users WHERE visible='f'")
	return result.fetchall()

# brings a player back from graveyard
def raise_dead(id):
	sql = "UPDATE users SET visible='t' WHERE id=:id"
	db.session.execute(sql, {"id":id})
	db.session.commit()
	return True
