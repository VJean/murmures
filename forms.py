from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, ValidationError

from models import db, Murmure


class LoginForm(FlaskForm):
    username = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class MurmureForm(FlaskForm):
    publishdate = DateField('publier le', format='%d/%m/%Y', validators=[DataRequired()])
    content = StringField('contenu', validators=[DataRequired()])
    subtext = StringField('texte additionnel', validators=[])

    def validate_publishdate(form, field):
        forbidden = [m[0] for m in db.session.query(Murmure.publishdate).all()]
        if field.data in forbidden:
            raise ValidationError('Un murmure a déjà cette date de publication')
