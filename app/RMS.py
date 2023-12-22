# from flask import Flask, render_template, url_for, redirect, request, flash, Blueprint
# from flask_login import login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError
# from flask_bcrypt import Bcrypt
# from flask_socketio import SocketIO, emit

# socketio = SocketIO(app)
# bcrypt = Bcrypt(app)
# db.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

# @login_manager.user_loader
# def load_user(user_id):
#      return User.session.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)


# class RegisterForm(FlaskForm):
#     username = StringField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Username"})
    
#     password = PasswordField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Password"})
    
#     submit = SubmitField("Register")

#     def validate_username(self, username):
#         existing_user_username = User.query.filter_by(
#             username=username.data).first()
#         if existing_user_username:
#              raise ValidationError(
#                   "There already is a user with that username. Choose a different one.")
        
# class LoginForm(FlaskForm):
#     username = StringField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Username"})
    
#     password = PasswordField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Password"})
    
#     submit = SubmitField("Login")

# with app.app_context():
#         db.create_all()

# @app.route('/')
# def home():
#     return render_template('home.html')

# @socketio.on('connect')
# def handle_connect():
#     username = request.args.get('username')
#     emit('user_connected', {'username': username}, broadcast=True)

# @socketio.on('message')
# def handle_message(message):
#     username = request.args.get('username')
#     emit('message', {'username': username, 'message': message}, broadcast=True)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#          user = User.query.filter_by(username=form.username.data).first()
#          if user:
#               if bcrypt.check_password_hash(user.password, form.password.data):
#                    login_user(user)
#                    return redirect(url_for('dashboard'))
#     return render_template('login.html', form=form)

# @app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#      return render_template('dashboard.html')

# @app.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#      logout_user()
#      return redirect(url_for('home'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()

#     if form.validate_on_submit():
#          hashed_password = bcrypt.generate_password_hash(form.password.data)
#          new_user = User(username=form.username.data, password=hashed_password)
#          db.session.add(new_user)
#          db.session.commit()
#          return redirect(url_for('login'))

#     return render_template('register.html', form=form)

# if __name__ == '__main__':
#     socketio.run(app)

import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)