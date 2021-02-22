from wtforms import Form, IntegerField, StringField, PasswordField, validators, TextField, HiddenField, SubmitField, RadioField, DateField, TimeField, BooleanField, SelectField, FieldList, FormField

class RegistrationForm(Form):
	username = StringField('Käyttäjätunnus', [validators.DataRequired(), validators.Length(min=3, max=25)])
	password = PasswordField('Salasana', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Salasana uudelleen')
	first_name = StringField('Etunimi', [validators.Length(min=3, max=25)])
	last_name = StringField('Sukunimi', [validators.Length(min=3, max=40)])
	player = BooleanField('Olen pelaaja')
	jersey = IntegerField('Pelinumero', [validators.DataRequired(), validators.NumberRange(min=0, max=99)], default=0)
	height = IntegerField('Pituus', [validators.NumberRange(min=0, max=300)], default=0)
	weight = IntegerField('Paino', [validators.NumberRange(min=0, max=300)], default=0)
	position = SelectField('Pelipaikka', choices=[('G','Takamies'), ('F','Laituri'), ('C','Sentteri')])

class CommentForm(Form):
	message = TextField([validators.DataRequired()])
	event_id = HiddenField('event_id')
	user_id = HiddenField('user_id')
	submit = SubmitField('Kommentoi')

class SignForm(Form):
	user_id = HiddenField('user_id')
	event_id = HiddenField('event_id')
	player_in = SubmitField(label='IN')
	player_out = SubmitField(label='OUT')

class EditEventForm(Form):
	name = StringField('Tapahtuma', [validators.Length(min=1, max=40)])
	type = RadioField('Tapahtumatyyppi', choices=[('0', 'Harjoitukset'), ('1', 'Ottelu')])
	day = DateField('Päivämäärä', [validators.Required()])
	time = TimeField('Aika', [validators.Required()], format='%H:%M')
	location = StringField('Paikka', [validators.Length(min=1, max=40)])
	submit = SubmitField('Tallenna muutokset')

class StatForm(Form):
	event_id = HiddenField('event_id')
	player_id = HiddenField('player_id')
	min = TimeField('min', [validators.Required()], format='%M:%S', default=0)
	fg = IntegerField('2P', [validators.Required()], default=0)
	fg_a = IntegerField('2PA', [validators.Required()], default=0)
	ft = IntegerField('1P', [validators.Required()], default=0)
	ft_a = IntegerField('1PA', [validators.Required()], default=0)
	three = IntegerField('3P', [validators.Required()], default=0)
	three_a = IntegerField('3PA', [validators.Required()], default=0)
	dreb = IntegerField('PL', [validators.Required()], default=0)
	oreb = IntegerField('HL', [validators.Required()], default=0)
	foul = IntegerField('V', [validators.Required()], default=0)
	ass = IntegerField('S', [validators.Required()], default=0)
	tover = IntegerField('M', [validators.Required()], default=0)
	steal = IntegerField('R', [validators.Required()], default=0)
	block = IntegerField('B', [validators.Required()], default=0)

class TeamClassForm(Form):
	stats = FieldList(FormField(StatForm))

class DeleteEventForm(Form):
	confirm = SubmitField('KYLLÄ')
	cancel = SubmitField('EI')
