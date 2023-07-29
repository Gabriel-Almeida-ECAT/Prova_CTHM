import datetime

from datetime import datetime
from flask import Flask, request, jsonify

server = Flask(__name__)

@server.before_request
def log_request_info():
    with open("request_time_log.log", "a") as log_file:
        current_time = datetime.now().strftime("%Y.%M.%d %H:%M:%S")
        log_file.write(f"{current_time} - Resquest: {request.method}\n")

@server.route('/save_resquest_time')
def index():
    return jsonify({"Request saved in file": "request_time_log"})

if __name__ == '__main__':
    server.run()


http://127.0.0.1:5000/login?login=user1&password=password_user1
http://127.0.0.1:5000/protected?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidXNlcjEiLCJleHAiOjE2OTA2NjQ4NzN9.3UWLv2YMbY45JyFWoELA91evE2crowYpTS5blz-Ddik