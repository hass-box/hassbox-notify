import aiohttp
import datetime

from homeassistant.components import persistent_notification

from .utils.logger import LOGGER
from .utils.store import async_save_to_store

base_url = "https://hassbox.cn/api/public/"
app_id = "gh_07ec63f43481"

class HassBoxDataClient:
    hass = None
    session = None
    token = None

    def __init__(self, hass, config=None):
        self.hass = hass
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        if config is not None:
            self.token = config["token"]

    async def __fetch(self, api, data, header=None):
        data["appId"] = app_id
        async with self.session.post(base_url + api, json=data) as response:
            result = await response.json()
            return result

    async def get_qrcode(self):
        poat_data = { "token": self.token }
        result = await self.__fetch("notify/getQRCode", poat_data)
        if "token" in result:
            self.token = result["token"]
        return result

    async def check_state(self):
        post_data = {"token": self.token}
        result = await self.__fetch("notify/checkState", post_data)
        if "token" in result:
            self.token = result["token"]
            await async_save_to_store(
                self.hass, "hassbox_notify.config", {"token": result["token"]}
            )
            return {"errcode": 0}
        else:
            return {"errcode": 1, "errmsg": result["errmsg"]}

    async def send(self, data):
        time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        post_data = {
            "data": data,
            "time": time,
            "token": self.token,
        }
        result = await self.__fetch("notify/send", post_data)
        LOGGER.warning(result)
        if "errmsg" in result:
            self.show_notification(data, time, result["errmsg"])

        if "wechat" in result and "errmsg" in result["wechat"]:
            self.show_notification(data, time, result["wechat"]["errmsg"])

        if "sms" in result:
            for item in result["sms"]:
                if "errmsg" in item:
                    self.show_notification(data, time, item["errmsg"])

        if "voice" in result:
            for item in result["voice"]:
                if "errmsg" in item:
                    self.show_notification(data, time, item["errmsg"])

        
    def show_notification(self, data, time, errmsg):

        persistent_notification.create(
            self.hass, errmsg + "\n\n报警内容：" + data["message"] + "\n报警时间：" + time, title="HassBox通知报警"
        )
