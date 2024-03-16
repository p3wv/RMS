from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, SelectField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_wtf.csrf import CSRFProtect

from ..models import Role, User


class OrderForm(FlaskForm):
    name = StringField('Name visible on your order:', validators=[DataRequired()])
    address = StringField('Delivery address:', validators=[DataRequired(), Length(6, 20)])
    email = StringField('Your e-mail (we will use it for contact purposes only)', validators=[DataRequired(), Length(1, 64), Email()])
    total_amount = HiddenField()
    submit = SubmitField('Submit')


    class Meta:
        csrf = True
    

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Nazwa użytkownika', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Username must consist only of letters, digits, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Name', validators=[Length(1, 64)])
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('This e-mail address is already in use')
        
    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already in use')
