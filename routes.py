from app import app
from flask import render_template, redirect, request
from db import db

import users, events, players, stats

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:

            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        jersey = request.form["jersey"]
        height = request.form["height"]
        weight = request.form["weight"]
        if users.new_user(username, password, first_name, last_name, jersey, height, weight):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/events")
def list_events():

    listed_events = events.get_events()
    sign_ups = events.get_sign_ups()
    comments = events.get_comments()

    return render_template("events.html", events=listed_events, sign_ups=sign_ups, comments=comments)

@app.route("/add_event", methods=["GET","POST"])
def add_event():
    if request.method == "GET":
        return render_template("add_event.html")
    if request.method == "POST":
        type = request.form["type"]
        date = request.form["date"]
        time = request.form["time"]
        name = request.form["name"]
        location = request.form["location"]
        if events.add_event(type, date, time, name, location):
            return redirect("/events")
        else:
            return render_template("error.html",message="Tapahtuman luonti ei onnistunut")


@app.route("/players")
def player_list():
    player_list = players.get_players()
    return render_template("players.html", players=player_list)


@app.route("/players/<int:id>")
def player_info(id):
    # compare_to = request.args["compare_to"]
    player_list = players.get_players_without(id)
    player = players.get_player(id)
    top_points = players.get_top_points(id)
    top_rebs = players.get_top_rebs(id)
    top_ass = players.get_top_ass(id)
    top_steal = players.get_top_steal(id)
    top_block = players.get_top_block(id)

    return render_template("player.html", person_info=player, players=player_list, top_points=top_points, top_rebs=top_rebs, top_ass=top_ass, top_steal=top_steal, top_block=top_block)


@app.route("/stats")
def games():
    games = stats.get_games()
    return render_template("stats.html", games=games)


@app.route("/stats/personal")
def personal_stats():
    personal_stats = stats.get_personal_stats()
    return render_template("personal_stats.html", person_stats=personal_stats)

@app.route("/stats/team")
def team_stats():

    game_stats = stats.get_game_stats()
    team_stats = stats.get_team_stats()
    return render_template("team_stats.html", tstats=game_stats, tstats_avg=team_stats)

@app.route("/stats/<int:id>")
def single_game_stats(id):

    player_stats = stats.get_single_game_stats(id)
    summed = stats.get_single_game_summary_stats(id)
    return render_template("game_stats.html", stats=player_stats, summed=summed)
