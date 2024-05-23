from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


from .const import DOMAIN
from .utils.logger import LOGGER
from .utils.store import async_load_from_store
from .data_client import HassBoxDataClient


async def async_setup(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    config = await async_load_from_store(hass, "hassbox_notify.config") or None
    hass.data[DOMAIN] = HassBoxDataClient(hass=hass, config=config)

    async def handle_notify(call) -> None:
        await hass.data[DOMAIN].send(call.data)

    hass.services.async_register(DOMAIN, "hassbox_notify", handle_notify)
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    return True
