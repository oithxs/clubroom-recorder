import sqlite3

def db():
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        # ログイン履歴は別テーブルに格納する
        c.execute('CREATE TABLE user (mailaddr, password, salt, regdate, regip)')
        c.execute('CREATE TABLE login_history (mailaddr, logindate, loginip)')
        conn.commit()
        conn.close()