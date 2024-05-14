import sqlite3
import firebase_admin
from firebase_admin import firestore

firebase_admin.initialize_app()

conn = sqlite3.connect('/Users/dlaczegociasteczkochinskie/Desktop/INZYNIERKA/RMS/RMS/app/data-dev.sqlite')
cursor = conn.cursor()

cursor.execute('SELECT * FROM users')
data = cursor.fetchall()

formatted_data = []
for row in data:
    doc = {
        'id': row[0],
        'email': row[1],
        'address': row[2],
        'name': row[3],
        'total': row[4],
        'items': row[5].split(",") if row[5] else []
    }
    formatted_data.append(doc)

db = firestore.client()
for doc in formatted_data:
    db.collection('previous_orders').add(doc)

conn.close()
