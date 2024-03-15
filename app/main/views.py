# from ctypes import addressof
from datetime import datetime
# import email
import json
from flask import flash, jsonify, render_template, session, redirect, url_for, request
# from flask import current_app, make_response, abort
from flask_login import login_required, current_user

from app.email import send_order_confirmation_email
# from app.email import send_email
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, NameForm, OrderForm
from .. import db
from ..models import Role, User, Order
# from ..models import Permission
from ..decorators import admin_required
# import app

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/RMS', methods=['GET', 'POST'])
def RMS_index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            # if app.config['RMS_ADMIN']:
            #     send_email(app.config['RMS_ADMIN'], 'New User',
            #                'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.RMS_index'))
    return render_template('RMS_index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())

@main.route('/menu')
def menu():
    cart_items = session.get('cart', [])
    page_number = request.args.get('page', default=1, type=int) 
    return render_template('menu.html', cart_items=cart_items, page_number=page_number)


@main.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

total_amount_storage = None

@main.route('/add_to_cart/<itemName>', methods=['POST'])
def add_to_cart(itemName):
    try:
        cart = session.get('cart', [])
        cart.append({'name': itemName, 'quantity': 1})

        session['cart'] = cart

        return jsonify({'success': True, 'message': f'Item "{itemName}" added to cart'})
    except Exception as e:
        print('Error:', e)
        return jsonify({'success': False, 'error': str(e)})

# @main.route('/add_to_cart/<itemName>', methods=['POST'])
# def add_to_cart(itemName):
#     try:
#         cart = session.get('cart', [])

#         cart.append(itemName)

#         session['cart'] = cart

#         # if itemName in cart:
#         #     cart[itemName]['quantity'] += 1
#         # else:
#         #     cart[itemName] = {'quantity': 1}

#         # session['cart'] = cart

#         return jsonify({'success': True, 'message': f'Item "{itemName}" added to cart'})
#     except Exception as e:
#         print('Error:', e)
#         return jsonify({'success': False, 'error': 'An error occurred while adding the item to the cart'})

@main.route('/save_total_amount', methods=['POST'])
def save_total_amount():
    global total_amount_storage

    try:
        data = request.get_json()
        total_amount = data.get('totalAmount')

        # Assuming you want to store the total amount globally on the server
        total_amount_storage = total_amount

        return jsonify({'success': True})
    except Exception as e:
        print('Error:', e)
        return jsonify({'success': False, 'error': 'An error occurred while saving the total amount'})


# def calculate_total_amount(cart_items):
#     return sum(item['price'] for item in cart_items)


@main.route('/order_confirmation', methods=['GET', 'POST'])
def order_confirmation():
    global total_amount_storage
    total_amount = total_amount_storage

    if total_amount is None:
        flash('Total amount not found')
        redirect(url_for('.cart'))

    form = OrderForm()

    if form.validate_on_submit():

        email = form.email.data
        name = form.name.data
        address = form.address.data

        cart_items_str = request.form.get('cart_items') or request.cookies.get('cart_items')
        print("Cart Items String:", cart_items_str)

        if cart_items_str:
            cart_items = json.loads(cart_items_str)
        else:
            cart_items = []

        items_json = json.dumps(cart_items)

        order = Order(
            email=email,
            name=name,
            address=address,
            total=total_amount,
            items=items_json
        )


        db.session.add(order)
        db.session.commit()

        order_id = order.id
        order = Order.query.get(order.id)
        items = order.get_items()

        print("order after from db: ", items)

        send_order_confirmation_email(email, items)
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('.ordered'))

    return render_template('order_confirmation.html', form=form, total_amount=total_amount)


@main.route('/ordered')
def ordered():
    return render_template('ordered.html')

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        db.session.add(user)
        db.session.commit()
        flash('Profile has been updated')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    return render_template('edit_profile.html', form=form, user=user)