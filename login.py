from flask import Blueprint,request
import sqlite3
import bcrypt
import datetime
import logging

login = Blueprint('login', __name__)

@login.route('/login', methods=['POST'])
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
        logging.log(mailaddr, logindate, loginip, 'failed, user not found')
        return False
    
    salt = result[2]
    password = salt + password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)
    
    if result[1] == password:
        logging.log(mailaddr, logindate, loginip, 'success')
        return True
    else:
        logging.log(mailaddr, logindate, loginip, 'failed, wrong password')
        return False