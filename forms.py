from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, ValidationError

from models import db, Murmure


class LoginForm(FlaskForm):
    username = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class MurmureForm(FlaskForm):
    content = StringField('contenu', validators=[DataRequired()])
    subtext = StringField('texte additionnel', validators=[DataRequired()])
