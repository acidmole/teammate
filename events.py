from db import db
import users

def sign_up(user_id, event_id, sign_up):
	sql = "DELETE FROM sign_ups WHERE user_id=" + user_id + " AND event_id=" + event_id
	db.session.execute(sql)
	db.session.commit()
	sql = "INSERT INTO sign_ups(user_id, event_id, sign_up) VALUES (" + user_id + "," + event_id + "," + "'" + sign_up + "')"
	db.session.execute(sql)
	db.session.commit()
	return True

def get_all_events(timespan):
    sql = "SELECT E.type, E.day, E.h_min, E.name, E.id, E.location "\
    "FROM events E " \
	"WHERE " + str(timespan) + " "\
	"ORDER BY E.day LIMIT 20"
    result = db.session.execute(sql)
    return result.fetchall()

def get_event_info(id):
    sql = "SELECT E.type, E.day, E.h_min, E.name, E.id, E.location "\
          "FROM events E " \
          "WHERE E.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

# returns every event's comments
def get_all_comments(timespan):
    sql = "SELECT C.t_stamp, C.event_id, C.user_id, C.message, U.first_name, U.last_name " \
	"FROM comments C " \
	"LEFT JOIN users U on U.id=C.user_id "\
	"LEFT JOIN events E on E.id=C.event_id "\
	"WHERE " + str(timespan) + " "\
	"ORDER BY C.t_stamp"
    result = db.session.execute(sql)
    return result.fetchall()

# returns single event's comments
def get_comments(id):
	sql = "SELECT C.t_stamp, C.event_id, C.user_id, C.message, U.first_name, U.last_name " \
                                "FROM comments C " \
                                "LEFT JOIN users U on U.id=C.user_id "\
                                "LEFT JOIN events E on E.id=C.event_id "\
                                "WHERE C.event_id=:id "\
                                "ORDER BY C.t_stamp"
	result = db.session.execute(sql, {"id":id})
	return result.fetchall()

# returns every "in" call for events selected timespan
def get_all_sign_ups(timespan):

	sql = "SELECT U.first_name, S.event_id, S.sign_up "\
	"FROM users U "\
	"LEFT JOIN sign_ups S ON S.user_id=U.id "\
	"LEFT JOIN events E ON S.event_id=E.id "\
	"WHERE " + str(timespan) + " AND S.sign_up='t' "\
	"ORDER BY E.day"
	result = db.session.execute(sql)
	return result.fetchall()

# returns every "out" call for events selected timespan
def get_all_sign_outs(timespan):

	sql = "SELECT U.first_name, S.event_id, S.sign_up "\
	"FROM users U "\
	"LEFT JOIN sign_ups S ON S.user_id=U.id "\
	"LEFT JOIN events E ON S.event_id=E.id "\
	"WHERE " + str(timespan) + " AND S.sign_up='f' "\
	"ORDER BY E.day"
	result = db.session.execute(sql)
	return result.fetchall()

# returns "in" calls for single event
def get_sign_ups(id):
    sql = "SELECT U.first_name, S.event_id, S.sign_up "\
                                "FROM users U "\
                                "LEFT JOIN sign_ups S ON S.user_id=U.id "\
                                "LEFT JOIN events E ON S.event_id=E.id "\
                                "WHERE E.id=:id AND S.sign_up='t'"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

# returns "out" calls for single event
def get_sign_outs(id):
    sql = "SELECT U.first_name, S.event_id, S.sign_up "\
                                "FROM users U "\
                                "LEFT JOIN sign_ups S ON S.user_id=U.id "\
                                "LEFT JOIN events E ON S.event_id=E.id "\
                                "WHERE E.id=:id AND S.sign_up='f'"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()


# returns a list of every game type event
def get_games():
    result = db.session.execute("SELECT E.day, E.name, E.id "\
                                "FROM events E " \
                                "WHERE E.type='1'")
    return result.fetchall()

# adds a new event
def add_event(type, day, time, name, location):
    sql = "INSERT INTO events (type, day, h_min, name, location) VALUES (:type, :day, :time, :name, :location)"
    db.session.execute(sql, {"type":type, "day":day, "time":time, "name":name, "location":location})
    db.session.commit()
    return True

# adds a comment for selected event
def add_comment(user_id, event_id, message):
	sql = "INSERT INTO comments (t_stamp, event_id, message, user_id) VALUES (now(), :event_id, :message, :user_id)"
	db.session.execute(sql, {"event_id":event_id, "message":message, "user_id":user_id})
	db.session.commit()
	return True

# updates an event
def update_event(id, type, day, h_min, name, location):
	sql = "UPDATE events SET type=:type, day=:day, h_min=:h_min, name=:name, location=:location WHERE id=:id"
	db.session.execute(sql, {"id":id, "type":type, "h_min":h_min, "name":name, "day":day, "location":location})
	db.session.commit()
	return True

# deletes event with no possibility to bring it back
def delete_event(id):
	sql = "DELETE FROM sign_ups WHERE event_id=:id"
	db.session.execute(sql, {"id":id})
	db.session.commit()
	sql = "DELETE FROM game_stats WHERE event_id=:id"
	db.session.execute(sql, {"id":id})
	db.session.commit()
	sql = "DELETE FROM comments WHERE event_id=:id"
	db.session.execute(sql, {"id":id})
	db.session.commit()
	sql = "DELETE FROM events WHERE id=:id"
	db.session.execute(sql, {"id":id})
	db.session.commit()
	return True
