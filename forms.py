from wtforms import Form, IntegerField, StringField, PasswordField, validators

class RegistrationForm(Form):
	username = StringField('Käyttäjätunnus', [validators.Length(min=3, max=25)])
	password = PasswordField('Salasana', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Salasana uudelleen')
	first_name = StringField('Etunimi', [validators.Length(min=3, max=25)])
	last_name = StringField('Sukunimi', [validators.Length(min=3, max=40)])
	jersey = IntegerField('Pelinumero', [validators.NumberRange(min=0, max=99)])
	height = IntegerField('Pituus', [validators.NumberRange(min=0, max=300)])
	weight = IntegerField('Paino', [validators.NumberRange(min=0, max=300)])
