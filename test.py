from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


#データベース作成
DB_ROOM = 'room.db'

conn = sqlite3.connect(DB_ROOM)

#データベース作成


@app.route('/room', methods=['POST'])
def room():
    try:
        data = request.get_json()  

        if data == None:
            return jsonify({'result': False})
        
        data_dict = dict(data)
        
        name = data_dict.get('name')
        Type = data_dict.get('type')

        if name == None or Type == None:
            return jsonify({'result': False})

        conn = sqlite3.connect(DB_ROOM)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, type) VALUES (?, ?)', (name, Type))
        conn.commit()
        conn.close()

        return jsonify({'result': True})

    except Exception as e:
        return jsonify({'result': False})

if __name__ == '__main__':
    initialize_database()
    app.run()
