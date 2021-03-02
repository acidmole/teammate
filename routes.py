from app import app
from flask import render_template, redirect, request, flash
from db import db
from forms import RegistrationForm, CommentForm, SignForm, EditEventForm, ConfirmDeleteForm, EditInfoForm

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
	form = RegistrationForm(request.form)

	if request.method == "GET":
		return render_template("register.html", form=form)

	if request.method == "POST" and form.validate():
		if users.new_user(form.username.data, form.password.data, form.first_name.data, form.last_name.data):
			flash ('Rekisteröityminen onnistui')
			if (form.player.data == True):
				if players.new_player(form.username.data, form.jersey.data, form.height.data, form.weight.data, form.position.data):
					return redirect("/")
				else: render_template("error.html",message="Rekisteröinti ei onnistunut")
			else:
					return redirect("/")
		else:
			return render_template("error.html",message="Rekisteröinti ei onnistunut")

# lists future or past events
@app.route("/events", methods=["GET", "POST"])
def list_events():

	# selected timespan for events. by default only future events
	# [1] = next week
	# [2] = this month
	# [3] = everything in the past
	ts = int(request.args.get('timespan', 1))-1
	ts_req= ["E.day >= now()", "(E.day::date - now()::date) >= 0 AND (E.day::date - now()::date) <= 7",\
	"EXTRACT(MONTH FROM now())=EXTRACT(MONTH FROM E.day) AND EXTRACT(YEAR FROM now())=EXTRACT(YEAR FROM E.day)",\
	"E.day < now()"]


	form = CommentForm(request.form)
	s_form = SignForm(request.form)

	if request.method == "GET":
		listed_events = events.get_all_events(ts_req[ts])
		sign_ups = events.get_all_sign_ups(ts_req[ts])
		sign_outs = events.get_all_sign_outs(ts_req[ts])
		comments = events.get_all_comments(ts_req[ts])
		if users.is_admin():
			mod_rights = True
		else:
			mod_rights =  False
		return render_template("events_list.html", events=listed_events, sign_ups=sign_ups, sign_outs=sign_outs, comments=comments, form=form, s_form=s_form, mod_rights=mod_rights)

	if request.method == "POST":

		if form.submit.data and form.validate():
			if events.add_comment(form.user_id.data, form.event_id.data, form.message.data):
				return redirect("/events")
			else:
				return render_template("error.html", message="Kommentin lisääminen ei onnistunut")

		if s_form.player_in.data and s_form.validate():
			if events.sign_up(s_form.user_id.data, s_form.event_id.data, "t"):
				return redirect("/events")
			else:
				return render_template("error.html",message="Ilmoittautuminen ei onnistunut")
		elif s_form.validate() and s_form.player_out.data:
				if events.sign_up(s_form.user_id.data, s_form.event_id.data, "f"):
					return redirect("/events")
				else:
					return render_template("error.html",message="Ilmoittautuminen ei onnistunut")

@app.route("/event/<int:id>", methods=["GET", "POST"])
def event_info(id):

	form = CommentForm(request.form)
	s_form = SignForm(request.form)

	if request.method == "GET":
		event = events.get_event_info(id)
		sign_ups = events.get_sign_ups(id)
		sign_outs = events.get_sign_outs(id)
		comments = events.get_comments(id)
		if users.is_admin():
			mod_rights = True
		else:
			mod_rights =  False

	if request.method == "POST":

		if form.submit.data and form.validate():
			if events.add_comment(form.user_id.data, form.event_id.data, form.message.data):
				return redirect("/events")
			else:
				return render_template("error.html", message="Kommentin lisääminen ei onnistunut")

		if s_form.player_in.data and s_form.validate():
			if events.sign_up(s_form.user_id.data, s_form.event_id.data, "t"):
				return redirect("/events")
			else:
				return render_template("error.html",message="Ilmoittautuminen ei onnistunut")
		elif s_form.validate() and s_form.player_out.data:
				if events.sign_up(s_form.user_id.data, s_form.event_id.data, "f"):
					return redirect("/events")
				else:
					return render_template("error.html",message="Ilmoittautuminen ei onnistunut")

	return render_template("event.html", event=event, sign_ups=sign_ups, sign_outs=sign_outs, comments=comments, form=form, s_form=s_form, mod_rights=mod_rights)

@app.route("/event/edit/<int:id>", methods=["GET", "POST"])
def event_edit(id):

	if users.is_admin():
		form = EditEventForm(request.form)
		if request.method == "GET":
			event = events.get_event_info(id)
			return render_template("edit_event.html", event=event, form=form)
		if request.method == "POST":
			if form.submit.data:
				if events.update_event(id, form.type.data, form.day.data, form.time.data, form.name.data, form.location.data):
					return redirect("/events")
				else:
					return render_template("error.html",message="Virhe päivityksessä")
	else:
		return render.template("error.html", message="Ei oikeutta")


@app.route("/events/add_event", methods=["GET","POST"])
def add_event():
	if users.is_admin():
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
	else:
		return render_template("error.html")

@app.route("/event/delete/<int:id>", methods=["GET", "POST"])
def delete_event(id):
	if users.is_admin():
		form = ConfirmDeleteForm(request.form)
		if request.method == "GET":
			event = events.get_event_info(id)
			return render_template("delete_event.html", event=event, form=form)
		if request.method == "POST":
			if form.confirm.data:
				if events.delete_event(id):
					return redirect("/events")
				else: return render_template("error.html", message="Tapahtuman poisto ei onnistunut")
			else:
				return redirect("/events")

@app.route("/players")
def player_list():

	if users.is_admin():
		mod_rights = True
	else:
		mod_rights =  False
	player_list = players.get_players()
	return render_template("player_list.html", players=player_list, mod_rights=mod_rights)


@app.route("/players/<int:id>")
def player_info(id):
	compared_id = request.args.get('compare_to', None)
	player_list = players.get_players_without(id)
	player = players.get_player(id)
	top_points = players.get_top_points(id)
	top_rebs = players.get_top_rebs(id)
	top_ass = players.get_top_ass(id)
	top_steal = players.get_top_steal(id)
	top_block = players.get_top_block(id)
	attendance = players.get_player_attendance(id)

	compared_player = players.get_player(compared_id)
	return render_template("player.html", person_info=player, players=player_list, top_points=top_points, top_rebs=top_rebs, top_ass=top_ass, top_steal=top_steal, top_block=top_block,
	attendance=attendance, compared_player=compared_player)

@app.route("/users/edit/<int:id>")
def edit_user(id):

	if users.is_admin() or users.user_id == id:
		form = EditInfoForm(request.form)
		if request.method == "GET":
			user = users.get_user(id)
			if players.is_player(id):
				player_id = players.get_player_id(id)
				player = players.get_player(player_id[0])
				return render_template("edit_user.html", user=user, player=player, form=form)
			else:
				return render_template("edit_user.html", user=user, form=form)
	else:
		return render_template("error.html", message="Ei oikeutta")

@app.route("/users/edit", methods=["POST"])
def user_edit_post():
	form = EditInfoForm(request.form)
	id = users.user_id()
	if users.is_admin() or users.user_id == id:
		if users.update_user(id, form.first_name.data, form.last_name.data):
			player_id = players.get_player_id(id)
			if players.update_player(player_id[0], form.jersey.data, form.height.data, form.weight.data, form.position.data):
				return redirect("/users")
			else:
				render_template("error.html", message="Päivitys ei onnistunut")
		else:
			render_template("error.html", message="Päivitys ei onnistunut")
	else:
		return render_template("error.html", message="Ei oikeutta")

@app.route("/users/delete/<int:id>", methods=["GET", "POST"])
def delete_user(id):
	if users.is_admin() or users.user_id == id:
		form = ConfirmDeleteForm(request.form)

		if request.method == "GET":
			del_user = users.get_user(id)
			return render_template("delete_user.html", del_user=del_user, form=form)

		if request.method == "POST":
			if form.confirm.data:
				if users.delete_user(id):
					return redirect("/users")
				else: return render_template("error.html", message="Pelaajan poisto ei onnistunut")
			else:
				return redirect("/users")
	else:
		return render_template("error.html", message="Ei oikeutta")


@app.route("/users")
def list_users():
	userlist = users.get_all_users()
	if users.is_admin():
		mod_rights = True
	else:
		mod_rights =  False
	return render_template("users_list.html", userlist=userlist, mod_rights=mod_rights)

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

@app.route("/stats/add_stats", methods=["GET", "POST"])
def add_stats():
	if users.is_admin():
		form = EditEventForm(request.form)
		if request.method=="GET":
			games = stats.get_games()
			stats = stats.get_game_stats()
		return redirect("/")

@app.route("/stats/practice")
def practice_stats():
	most_in = stats.get_attendance_stats()
	pop_event = stats.get_attendance_pct()
	return render_template("practice_stats.html", most_in=most_in, pop_event=pop_event)
