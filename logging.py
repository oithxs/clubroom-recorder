import sqlite3

def log(mailaddr, logindate, loginip, authresult):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('INSERT INTO login_history VALUES (?, ?, ?)', (mailaddr, logindate, loginip, authresult))
    conn.close()