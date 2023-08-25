from flask import Flask, request, jsonify
import sqlite3
import datetime
app = Flask(__name__)

#ファイル変数
DB_Room = 'room.db'
TXT_LOG = 'history.log'

@app.route('/room', methods=['POST'])
def room():#POST/ROOM実行関数
    try:
        data_dict = dict(request.get_json())     
        Name = data_dict.get('name')
        Type = data_dict.get('type')
        if Name == None or Type == None:
            return jsonify({'result-notName': False})

        UpDate(Name, Type)
        return jsonify({'result': True})
    
    except Exception as e:
        return jsonify({'result-error': "Error"})

def WriteLog(name,type,Message):#LOG書き込み関数
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    f = open(TXT_LOG, 'a')
    f.write(f'{now} || {name.ljust(15)}|{type.ljust(20)}|{Message}\n')
    f.close()

def SignUp(name):#ユーザー登録関数
    Conn_Room = sqlite3.connect(DB_Room)
    Cur_Room = Conn_Room.cursor()
    Cur_Room.execute('SELECT Name FROM room WHERE Name = ?;',(name,))
    if Cur_Room.fetchone() != None: #nameが存在する場合
        Conn_Room.close()
        WriteLog(name,'sign-up error', 'This name is already in use')
        return False
    else:                           #nameが存在しない場合
        Cur_Room.execute('INSERT INTO room(Name) values(?)',(name,))
        Conn_Room.commit()
        Conn_Room.close()
        WriteLog(name, 'sign-up log', 'Hello! new user')
        print(name + "を作成しました")
        return True

def ChangeName(name,new_name):
    print("changeName")

def UpDate(name, type):#入退室更新関数
    Conn_Room = sqlite3.connect(DB_Room)
    Cur_Room = Conn_Room.cursor()
    Cur_Room.execute('SELECT Name FROM room WHERE Name = ?;',(name,))
    if Cur_Room.fetchone() != None:  #nameが存在する場合
        if(type == "entering"):
            Cur_Room.execute('UPDATE room SET InTheRoom= TRUE WHERE name = ?', (name,))
            Conn_Room.commit()
            WriteLog(name, 'normal log', 'Entered the clubroom')
            print(name + "を状態Entryにしました。")
        elif(type == "leaving"):
            Cur_Room.execute('UPDATE room SET InTheRoom= FALSE WHERE name = ?', (name,))
            Conn_Room.commit()
            WriteLog(name, 'normal log', 'Left the clubroom')
            print(name + "を状態Leveaingにしました。")
        else:
            Conn_Room.close()
            return False
        Conn_Room.close()
        return True
    else:
        Conn_Room.close()
        WriteLog(name, 'normal error', 'This name does not exist')
        print(name + "は存在しません")
        return False
    
def ReSet():#入退室リセット関数
    Conn_Room = sqlite3.connect(DB_Room)
    Cur_Room = Conn_Room.cursor()
    Cur_Room.execute('SELECT Name FROM room WHERE InTheRoom = TRUE;')
    for name in Cur_Room:
        WriteLog(name[0], 'Reset error', 'Haven\'t left')
        print(name[0] + "が退室していません")
    Cur_Room.execute('UPDATE room SET InTheRoom= FALSE')
    Conn_Room.commit()
    Conn_Room.close()

if __name__ == '__main__':#Flask起動
    app.run()