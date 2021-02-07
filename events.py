from db import db
import users

def get_events():
    result = db.session.execute("SELECT E.type, E.day, E.h_min, E.name, E.id, E.location "\
                                "FROM events E " \
                                "WHERE E.day >= now() " \
                                "ORDER BY E.day DESC LIMIT 10")
    return result.fetchall()



def get_comments():
    result = db.session.execute("SELECT C.tstamp, C.event_id, C.user_id, C.message, U.first_name, U.last_name " \
                                "FROM comments C " \
                                "LEFT JOIN users U on U.id=C.user_id "\
                                "LEFT JOIN events E on E.id=C.event_id "\
                                "WHERE E.day >= now() "\
                                "ORDER BY C.tstamp")

    return result.fetchall()


def get_sign_ups():

    result = db.session.execute("SELECT U.first_name, S.event_id, S.sign_up "\
                                "FROM users U "\
                                "LEFT JOIN sign_ups S ON S.user_id=U.id "\
                                "LEFT JOIN events E ON S.event_id=E.id "\
                                "ORDER BY E.day")
    return result.fetchall()

def add_event(type, day, time, name, location):
    sql = "INSERT INTO events (type, day, h_min, name, location) VALUES (:type, :day, :time, :name, :location)"
    db.session.execute(sql, {"type":type, "day":day, "time":time, "name":name, "location":location})
    db.session.commit()
    return True
