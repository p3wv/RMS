from google.cloud import firestore

db = firestore.Client()

def get_user_by_email(email):
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).stream()
    user = None
    for doc in query:
        user = doc.to_dict()
        user['id'] = doc.id #type: ignore
        break
    return user

def create_user(email, username, password):
    user_ref = db.collection('users').add({
        'email': email,
        'username': username,
        'password': password
    })
    return user_ref
