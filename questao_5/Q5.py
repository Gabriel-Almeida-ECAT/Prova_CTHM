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