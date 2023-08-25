import sqlite3

def MakeTable(file_name):
    Conn = sqlite3.connect(file_name)
    Cur = Conn.cursor()
    Cur.execute('CREATE TABLE room(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name STRING NOT NULL, InTheRoom BOOLEAN DEFAULT FALSE)')
    Conn.close()

def Look(file_name):
    print("--  --  --  --  --")
    print("id  name   InTheRoom")
    Conn = sqlite3.connect(file_name)
    Cur = Conn.cursor()
    Cur.execute('SELECT * FROM room')
    for row in Cur :
        print(row)
    Conn.close()
    
Look('room.db')