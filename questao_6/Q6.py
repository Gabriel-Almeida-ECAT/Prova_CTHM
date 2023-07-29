import jwt
import datetime

from functools import wraps
from flask import Flask, request, jsonify

server = Flask(__name__)
server.config['JWT_SECRET_KEY'] = 'chave_exemplo'
server.config['current_user'] = ''

users = {
    'user1': {'password': 'password_user1'}
}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({"msg": 'token missing'}), 401

        data = jwt.decode(token, server.config['JWT_SECRET_KEY'], algorithms=['HS256'])

        with open("teste.txt", 'w') as file:
            file.write(str(data))

        if not data:
            return jsonify({"msg": "Signature verification failed"}), 401
        else:
            server.config['current_user'] = data['user']

        return f(*args, **kwargs)

    return decorated


@server.route('/login')
def login():
    username = request.args.get('login')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'msg': 'invalid login or password'}), 401

    if users.get(username) and users[username]['password'] == password:
        access_token = jwt.encode(
            {'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            server.config['JWT_SECRET_KEY']
        )
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'msg': 'invalid login or password'}), 401


@server.route('/get_user_id_from_token')
@token_required
def get_user_id_from_token():
    return jsonify(logged_in_as=server.config['current_user']), 200


if __name__ == '__main__':
    server.run()
