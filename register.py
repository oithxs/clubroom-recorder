from flask import Blueprint,request
import sqlite3
import bcrypt
import os.path
import datetime
import json

register = Blueprint('register', __name__)

@register.route('/register', methods=['POST'])
def reg():
    # ユーザーのメールアドレスが既に登録されているかどうかを確認する
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('SELECT * FROM user WHERE mailaddr = ?', (mailaddr,))
    result = c.fetchone()
    conn.close()

    regdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if 'X-Forwarded-For' in request.headers:
        regip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        regip = request.remote_addr

    postdata = request.get_json()
    mailaddr = postdata['mailaddr']
    
    if result is not None:
        return False
    if len(password) < 8:
        return False
    if mailaddr == '' or password == '' or regip == '' or regdate == '':
        return False
    
    # メアドがoit.ac.jp, *.oit.ac.jpでない場合は登録しない
    chkmaildomain = mailaddr.split('@')
    if not chkmaildomain[1].endswith('oit.ac.jp'):
        return False
    
    salt = bcrypt.gensalt()
    password = salt + password.encode('utf-8')
    # パスワードをハッシュ化する
    password = bcrypt.hashpw(password, salt)
    # ユーザーを登録する
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('INSERT INTO user VALUES (?, ?, ?, ?, ?)', (mailaddr, password, salt, regdate, regip))
    conn.commit()
    conn.close()