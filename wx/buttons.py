

class ButtonBase(object):

    def __init__(self, name, button_type=None):
        self.name = name
        if button_type:
            self.type = button_type

    def add_sub_button(self, button):
        assert isinstance(button, ButtonBase)
        if hasattr(self, 'sub_button') is False:
            setattr(self, 'sub_button', [])
        self.sub_button.append(button.__dict__)


class SubButton(ButtonBase):

    def __init__(self, name, buttons=None):
        super(SubButton, self).__init__(name)
        if buttons is None:
            buttons = []
        self.sub_button = []
        for button in buttons:
            self.add(button)

    def add(self, button):
        assert isinstance(button, ButtonBase)
        self.sub_button.append(button.__dict__)


class ClickButton(ButtonBase):

    def __init__(self, name, key):
        super(ClickButton, self).__init__(name, 'click')
        self.key = key


class ViewButton(ButtonBase):

    def __init__(self, name, url):
        super(ViewButton, self).__init__(name, 'view')
        self.url = url


class MiniProgramButton(ButtonBase):

    def __init__(self, name, app_id, url, page_path):
        super(MiniProgramButton, self).__init__(name, 'miniprogram')
        self.appid = app_id
        self.url = url
        self.pagepath = page_path


class ScanCodeWaitMsgButton(ButtonBase):

    def __init__(self, name, key):
        super(ScanCodeWaitMsgButton, self).__init__(name, 'scancode_waitmsg')
        self.key = key


class ScanCodePushButton(ButtonBase):

    def __init__(self, name, key):
        super(ScanCodePushButton, self).__init__(name, 'scancode_push')
        self.key = key


class PicSystemPhotoButton(ButtonBase):

    def __init__(self, name, key):
        super(PicSystemPhotoButton, self).__init__(name, 'pic_sysphoto')
        self.key = key


class PicPhotoOrAlbumButton(ButtonBase):

    def __init__(self, name, key):
        super(PicPhotoOrAlbumButton, self).__init__(name, 'pic_photo_or_album')
        self.key = key


class PicWeiXinButton(ButtonBase):

    def __init__(self, name, key):
        super(PicWeiXinButton, self).__init__(name, 'pic_weixin')
        self.key = key


class LocationSelectButton(ButtonBase):

    def __init__(self, name, key):
        super(LocationSelectButton, self).__init__(name, 'location_select')
        self.key = key


class MediaIdButton(ButtonBase):

    def __init__(self, name, media_id):
        super(MediaIdButton, self).__init__(name, 'media_id')
        self.media = media_id


class ViewLimitedButton(ButtonBase):
                                                                    
    def __init__(self, name, media_id):
        super(ViewLimitedButton, self).__init__(name, 'view_limited')
        self.media_id = media_id
