import jwt
import datetime

from functools import wraps
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity

server = Flask(__name__)
server.config['JWT_SECRET_KEY'] = 'chave_exemplo'
jwt_handler = JWTManager(server)

users = {
    'user1': {'password': 'password_user1'}
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({"message": 'token missing'}), 401

        try:
            data = jwt.decode(token, 'chave_exemplo')
            print(data)
        except:
            return jsonify({"message": f'token invalid'}), 401

        return f(*args, **kwargs)
    return decorated

@server.route('/login')
def login():
    username = request.args.get('login')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'message': 'Credenciais inválidas'}), 401

    if users.get(username) and users[username]['password'] == password:
        access_token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, server.config['JWT_SECRET_KEY'])
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401


@server.route('/protected', methods=['GET'])
@token_required
def get_user_id_from_token():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    server.run()
