from flask import Flask
from flask import request
from messages import ReceiveMessage
from messages import ReplayTextMessage
from messages import ReplayImageMessage
from messages import ReplayNewsMessage

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
        res = ReplayNewsMessage(message.FromUserName, message.ToUserName, [
            {'title': 'roger', 'description': 'news by roger', 'pic_url': "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1493731217&di=acd14bc2ebb693d65b9492a122bb1d71&imgtype=jpg&er=1&src=http%3A%2F%2Fwenwen.soso.com%2Fp%2F20070702%2F20070702182221-362233278.JPG", 'url': 'http://www.baidu.com'},
            {'title': 'seaman', 'description': 'news by seaman',
          'pic_url': "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1493136595032&di=b37631eb2154bd3e13aa61eb2373f151&imgtype=0&src=http%3A%2F%2Fh6.86.cc%2Fwalls%2F20150909%2F1440x900_4b4872ef084a65e.jpg",
          'url': 'http://www.sina.com.cn'}]).send()
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
