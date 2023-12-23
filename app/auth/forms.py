from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')

class RegistrationForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(1, 64), 
                                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                   'Nazwa użytkownika może składać się jedynie z liter, cyfr, kropek'
                                                                   'i znaków podkreślenia')])
    password = PasswordField('Hasło', validators=[DataRequired(), EqualTo('password2', message='Hasła muszą być identyczne!')])
    password2 = PasswordField('Potwierdź hasło', validators=[DataRequired()])
    submit = SubmitField('Zarejestruj')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Ten e-mail należy do już zarejestrowanego użytkownika!')
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Ta nazwa użytkownika jest już zajęta.')