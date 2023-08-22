import sqlite3
import bcrypt
import os.path

def create_sqlite3():
    # データベースが存在しない場合は作成する
    if not os.path.isfile('user.db'):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        # ログイン履歴は別テーブルに格納する
        c.execute('CREATE TABLE user (mailaddr, password, salt, regdate, regip)')
        c.execute('CREATE TABLE login_history (mailaddr, login_date, login_ip)')
        conn.commit()
        conn.close()

def reg(mailaddr, password, regip, regdate):
    # ユーザーのメールアドレスが既に登録されているかどうかを確認する
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('SELECT * FROM user WHERE mailaddr = ?', (mailaddr,))
    result = c.fetchone()
    conn.close()

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