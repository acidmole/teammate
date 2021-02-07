from db import db

#returns a list of games with stats
def get_games():
    result = db.session.execute("SELECT DISTINCT(G.event_id), E.name, E.day "\
                                "FROM game_stats G " \
                                "LEFT JOIN events E ON G.event_id=E.id")
    return result.fetchall()

#returns a list of all players' personal average stats
def get_personal_stats():
    result = db.session.execute("SELECT G.player_id, U.first_name, U.last_name, P.jersey_number, COUNT(G.player_id), TO_CHAR(AVG(G.mins), 'MI:SS'), ROUND(AVG (2*G.fg + G.ft + 3*G.three),1), "\
                                "ROUND(AVG(G.dreb+G.oreb),1) "\
                                "FROM game_stats G " \
                                "LEFT JOIN players P ON G.player_id = P.id " \
                                "LEFT JOIN users U ON P.user_id = U.id " \
                                "GROUP BY G.player_id, U.first_name, U.last_name, P.jersey_number " \
                                "ORDER BY P.jersey_number")
    return result.fetchall()

# returns a list of separated game stats
def get_game_stats():
    result = db.session.execute("SELECT E.id, E.name, E.day, SUM(fg), SUM(fg_a), ROUND(100.0 * SUM (G.fg) / SUM(G.fg_a),1), SUM(ft), SUM(ft_a), "\
                                "ROUND(100.0 * SUM (G.ft) / SUM(G.ft_a),1), SUM(three), SUM(three_a), ROUND(100.0 * SUM (G.three) / SUM(G.three_a),1), "\
                                "SUM(foul), sum(dreb), sum(oreb), sum(tover), sum(steal), sum(block), sum(ass) "\
                                "FROM game_stats G "\
                                "LEFT JOIN events E ON E.id=G.event_id "\
                                "GROUP BY E.id, E.name, E.day "\
                                "ORDER BY E.day")
    return result.fetchall()

#returns team's average game stats
def get_team_stats():
    result = db.session.execute("SELECT ROUND (1.0*SUM(fg)/COUNT(DISTINCT G.event_id),1), ROUND(1.0*SUM(fg_a) / COUNT(DISTINCT G.event_id),1), ROUND(100.0 * SUM(fg) / NULLIF(SUM(fg_a),0),1), "\
                                "ROUND(1.0*SUM(ft) / COUNT(DISTINCT G.event_id),1), ROUND(1.0* SUM(ft_a) / COUNT(DISTINCT G.event_id),1), ROUND(100.0 * SUM (ft) / NULLIF(SUM(ft_a),0),1), "\
                                "ROUND(1.0*SUM(three) / COUNT(DISTINCT G.event_id),1), ROUND(1.0* SUM(three_a) / COUNT(DISTINCT G.event_id),1), ROUND(100.0 * SUM (three) / NULLIF(SUM(three_a),0),1), "\
                                "ROUND(1.0*SUM(foul) / COUNT(DISTINCT G.event_id),1), ROUND(1.0*SUM(dreb) / COUNT(DISTINCT G.event_id),1), ROUND(1.0*SUM(oreb) / COUNT(DISTINCT G.event_id),1), " \
                                "ROUND(1.0*SUM(tover) / COUNT(DISTINCT G.event_id),1), ROUND(1.0*SUM(steal) / COUNT(DISTINCT G.event_id),1), ROUND(1.0*SUM(block) / COUNT(DISTINCT G.event_id),1), "\
                                "ROUND(1.0*SUM(ass) / COUNT(DISTINCT G.event_id),1) " \
                                "FROM game_stats G")
    return result.fetchall()


#returns a single game's separated stats
def get_single_game_stats(id):
    sql = ("SELECT U.first_name, U.last_name, P.jersey_number, G.mins, G.fg, G.fg_a, ROUND (100.0* G.fg / NULLIF(G.fg_a,0),1), G.ft, G.ft_a, " \
           "ROUND(100.0* G.ft / NULLIF(G.ft_a, 0),1), G.three, G.three_a, ROUND(100.0*G.ft / NULLIF(G.ft_a, 0)), G.dreb, G.oreb, G.foul, G.ass, G.tover, G.steal, G.block, "\
           "(2*fg + ft + 3*three) "\
           "FROM game_stats G "\
           "LEFT JOIN players P ON G.player_id = P.id "\
           "LEFT JOIN users U ON P.user_id = U.id "\
           "WHERE G.event_id=:id "\
           "GROUP BY U.first_name, U.last_name, P.jersey_number, G.mins, G.fg, G.fg_a, G.ft, G.ft_a, G.three, G.three_a, G.dreb, G.oreb, G.foul, G.ass, G.tover, G.steal, G.block "\
           "ORDER BY P.jersey_number")
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

# returns a single game's summed stats
def get_single_game_summary_stats(id):
    sql = ("SELECT SUM(mins), SUM(fg), SUM(fg_a), ROUND(100.0 * SUM (fg) / NULLIF(SUM(fg_a),0),1), SUM(ft), SUM(ft_a), "\
          "ROUND(100.0 * SUM(ft) / NULLIF(SUM(ft_a),0),1), SUM(three), SUM(three_a), ROUND(100.0 * SUM (three) / NULLIF(SUM(three_a),0),1), "\
          "SUM(dreb), SUM(oreb), SUM(foul), SUM(ass), SUM(tover), SUM(steal), SUM(block), SUM(2*fg + ft + 3*three) "\
          "FROM game_stats "\
          "WHERE event_id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()
