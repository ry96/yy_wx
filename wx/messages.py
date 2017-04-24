# coding=utf-8
import xml.etree.ElementTree as ET
import time


class ReceiveMessage(object):
    def __init__(self, msg):
        xml_data = ET.fromstring(msg)
        self.__find(["ToUserName", "FromUserName", "CreateTime", "MsgType", "MsgId"], xml_data)
        getattr(self, self.MsgType)(xml_data)

    def test(self, xml_data):
        self.__find("Content", xml_data)

    def image(self, xml_data):
        self.__find(["PicUrl", "MediaId"], xml_data)

    def event(self, xml_data):
        self.__find(["Event", "EventKey"], xml_data, is_lower=True)
        getattr(self, self.Event)(xml_data)

    def click(self, xml_data):
        pass

    def view(self, xml_data):
        self.__find("MenuId", xml_data)

    def scancode_push(self, xml_data):
        scan_code_info = xml_data.find("ScanCodeInfo")
        self.__find(["ScanType", "ScanResult"], scan_code_info)

    def scancode_waitmsg(self, xml_data):
        self.scancode_push(xml_data)

    def pic_sysphoto(self, xml_data):
        send_pics_info = xml_data.find("SendPicsInfo")
        self.__find("Count", send_pics_info)
        pic_list = send_pics_info.find("PicList")
        pics = []
        for item in pic_list:
            pics.append(item.find("PicMd5Sum").text)
        setattr(self, "PicList", pics)

    def pic_photo_or_album(self, xml_data):
        self.pic_sysphoto(xml_data)

    def pic_weixin(self, xml_data):
        self.pic_sysphoto(xml_data)

    def location_select(self, xml_data):
        location_info = xml_data.find("SendLocationInfo")
        self.__find(["Location_X", "Location_Y", "Scale", "Label", "Poiname"], location_info)

    def __find(self, keys, xml_data, is_lower=False):
        if isinstance(keys, str):
            keys = [keys]
        for key in keys:
            value = xml_data.find(key).text
            if value:
                value = value.lower() if is_lower else value
                value = value.encode('utf-8')
            setattr(self, key, value)


REPLAY_MESSAGE = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[{3}]]></MsgType>
                {4}
                </xml>
                """


class ReplayMessage(object):
    def __init__(self, message_type, to_user_name, from_user_name):
        self.message = REPLAY_MESSAGE.format(to_user_name, from_user_name, int(time.time()), message_type, '{0}')

    def send(self):
        return "success"


class ReplayTextMessage(ReplayMessage):
    def __init__(self, to_user_name, from_user_name, content):
        super(ReplayTextMessage, self).__init__("text", to_user_name, from_user_name)
        self.content = content

    def send(self):
        return self.message.format("<Content><![CDATA[{0}]]></Content>").format(self.content)


class ReplayImageMessage(ReplayMessage):
    def __init__(self, to_user_name, from_user_name, media_id):
        super(ReplayImageMessage, self).__init__('image', to_user_name, from_user_name)
        self.media_id = media_id

    def send(self):
        return self.message.format("<Image><MediaId><![CDATA[{0}]]></MediaId></Image>").format(self.media_id)

