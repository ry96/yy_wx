from flask import Flask
from flask import request
from messages import ReceiveMessage
from messages import ReplayTextMessage
from messages import ReplayImageMessage

import hashlib

app = Flask(__name__)


@app.route('/wx', methods=['GET'])
def check_echostr():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')

    args = ["ry96", timestamp, nonce]
    args.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, args)
    hashcode = sha1.hexdigest()
    return echostr if hashcode == signature else ""


@app.route('/wx', methods=['POST'])
def receive_message():
    res = "success"
    message = ReceiveMessage(request.data)
    if message.MsgType == 'text':
        res = ReplayTextMessage(message.FromUserName, message.ToUserName, "test").send()
    elif message.MsgType == 'image':
        res = ReplayImageMessage(message.FromUserName, message.ToUserName, message.MediaId).send()
    else:
        print message.__dict__
        res = ReplayTextMessage(message.FromUserName, message.ToUserName, "received message").send()
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
