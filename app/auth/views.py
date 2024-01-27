from crypt import methods
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_migrate import current
from sqlalchemy import URL
from . import auth
from .. import db
from ..models import User
from .forms import ChangeEmailForm, LoginForm, PasswordResetForm, PasswordResetRequestForm, RegistrationForm, ChangePasswordForm
from ..email import send_email

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
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Nieprawidłowa nazwa użytkownika lub hasło.')

    return render_template('auth/login.html', form=form)

import logging

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        logging.info('Form is validated')
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data) # type: ignore
        db.session.add(user)
        db.session.commit()
        logging.info('User added to the database')
        try:
            token = user.generate_confirmation_token()
            send_email(user.email, 'Potwierdź swoje konto',
                    'auth/email/confirm', user=user, token=token)
            flash('Na podany adres e-mail wysłano prośbę o potwierdzenie konta')
            return redirect(url_for('main.index'))
        except Exception as e:
            logging.error(f'Error sending email: {e}')
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
        db.session.commit()
        flash('Potwierdziłeś konto!')
    else:
        flash('Link potwierdzający jest nieprawidłowy lub wygasł :(')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    try:
        token = current_user.generate_confirmation_token()
        send_email(current_user.email, 'Potwierdź swoje konto',
                'auth/email/confirm', user=current_user, token=token)
        flash('Nowy link potwierdzający został wysłany na podany adres e-mail')
    except Exception as e:
        print(f"Error sending email: {e}")
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
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
        user = User.query.filter_by(email=form.email.data.lower()).first() # type: ignore
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset your password',
                       'auth/email/reset_password',
                       user=user, token=token)
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
            db.session.commit()
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
            new_email = form.email.data.lower() # type: ignore
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions as to how to confirm your new email address has been'
                  'sent to you inbox')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password')
    return render_template('auth/change_email.html', form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated')
    else:
        flash('Invalid')
    return redirect(url_for('main.index'))