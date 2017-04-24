from flask import Flask
from flask import request
from messages import ReceiveMessage
from messages import ReplayTextMessage
from messages import ReplayImageMessage

import hashlib

app = Flask(__name__)


@app.route('/wx', methods=['GET'])
def check_echostr():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    args = ["ry96", timestamp, nonce]
    args.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, args)
    hashcode = sha1.hexdigest()
    return echostr if hashcode == signature else ""


@app.route('/wx', methods=['POST'])
def receive_message():
    message = ReceiveMessage(request.data)
    if message.MsgType == 'text':
        return ReplayTextMessage(message.ToUserName, message.FromUserName, "test")
    elif message.MsgType == 'image':
        return ReplayImageMessage(message.ToUserName, message.FromUserName, message.MediaId)
    else:
        print message
        return "success"


if __name__ == '__main__':
    app.run(port=80, debug=True)
