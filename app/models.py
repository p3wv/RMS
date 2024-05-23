from flask_login import UserMixin, AnonymousUserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from datetime import timedelta
from google.cloud import firestore
import json

db = firestore.Client()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user_ref = db.collection('users').document(user_id).get()
    return User.from_dict(user_ref.to_dict()) if user_ref.exists else None

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role:
    def __init__(self, name, permissions=0, default=False):
        self.name = name
        self.permissions = permissions
        self.default = default

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role_ref = db.collection('roles').document(r)
            role = role_ref.get().to_dict()
            if not role:
                role = Role(name=r)
            role['permissions'] = 0 # type: ignore
            for perm in roles[r]:
                role['permissions'] += perm # type: ignore
            role['default'] = (role['name'] == default_role) # type: ignore
            role_ref.set(role) # type: ignore

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin):
    def __init__(self, email, username, password, role=None, confirmed=False, name='', accounted_time=timedelta(), id=None):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.confirmed = confirmed
        self.name = name
        self.accounted_time = accounted_time
        self.id = id

    def account_time(self, time_diff):
        self.accounted_time += time_diff

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            print(f"Error decoding token: {e}")
            return False
        if data.get('confirm') != self.id:
            print("User ID does not match")
            return False
        self.confirmed = True
        user_ref = db.collection('users').document(self.id)
        user_ref.update({'confirmed': True})
        print("User confirmed successfully")
        return True

    @property
    def password(self):
        raise AttributeError('Nie można odczytać atrybutu password.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id}).decode('utf-8') # type: ignore

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        user_ref = db.collection('users').document(data['id']).get()
        return User.from_dict(user_ref.to_dict()) if user_ref.exists else None

    @staticmethod
    def from_dict(source):
        return User(
            email=source.get('email'),
            username=source.get('username'),
            password=source.get('password'),
            role=Role(source.get('role')),
            confirmed=source.get('confirmed', False),
            name=source.get('name', ''),
            accounted_time=timedelta(seconds=source.get('accounted_time', 0)),
            id=source.get('id')
        )

    def to_dict(self):
        return {
            'email': self.email,
            'username': self.username,
            'password': self.password_hash,
            'role': self.role.name if self.role else None,
            'confirmed': self.confirmed,
            'name': self.name,
            'accounted_time': self.accounted_time.total_seconds(),
            'id': self.id
        }

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class Order:
    def __init__(self, email, address, name, total, items, id=None):
        self.email = email
        self.address = address
        self.name = name
        self.total = total
        self.items = items
        self.id = id

    def set_items(self, items):
        self.items = json.dumps(items)

    def get_items(self):
        return json.loads(self.items)

    def to_dict(self):
        return {
            'email': self.email,
            'address': self.address,
            'name': self.name,
            'total': self.total,
            'items': self.items,
            'id': self.id
        }

    @staticmethod
    def from_dict(source):
        return Order(
            email=source.get('email'),
            address=source.get('address'),
            name=source.get('name'),
            total=source.get('total'),
            items=source.get('items'),
            id=source.get('id')
        )

class OrderDone(Order):
    pass

class CartItem:
    def __init__(self, product_name, price, quantity, id=None):
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.id = id

    def to_dict(self):
        return {
            'product_name': self.product_name,
            'price': self.price,
            'quantity': self.quantity,
            'id': self.id
        }

    @staticmethod
    def from_dict(source):
        return CartItem(
            product_name=source.get('product_name'),
            price=source.get('price'),
            quantity=source.get('quantity'),
            id=source.get('id')
        )
