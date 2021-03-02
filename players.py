from db import db

# returns a list of all players excluding graveyard
def get_players():
    result = db.session.execute("SELECT U.first_name, U.last_name, P.jersey_number, P.id "\
                                "FROM users U "\
                                "LEFT JOIN players P ON P.user_id=U.id "\
                                "WHERE U.visible='t' "\
                                "ORDER BY P.jersey_number")
    return result.fetchall()


# returns a summary of a single player
def get_player(id):
	sql = "SELECT U.first_name, U.last_name, P.jersey_number, P.height, P.weight, " \
	"ROUND(AVG(2*G.fg + G.ft + 3*G.three),1), ROUND(AVG(dreb + oreb),1), ROUND(AVG(ass),1), ROUND(AVG(steal),1), P.position " \
	"FROM players P "\
	"LEFT JOIN users U ON U.id=P.user_id "\
	"LEFT JOIN game_stats G ON G.player_id = P.id "\
	"WHERE P.id=:id AND U.visible='t'" \
	"GROUP BY U.first_name, U.last_name, P.jersey_number, P.height, P.weight, P.id"

	result = db.session.execute(sql, {"id":id})
	return result.fetchone()

# returns player's 5 last attendance
def get_player_attendance(id):
	sql = "SELECT E.day, E.h_min, E.name FROM sign_ups S "\
			"LEFT JOIN events E ON E.id=S.event_id "\
			"LEFT JOIN users U ON U.id=S.user_id "\
			"LEFT JOIN players P ON U.id=P.user_id "\
			"WHERE P.id=:id "\
			"ORDER BY S.id DESC LIMIT 5";
	result = db.session.execute(sql, {"id":id})
	return result.fetchall()


# returns a list of all except one
def get_players_without(id):
    sql = ("SELECT P.id, P.jersey_number, U.first_name, U.last_name " \
           "FROM players P "\
           "LEFT JOIN users U on U.id = P.user_id " \
           "WHERE P.id<>:id AND U.visible='t' "\
           "ORDER BY P.jersey_number")
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


# returns player's top points performance with game information
def get_top_points(id):
    sql = ("SELECT MAX(2*fg + ft + 3*three) AS top_points, E.day, E.name "\
           "FROM game_stats G "\
           "LEFT JOIN events E ON E.id=G.event_id "\
           "LEFT JOIN players P ON P.id=G.player_id "\
           "WHERE P.id=:id "\
           "GROUP BY E.day, E.name " \
           "ORDER BY top_points DESC LIMIT 1")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

# returns player's top rebound performance with game information
def get_top_rebs(id):
    sql = ("SELECT MAX(G.dreb+G.oreb) AS top_rebs, E.day, E.name "\
           "FROM game_stats G "\
           "LEFT JOIN events E ON E.id=G.event_id "\
           "LEFT JOIN players P ON P.id=G.player_id "\
           "WHERE P.id=:id "\
           "GROUP BY E.day, E.name " \
           "ORDER BY top_rebs DESC LIMIT 1")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


# returns player's top assist performance with game information
def get_top_ass(id):
    sql = ("SELECT MAX(ass) AS top_ass, E.day, E.name "\
           "FROM game_stats G "\
           "LEFT JOIN events E ON E.id=G.event_id "\
           "LEFT JOIN players P ON P.id=G.player_id "\
           "WHERE P.id=:id "\
           "GROUP BY E.day, E.name " \
           "ORDER BY top_ass DESC LIMIT 1")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


# returns player's top steal performance with game information
def get_top_steal(id):
    sql = ("SELECT MAX(steal) AS top_steal, E.day, E.name "\
           "FROM game_stats G "\
           "LEFT JOIN events E ON E.id=G.event_id "\
           "LEFT JOIN players P ON P.id=G.player_id "\
           "WHERE P.id=:id "\
           "GROUP BY E.day, E.name " \
           "ORDER BY top_steal DESC LIMIT 1")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


#returns player's top block performance with game information
def get_top_block(id):
    sql = ("SELECT MAX(block) AS top_block, E.day, E.name "\
           "FROM game_stats G "\
           "LEFT JOIN events E ON E.id=G.event_id "\
           "LEFT JOIN players P ON P.id=G.player_id "\
           "WHERE P.id=:id "\
           "GROUP BY E.day, E.name " \
           "ORDER BY top_block DESC LIMIT 1")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def get_player_id(user_id):
	sql = "SELECT id FROM players WHERE user_id=:user_id"
	result = db.session.execute(sql, {"user_id":user_id})
	return result.fetchone()


def update_player(id, jersey_number, height, weight, position):
	sql = "UPDATE players SET jersey_number=:jersey_number, height=:height, weight=:weight, position=:position WHERE id=:id"
	db.session.execute(sql, {"jersey_number":jersey_number, "height":height, "weight":weight, "position":position, "id":id})
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

def is_player(user_id):
	sql = "SELECT user_id FROM players WHERE user_id=:user_id"
	result = db.session.execute(sql, {"user_id":user_id})
	id = result.fetchone()
	if id == None:
		return False
	else:
		return True
