import requests
import time


class WXClient(object):
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.__url = "https://api.weixin.qq.com/cgi-bin/{0}"
        self.session = requests.Session()
        self.__access_token = None
        self.__access_token_expires_time = None

    def add_buttons(self, buttons):
        self.__update_access_token()
        url = self.__url.format("menu/create?access_token={0}".format(self.__access_token))
        data = {'button': map(lambda b: b.__dict__, buttons) if isinstance(buttons, list) else [buttons.__dict__]}
        return self.session.post(url, json=data).json() == {"errcode": 0, "errmsg": "ok"}

    def get_buttons(self):
        self.__update_access_token()
        url = self.__url.format("menu/get?access_token={0}".format(self.__access_token))
        return self.session.get(url).json()

    def get_buttons_info(self):
        self.__update_access_token()
        url = self.__url.format("get_current_selfmenu_info?access_token={0}".format(self.__access_token))
        return self.session.get(url).json()

    def delete_buttons(self):
        self.__update_access_token()
        url = self.__url.format("menu/delete?access_token={0}".format(self.__access_token))
        return self.session.get(url).json() == {"errcode": 0, "errmsg": "ok"}

    def __update_access_token(self):
        if self.__access_token is None or self.__access_token_expires_time <= time.time():
            url = self.__url.format(
                'token?grant_type=client_credential&appid={0}&secret={1}'.format(self.app_id, self.app_secret))
            res = self.session.get(url).json()

            if 'access_token' in res and 'expires_in' in res:
                self.__access_token = res['access_token']
                self.__access_token_expires_time = time.time() + res['expires_in']
            else:
                raise Exception(res)
        return self.__access_token
