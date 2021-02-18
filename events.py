from db import db
import users

def sign_up():
	sql = "INSERT INTO sign_ups(user_id, event_id, sign_up) VALUES (user_id, event_id, sign_up)"
	db.session.execute()
	db.session.commit()
	return True

def get_events():
    result = db.session.execute("SELECT E.type, E.day, E.h_min, E.name, E.id, E.location "\
                                "FROM events E " \
                                "WHERE E.day >= now() " \
                                "ORDER BY E.day DESC LIMIT 10")
    return result.fetchall()

def get_event_info(id):
    sql = "SELECT E.type, E.day, E.h_min, E.name, E.id, E.location "\
          "FROM events E " \
	  "LEFT JOIN comments C on E.id = C.event_id " \
          "WHERE E.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_comments():
    result = db.session.execute("SELECT C.t_stamp, C.event_id, C.user_id, C.message, U.first_name, U.last_name " \
                                "FROM comments C " \
                                "LEFT JOIN users U on U.id=C.user_id "\
                                "LEFT JOIN events E on E.id=C.event_id "\
                                "WHERE E.day >= now() "\
                                "ORDER BY C.t_stamp")

    return result.fetchall()


def get_all_sign_ups():

    result = db.session.execute("SELECT U.first_name, S.event_id, S.sign_up "\
                                "FROM users U "\
                                "LEFT JOIN sign_ups S ON S.user_id=U.id "\
                                "LEFT JOIN events E ON S.event_id=E.id "\
                                "ORDER BY E.day")
    return result.fetchall()

def get_sign_ups(id):
    sql = "SELECT U.first_name, S.event_id, S.sign_up "\
                                "FROM users U "\
                                "LEFT JOIN sign_ups S ON S.user_id=U.id "\
                                "LEFT JOIN events E ON S.event_id=E.id "\
                                "WHERE E.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()


def get_games():
    result = db.session.execute("SELECT E.day, E.name"\
                                "FROM events E " \
                                "WHERE E.type='1'")
    return result.fetchall()


def add_event(type, day, time, name, location):
    sql = "INSERT INTO events (type, day, h_min, name, location) VALUES (:type, :day, :time, :name, :location)"
    db.session.execute(sql, {"type":type, "day":day, "time":time, "name":name, "location":location})
    db.session.commit()
    return True

def add_comment(user_id, event_id, message):
	sql = "INSERT INTO comments (t_stamp, event_id, message, user_id) VALUES (now(), :event_id, :message, :user_id)"
	db.session.execute(sql, {"event_id":event_id, "message":message, "user_id":user_id})
	db.session.commit()
	return True
