from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import ChangeEmailForm, LoginForm, PasswordResetForm, PasswordResetRequestForm, RegistrationForm, ChangePasswordForm
from ..email import send_email
from werkzeug.security import generate_password_hash
import logging

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/email/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_doc = db.collection('users').where('email', '==', form.email.data).get()
        if user_doc:
            user_data = user_doc[0].to_dict()
            if user_data and User.verify_password(user_data['password'], form.password.data):
                user = User.from_dict(user_data)
                login_user(user, form.remember_me.data)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.dashboard')
                return redirect(next)
        flash('Nieprawidłowa nazwa użytkownika lub hasło.')

    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = generate_password_hash(form.password.data)

        user_doc = db.collection('users').where('email', '==', email).get()
        if user_doc:
            flash('Ten e-mail należy do już zarejestrowanego użytkownika!')
            return render_template('auth/register.html', form=form)

        user = User(email=email, username=username, password=password)
        db.collection('users').add(user.to_dict())
        flash('Rejestracja zakończona sukcesem.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Zostałeś wylogowany.')
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        user_ref = db.collection('users').document(current_user.id)
        user_ref.update({'confirmed': True})
        flash('Potwierdziłeś konto!')
    else:
        flash('Link potwierdzający jest nieprawidłowy lub wygasł :(')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    try:
        token = current_user.generate_confirmation_token()
        send_email(current_user.email, 'Potwierdź swoje konto', 'auth/email/confirm', user=current_user, token=token)
        flash('Nowy link potwierdzający został wysłany na podany adres e-mail')
    except Exception as e:
        logging.error(f"Error sending email: {e}")
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = generate_password_hash(form.password.data)
            user_ref = db.collection('users').document(current_user.id)
            user_ref.update({'password': current_user.password})
            flash('Your password has been updated')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password')
    return render_template('auth/change_password.html', form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user_doc = db.collection('users').where('email', '==', form.email.data.lower()).get()
        if user_doc:
            user_data = user_doc[0].to_dict()
            user = User.from_dict(user_data)
            token = user.generate_reset_token()
            send_email(user.email, 'Reset your password', 'auth/email/reset_password', user=user, token=token)
        flash('An email with instructions as to how to reset your password has been sent to your inbox')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            flash('Your password has been updated!')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address', 'auth/email/change_email', user=current_user, token=token)
            flash('An email with instructions as to how to confirm your new email address has been sent to you inbox')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password')
    return render_template('auth/change_email.html', form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        user_ref = db.collection('users').document(current_user.id)
        user_ref.update({'email': current_user.email})
        flash('Your email address has been updated')
    else:
        flash('Invalid')
    return redirect(url_for('main.index'))
