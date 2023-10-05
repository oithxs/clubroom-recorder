from flask import Blueprint,request,jsonify
from app.lib import log
import sqlite3
import bcrypt
import datetime
import os
import dotenv

blueprint = Blueprint('login', __name__)
dotenv.load_dotenv('.env')

@blueprint.route('/login', methods=['POST'])
def login():
    postdata = request.get_json()
    mailaddr = postdata['mailaddr']
    password = postdata['password']
    logindate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if os.getenv('USE_REVERSE_PROXY') == 'true':
        loginip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        loginip = request.remote_addr

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('SELECT * FROM user WHERE mailaddr = ?', (mailaddr,))
    result = c.fetchone()
    conn.close()

    if result is None:
        log(mailaddr, logindate, loginip, '[login]failed, user not found')
        return jsonify({'result': 'failed', 'reason': 'user not found or wrong password'}), 401

    salt = result[2]
    password = salt + password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)

    if result[1] == password:
        log(mailaddr, logindate, loginip, 'success')
        return jsonify({'result': 'success'}), 200
    else:
        log(mailaddr, logindate, loginip, '[login]failed, wrong password')
        return jsonify({'result': 'failed', 'reason': 'user not found or wrong password'}), 401