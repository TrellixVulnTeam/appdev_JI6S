from wtforms import *
from wtforms.validators import *
from wtforms.fields.html5 import *

class AdminForm(Form):
    username = StringField('Username', [validators.Length(min=8
                                                          ), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8
                                                            ), validators.DataRequired()])
    code = PasswordField('Code:', [validators.Length(max=150
                                                        ), validators.DataRequired()])

class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])

    email = StringField('Email', [validators.Length(min=1,
                                                    max=150), validators.DataRequired(), validators.email()])
    username = StringField('Username', [validators.Length(min=8
                                                          ), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8
                                                            ), validators.DataRequired(),
                                          EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=8
                                                          ), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8
                                                            ), validators.DataRequired()])
    remember = BooleanField('Remember me')

class EditForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])

    email = StringField('Email', [validators.Length(min=1,
                                                    max=150), validators.DataRequired(), validators.email()])
    username = StringField('Username', [validators.Length(min=8
                                                          ), validators.DataRequired()])

class Payment(Form):
    block_number = StringField('Block Number:', [validators.Length(min=1, max=150), validators.DataRequired()])
    postal_code = StringField('Postal Code:', [validators.Length(min=6, max=6), validators.DataRequired()])

class Reviews(Form):
    review = StringField('Review', [validators.Length(min=1)])


class SeatForm(Form):
    seat = SelectField('Choose your seat here: ', choices=[('1', '1'), ('2', '2'), ('3', '3')], default='')
    name = StringField('Name: ', [validators.Length(min=1, max=150), validators.DataRequired()])

class TemperatureMorning(Form):
    temperature_morning = StringField('Morning Temperature', [validators.DataRequired()])