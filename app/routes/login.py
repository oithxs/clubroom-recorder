from flask import Blueprint,request,jsonify
from app.lib import log
import sqlite3
import bcrypt
import datetime

blueprint = Blueprint('login', __name__)

@blueprint.route('/login', methods=['POST'])
def login():
    postdata = request.get_json()
    mailaddr = postdata['mailaddr']
    password = postdata['password']
    logindate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if 'X-Forwarded-For' in request.headers:
        loginip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        loginip = request.remote_addr

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('SELECT * FROM user WHERE mailaddr = ?', (mailaddr,))
    result = c.fetchone()
    conn.close()

    if result is None:
        log(mailaddr, logindate, loginip, 'failed, user not found')
        return jsonify({'result': 'failed', 'reason': 'user not found or wrong password'}), 401

    salt = result[2]
    password = salt + password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)

    if result[1] == password:
        log(mailaddr, logindate, loginip, 'success')
        return jsonify({'result': 'success'}), 200
    else:
        log(mailaddr, logindate, loginip, 'failed, wrong password')
        return jsonify({'result': 'failed', 'reason': 'user not found or wrong password'}), 401