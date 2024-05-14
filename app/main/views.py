from datetime import datetime, timedelta
import json
from flask import current_app, flash, jsonify, render_template, session, redirect, url_for, request, send_from_directory
from flask_login import login_required, current_user
from flask_socketio import SocketIO, emit

from ..email import send_order_confirmation_email
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, NameForm, OrderForm
from .. import db
from ..models import Role, User, Order, CartItem
from ..decorators import admin_required

@main.route('/service-worker.js')
def service_worker():
    return send_from_directory('static/js', 'service-worker.js')

@main.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

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

import sqlite3

@main.route('/dashboard')
def dashboard():
    connection = sqlite3.connect('/Users/dlaczegociasteczkochinskie/Desktop/INZYNIERKA/RMS/RMS/app/data-dev.sqlite')
    cursor = connection.cursor()


    connection.commit()


    query = """
            SELECT id, items
            FROM orders
            """

    cursor.execute(query)
    fetched_data = cursor.fetchall()

    orders = []
    for row in fetched_data:
        num_columns = len(row)
        order_id = row[0]

        order_items = row[num_columns - 1]

        if order_items is None or not isinstance(order_items, str):
            print(f"Skipping order {order_id} due to non-string items: {order_items}")
            continue
        else:
            try:
                order_items = json.loads(order_items)
                orders.append({
                    "id": order_id,
                    "items": order_items
                })
            except json.JSONDecodeError:
                print(f"Skipping order {order_id} due to invalid JSON for items")
                continue

    connection.close()
    
    return render_template('dashboard.html', orders=orders)

socketio = SocketIO()

@main.route('/chat')
@login_required
def chat():
    return render_template('chat.html', username=current_user.username)

@socketio.on('message')
def handle_message(message):
    emit('message', {'username': current_user.username, 'message': message}, broadcast=True)

@main.route('/clock_in', methods=['POST'])
def clock_in():
    if current_user.is_authenticated:
        session['clock_in_time'] = datetime.now()

        current_user.accounted_time = timedelta()

        db.session.commit()

    return redirect(url_for('dashboard'))

@main.route('/clock_out', methods=['POST'])
def clock_out():
    if current_user.is_authenticated:
        clockInTime = session.get('clock_in_time')

        if clockInTime:
            clockOutTime = datetime.now()

            timeDiff = clockOutTime - clockInTime

            print(timeDiff)

            current_user.accounted_time += timeDiff

            db.session.commit()


    return redirect(url_for('dashboard'))


@main.route('/move_order/<int:order_id>', methods=['POST'])
def move_order(order_id):
    try:
        connection = sqlite3.connect('/Users/dlaczegociasteczkochinskie/Desktop/INZYNIERKA/RMS/RMS/app/data-dev.sqlite')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO orders_done SELECT * FROM orders WHERE id = ?", (order_id,))
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))

        connection.commit()
        connection.close()

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/previous_orders')
def previous_orders():
    connection = sqlite3.connect('/Users/dlaczegociasteczkochinskie/Desktop/INZYNIERKA/RMS/RMS/app/data-dev.sqlite')
    cursor = connection.cursor()


    connection.commit()


    query = """
            SELECT id, items
            FROM orders_done
            """

    cursor.execute(query)
    fetched_data = cursor.fetchall()

    orders = []
    for row in fetched_data:
        num_columns = len(row)
        order_id = row[0]

        order_items = row[num_columns - 1]

        if order_items is None or not isinstance(order_items, str):
            print(f"Skipping order {order_id} due to non-string items: {order_items}")
            continue
        else:
            try:
                order_items = json.loads(order_items)
                orders.append({
                    "id": order_id,
                    "items": order_items
                })
            except json.JSONDecodeError:
                print(f"Skipping order {order_id} due to invalid JSON for items")
                continue


    connection.close()

    return render_template('previous_orders.html', orders=orders)

@main.route('/menu')
def menu():
    cart_items = session.get('cart', [])
    page_number = request.args.get('page', default=1, type=int) 
    return render_template('menu.html', cart_items=cart_items, page_number=page_number)


@main.route('/cart', methods=['GET', 'POST'])
def cart():
    form = OrderForm()
    return render_template('cart.html', form=form)

def add_item_to_cart(product_name, price, quantity):
    existing_item = CartItem.query.filter_by(product_name=product_name).first()

    if existing_item:
        existing_item.quantity += int(quantity)
    else:
        new_item = CartItem(product_name=product_name, price=price, quantity=int(quantity))
        db.session.add(new_item)

    db.session.commit()
    return True

@main.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()

    try:
        product_name = data.get('productName')
        price = data.get('price')
        quantity = data.get('quantity')

        if not all([product_name, price, quantity]):
            return jsonify({'success': False, 'message': 'Missing required data'}), 400

        if not add_item_to_cart(product_name, price, quantity):
            return jsonify({'success': False, 'message': 'Invalid quantity'}), 400

        return jsonify({'success': True}), 200

    except Exception as e:
        print(f"Error adding item to cart: {e}")
        return jsonify({'success': False}), 500

@main.route('/order_confirmation', methods=['GET', 'POST'])
def order_confirmation():
    form = OrderForm()
    
    cart_items_json = request.form.get('items')
    print('items:', cart_items_json)

    cart_items = json.loads(cart_items_json) if cart_items_json else []

    total_amount = request.form.get('total_amount')
    print(total_amount)

    if not total_amount:
        flash('Total amount not found')
        return redirect(url_for('.cart'))
    elif total_amount == 0:
        flash('No items in cart!')
        return redirect(url_for('.cart'))

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        address = form.address.data

        try:
            order = Order(
                email=email,
                name=name,
                address=address,
                total=total_amount
            )

            order.set_items(cart_items)

            db.session.add(order)
            db.session.commit()

            print("asjhajdhsa:", cart_items)
            send_order_confirmation_email(email, cart_items)
                    
            session.pop('cart', None)
            
            flash('Order placed successfully! An email confirmation has been sent to you.', 'success')
            return redirect(url_for('.ordered'))

        except Exception as e:
                flash('An error occurred while processing your order. Please try again later.', 'error')
                current_app.logger.error('Error processing order: %s', str(e))
                return jsonify({'error': str(e)}), 500

    return render_template('order_confirmation.html', cart_items=cart_items, total_amount=total_amount, form=form)


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