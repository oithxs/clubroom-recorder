from flask import Flask
import sqlite3
import os

app = Flask(__name__)

if os.path.exists('user.db'):
    pass
else:
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    # ログイン履歴は別テーブルに格納する
    c.execute('CREATE TABLE user (mailaddr, password, salt, regdate, regip)')
    c.execute('CREATE TABLE login_history (mailaddr, logindate, loginip, authresult)')
    conn.commit()
    conn.close()