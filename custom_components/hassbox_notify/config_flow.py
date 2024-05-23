from homeassistant import config_entries

from .const import DOMAIN
from .utils.store import async_load_from_store

from .data_client import HassBoxDataClient

class HassBoxNotifyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if self.hass.data.get(DOMAIN):
            return self.async_abort(reason="single_instance_allowed")

        config = await async_load_from_store(self.hass, "hassbox_notify.config") or None
        self.data_client = HassBoxDataClient(hass=self.hass, config=config)
        result = await self.data_client.get_qrcode()
        
        if "errcode" in result and result["errcode"] == 200:
            return self.async_create_entry(title="HassBox通知报警", data={})

        if "ticket" not in result:
            return self.async_abort(
                reason="qrcode_error",
                description_placeholders={"errmsg": result["errmsg"]},
            )

        return self.async_show_form(
            step_id="bind_wechat",
            description_placeholders={
                "qr_image": '<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + result["ticket"] + '" width="250"/>'
            },
        )

    async def async_step_bind_wechat(self, user_input=None):
        result = await self.data_client.check_state()

        if result["errcode"] != 0:
            return self.async_abort(
                reason="qrcode_error",
                description_placeholders={"errmsg": result["errmsg"]},
            )

        return self.async_create_entry(title="HassBox通知报警", data={})