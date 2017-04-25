# coding=utf-8
import xml.etree.ElementTree as ET
import time


class ReceiveMessage(object):
    def __init__(self, msg):
        xml_data = ET.fromstring(msg)
        self.__find(["ToUserName", "FromUserName", "CreateTime", "MsgType", "MsgId"], xml_data)
        getattr(self, self.MsgType)(xml_data)

    def text(self, xml_data):
        self.__find("Content", xml_data)

    def image(self, xml_data):
        self.__find(["PicUrl", "MediaId"], xml_data)

    def voice(self, xml_data):
        self.__find(['MediaId', 'Format'], xml_data)

    def video(self, xml_data):
        self.__find(['MediaId', 'ThumbMediaId'], xml_data)

    def shortvideo(self, xml_data):
        self.video(xml_data)

    def location(self, xml_data):
        self.__find(['Location_X', 'Location_Y', 'Scale', 'Label'], xml_data)

    def link(self, xml_data):
        self.__find(['Title', 'Description', 'Url'], xml_data)

    def event(self, xml_data):
        self.__find(["Event", "EventKey"], xml_data, is_lower=True)
        getattr(self, "event_" + self.Event)(xml_data)

    def event_click(self, xml_data):
        pass

    def event_view(self, xml_data):
        self.__find("MenuId", xml_data)

    def event_scancode_push(self, xml_data):
        scan_code_info = xml_data.find("ScanCodeInfo")
        self.__find(["ScanType", "ScanResult"], scan_code_info)

    def event_scancode_waitmsg(self, xml_data):
        self.scancode_push(xml_data)

    def event_pic_sysphoto(self, xml_data):
        send_pics_info = xml_data.find("SendPicsInfo")
        self.__find("Count", send_pics_info)
        pic_list = send_pics_info.find("PicList")
        pics = []
        for item in pic_list:
            pics.append(item.find("PicMd5Sum").text)
        setattr(self, "PicList", pics)

    def event_pic_photo_or_album(self, xml_data):
        self.pic_sysphoto(xml_data)

    def event_pic_weixin(self, xml_data):
        self.pic_sysphoto(xml_data)

    def event_location_select(self, xml_data):
        location_info = xml_data.find("SendLocationInfo")
        self.__find(["Location_X", "Location_Y", "Scale", "Label", "Poiname"], location_info)

    def event_subscribe(self, xml_data):
        self.__find("Ticket", xml_data)

    def event_unsubscribe(self, xml_data):
        pass

    def event_scan(self, xml_data):
        self.__find('Ticket', xml_data)

    def event_location(self, xml_data):
        self.__find(['Latitude', 'Longitude', 'Precision'], xml_data)

    def __find(self, keys, xml_data, is_lower=False):
        if isinstance(keys, str):
            keys = [keys]
        for key in keys:
            element = xml_data.find(key)
            if element is not None:
                value = element.text
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


class ReplayVoiceMessage(ReplayMessage):
    def __init__(self, to_user_name, from_user_name, media_id):
        super(ReplayVoiceMessage, self).__init__('voice', to_user_name, from_user_name)
        self.media_id = media_id

    def send(self):
        return self.message.format("<Voice><MediaId><![CDATA[{0}]]></MediaId></Voice>").format(self.media_id)


class ReplayVideoMessage(ReplayMessage):
    def __init__(self, to_user_name, from_user_name, media_id, title, description):
        super(ReplayVideoMessage, self).__init__('video', to_user_name, from_user_name)
        self.media_id = media_id
        self.title = title
        self.description = description

    def send(self):
        return self.message.format("<Video><MediaId><![CDATA[{0}]]></MediaId><Title><![CDATA[{1}]]></Title><Description><![CDATA[{2}]]></Description></Video>")\
            .format(self.media_id, self.title, self.description)


class ReplayMusicMessage(ReplayMessage):
    def __init__(self, to_user_name, from_user_name, title, description, music_url, HQ_music_url, thumb_media_id):
        super(ReplayMusicMessage, self).__init__('music', to_user_name, from_user_name)
        self.title = title
        self.description = description
        self.music_url = music_url
        self.HQ_music_url = HQ_music_url
        self.thumb_media_id = thumb_media_id

    def send(self):
        return self.message.format("<Music><Title><![CDATA[{0}]]></Title><Description><![CDATA[{1}]]></Description><MusicUrl><![CDATA[{2}]]></MusicUrl><HQMusicUrl><![CDATA[{3}]]></HQMusicUrl><ThumbMediaId><![CDATA[{4}]]></ThumbMediaId></Music>")\
            .format(self.title, self.description, self.music_url, self.HQ_music_url, self.thumb_media_id)


class ReplayNewsMessage(ReplayMessage):
    def __init__(self, to_user_name, from_user_name, items):
        assert isinstance(items, list)
        super(ReplayNewsMessage, self).__init__('news', to_user_name, from_user_name)
        self.items = items

    def send(self):
        items_xml = ""
        for item in self.items:
            items_xml += """
                        <item>
                        <Title><![CDATA[{0}]]></Title> 
                        <Description><![CDATA[{1}]]></Description>
                        <PicUrl><![CDATA[{2}]]></PicUrl>
                        <Url><![CDATA[{3}]]></Url>
                        </item>
                    """.format(item.title, item.description, item.pic_url, item.url)
        return self.message.format("<ArticleCount>{0}</ArticleCount><Articles>{1}</Articles>").format(len(self.items), items_xml)
