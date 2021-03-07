from wtforms import Form, IntegerField, StringField, PasswordField, validators, TextField, HiddenField, SubmitField, RadioField
from wtforms import DateField, TimeField, BooleanField, SelectField, FieldList, FormField
from wtforms.fields.html5 import IntegerField
from wtforms.widgets.html5 import NumberInput
from db import db
import players, events

class RegistrationForm(Form):
	username = StringField('Käyttäjätunnus', [validators.DataRequired(), validators.Length(min=3, max=25)])
	password = PasswordField('Salasana', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Salasana uudelleen')
	first_name = StringField('Etunimi', [validators.Length(min=3, max=25)])
	last_name = StringField('Sukunimi', [validators.Length(min=3, max=40)])
	player = BooleanField('Olen pelaaja')
	jersey = IntegerField('Pelinumero', default=0)
	height = IntegerField('Pituus', default=0)
	weight = IntegerField('Paino', default=0)
	position = SelectField('Pelipaikka', choices=[('G','Takamies'), ('F','Laituri'), ('C','Sentteri')])

class EditInfoForm(Form):
	first_name = StringField('Etunimi', [validators.Length(min=3, max=25)])
	last_name = StringField('Sukunimi', [validators.Length(min=3, max=40)])
	jersey = IntegerField('Pelinumero', [validators.DataRequired(), validators.NumberRange(min=0, max=99)], default=0)
	height = IntegerField('Pituus', [validators.NumberRange(min=0, max=300)], default=0)
	weight = IntegerField('Paino', [validators.NumberRange(min=0, max=300)], default=0)
	position = SelectField('Pelipaikka', choices=[('G','Takamies'), ('F','Laituri'), ('C','Sentteri')])
	user_id = HiddenField('user_id')
	submit = SubmitField('Tallenna muutokset')
	cancel = SubmitField('Hylkää muutokset')
	csrf_token = HiddenField('csrf_token')

class CommentForm(Form):
	message = TextField([validators.DataRequired()])
	event_id = HiddenField('event_id')
	user_id = HiddenField('user_id')
	submit = SubmitField('Kommentoi')
	csrf_token = HiddenField('csrf_token')

class SignForm(Form):
	user_id = HiddenField('user_id')
	event_id = HiddenField('event_id')
	player_in = SubmitField(label='IN')
	player_out = SubmitField(label='OUT')
	csrf_token = HiddenField('csrf_token')

class EditEventForm(Form):
	name = StringField('Tapahtuma', [validators.Length(min=1, max=40)])
	type = RadioField('Tapahtumatyyppi', choices=[('0', 'Harjoitukset'), ('1', 'Ottelu')], default=0)
	day = DateField('Päivämäärä', [validators.Required()], format='%d-%m-%Y')
	time = TimeField('Aika', [validators.Required()], format='%H:%M')
	location = StringField('Paikka', [validators.Length(min=1, max=40)])
	submit = SubmitField('Tallenna muutokset')
	csrf_token = HiddenField('csrf_token')

class StatForm(Form):
	player_id = SelectField('Player_id', default=0)
	event_id = SelectField('event_id', default=0)
	min = TimeField('min', format='%M:%S')
	fg = IntegerField('2P', [validators.NumberRange(min=0, max=200)], widget=NumberInput(step=1), default=0)
	fg_a = IntegerField('2PA', default=0)
	ft = IntegerField('1P', default=0)
	ft_a = IntegerField('1PA', default=0)
	three = IntegerField('3P', default=0)
	three_a = IntegerField('3PA', default=0)
	dreb = IntegerField('PL', default=0)
	oreb = IntegerField('HL', default=0)
	foul = IntegerField('V',  default=0)
	ass = IntegerField('S', default=0)
	tover = IntegerField('M', default=0)
	steal = IntegerField('R', default=0)
	block = IntegerField('T', default=0)
	submit = SubmitField('LÄHETÄ')
	cancel = SubmitField('PERUUTA')
	csrf_token = HiddenField('csrf_token')

# this is not in use atm
class InsertStatForm(Form):

	games = events.get_games()
	games_list =  [(g[2], (str(g[0]) + " " + g[1])) for g in games]
	games_list.append([0, "Valitse ottelu"])
	s_form = StatForm()
	statistics = FieldList(FormField(StatForm), min_entries=12, max_entries=12)
	event_id = SelectField('event_id', choices=games_list, default=0)
	submit = SubmitField('LÄHETÄ')
	cancel = SubmitField('PERUUTA')

class ConfirmDeleteForm(Form):
	confirm = SubmitField('KYLLÄ')
	cancel = SubmitField('EI')
	csrf_token = HiddenField('csrf_token')

class EventSelectForm(Form):
	games = events.get_games()
	games_list =  [(g[2], (str(g[0]) + " " + g[1])) for g in games]
	games_list.append([0, "Valitse ottelu"])
	event_id = SelectField('event_id', choices=games_list, default=0)
	csrf_token = HiddenField('csrf_token')
