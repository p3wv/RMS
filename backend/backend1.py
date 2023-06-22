from urllib import request
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/add-address', methods=['POST'])
def add_address():
    address = request.form.get('address')

    return jsonify({'message': 'Address added successfully'})

if __name__ == '__main__':
    app.run()
