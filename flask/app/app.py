# ライブラリのインポート
from flask import Flask, render_template
from flask_socketio import SocketIO

# 応答の関数
from request import send_text_data

# インスタンスを作成
app = Flask(__name__)
socketio = SocketIO(app)

# HTMLページに対するルーティング


@app.route('/')
def index():
    return render_template('index.html')

# 送信ボタン押下時に実行


@socketio.on('send_message')
def handle_message(data):
    # 入力されたテキストのイベントを送る
    print(f"Data received: {data}")
    socketio.emit('insert_message', {'message': data['message']})

    # APIからの応答を取得
    response_message = send_text_data(data['message'])
    print(f"API received: {response_message}")

    # クライアントに対してイベントを送る
    socketio.emit('receive_message', {'message': response_message})


if __name__ == '__main__':
    socketio.run(app, port=3000)
