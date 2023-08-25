from flask import Blueprint,request,jsonify
import sqlite3
import bcrypt
import datetime

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
    password = postdata['password']
    
    if result is not None:
        return jsonify({'result': 'failed', 'reason': 'user already exists'}), 400
    if len(password) < 8:
        return jsonify({'result': 'failed', 'reason': 'password is too short'}), 400
    if mailaddr == '' or password == '' or regip == '' or regdate == '':
        return jsonify({'result': 'failed', 'reason': 'invalid request'}), 400
    
    # メアドがoit.ac.jp, *.oit.ac.jpでない場合は登録しない
    maildomain = mailaddr.split('@')
    if not maildomain[1].endswith('oit.ac.jp'):
        return jsonify({'result': 'failed', 'reason': 'mail address domain is not authorized'}), 400
    
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
    
    return jsonify({'result': 'success'}), 200